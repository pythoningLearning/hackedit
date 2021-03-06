import logging
import os
import re

from PyQt5 import QtCore

from hackedit.api import utils, system


class InterpreterConfig(utils.JSonisable, utils.Copyable):
    def __init__(self):
        self.name = ''
        self.command = ''
        self.type_name = ''
        self.mimetypes = []
        self.environment_variables = {}
        self.command_pattern = '$command $interpreter_arguments $script $script_arguments'
        self.version_command = ['--version']
        self.version_regex = r'(?P<version>\d\.\d\.\d)'
        self.test_command = []

    def __repr__(self):
        return 'InterpreterConfig(%s)' % self.to_json()


class InterpreterCheckFailed(utils.ProgramCheckFailedError):
    def __init__(self, type_name, *args, **kwargs):
        super().__init__(type_name, _logger, *args, **kwargs)


class Interpreter:
    def __init__(self, config, working_directory='', print_output=False):
        """
        :type config: InterpreterConfig
        :type working_directory: str
        :type print_output: bool
        """
        self.config = config
        self.working_directory = working_directory
        self.print_output = print_output

    def get_version(self, include_all=False):
        """
        Gets the interpreter version using config.version_command_args and config.version_regex
        """
        def get_version_number(text):
            for l in text.splitlines():
                prog = re.compile(self.config.version_regex)
                m = prog.match(l)
                for m in prog.finditer(l):
                    if m:
                        try:
                            return m.group('version')
                        except IndexError:
                            _logger().warn('matched regex does not contain a capute groupe named "version"')
                            continue
            return text.splitlines()[0]

        _logger().info('getting interpreter version: %s', ' '.join(
            [self.config.command] + self.config.version_command))
        ret_val = _('version not found')
        exists = os.path.exists(self.get_full_path())
        if exists and self.config.version_command:
            status, output = self._run_command(self.config.version_command)
            if status == 0 and output:
                ret_val = output if include_all else get_version_number(output)
        elif not exists:
            ret_val = _('Interpreter not found')
        _logger().info('interpreter version: %s', ret_val)
        return ret_val

    def _run_command(self, args):
        _logger().debug('interpreter command: %s', ' '.join([self.config.command] + args))
        process = utils.BlockingProcess(working_dir=self.working_directory, print_output=self.print_output)
        process.setProcessEnvironment(self.get_process_environment())
        exit_code, output = process.run(self.config.command, args)
        _logger().debug('exit code: %d', exit_code)
        _logger().debug('output:\n%s', output)
        return exit_code, output

    def check(self):
        _logger().info('checking interpreter config %r: %s', self.config.name, self.config.to_json())
        if not os.path.exists(self.get_full_path()):
            raise InterpreterCheckFailed(self.config.type_name, _('Interpreter path does not exists'), -1)
        if not self.config.mimetypes:
            raise InterpreterCheckFailed(self.config.type_name, _('There is no associated mime types'), -1)
        if not self.config.command_pattern:
            raise InterpreterCheckFailed(self.config.type_name, _('There is no command pattern'), -1)
        if self.config.test_command:
            exit_code, output = self._run_command(self.config.test_command)
            if exit_code != 0:
                raise InterpreterCheckFailed(self.config.type_name,
                                             _('Test command terminated with a non-zero exit code.'), exit_code)
            _logger().info('interpreter check succeeded')
        else:
            raise InterpreterCheckFailed(self.config.type_name, _(
                "Cannot perform interpreter check because we don't know how to create a validation test for this "
                'type of interpreter.\n'
                'The configuration seems correct but the interpreter might not work...'),
                0, error_level=InterpreterCheckFailed.WARNING)

    def make_command(self, script, script_arguments=None, interpreter_arguments=None):
        options = {
            'command': self.config.command,
            'interpreter_arguments': interpreter_arguments if interpreter_arguments else [],
            'script': script,
            'script_arguments': script_arguments if script_arguments else []
        }
        return utils.CommandBuilder(self.config.command_pattern, options).as_list()

    def get_full_path(self):
        if os.path.exists(self.config.command):
            return os.path.realpath(self.config.command)
        else:
            try:
                PATH = self.config.environment_variables['PATH']
            except KeyError:
                PATH = ''
            PATH += os.pathsep + os.environ['PATH']
            path = system.which(self.config.command, path=PATH)
            if path is None:
                path = ''
            else:
                path = os.path.realpath(path)
            return path

    def get_process_environment(self):
        env = QtCore.QProcessEnvironment()

        # setup system environment variables except PATH
        for k, v in os.environ.items():
            if k != 'PATH':
                env.insert(k, v)

        path = os.environ['PATH']

        # Setup interpreter environment variables
        for k, v in self.config.environment_variables.items():
            if not v:
                continue
            if k == 'PATH':
                # special case for PATH, best is to prepend to the existing system path
                path = v + os.pathsep + path
            env.insert(k, v)

        # Prepend interpreter path
        interpreter_path = self.get_full_path()
        if interpreter_path and os.path.exists(os.path.dirname(interpreter_path)):
            compiler_dir = os.path.dirname(interpreter_path)
            path = compiler_dir + os.pathsep + path

        env.insert('PATH', path)

        return env


class Package:
    """
    Stores the data of a package.
    """
    def __init__(self):
        self.name = ''
        self.current_version = ''
        self.latest_version = ''

    @property
    def outdated(self):
        """
        Tells whether the package is outdated or not
        """
        return self.latest_version != self.current_version

    def __repr__(self):
        if self.latest_version:
            return ' '.join([self.name, self.current_version, self.latest_version])
        return ' '.join([self.name, self.current_version])


class PackageManager:
    """
    Base class for adding an interpreter package manager to hackedit.

    This class is responsible for running the needed commands to:
        - get the list of installed packages
        - install, update or uninstall a series of packages
    """
    def __init__(self, config):
        """
        :param config: InterpreterConfig
        """
        self.config = config
        self.last_command = ''

    def get_installed_packages(self):
        """
        Returns a list of installed packages with their current and latest version.

        :rtype: [Package]
        """
        raise NotImplementedError()

    def install_packages(self, packages):
        """
        Installs the specified packages.

        :type packages: [str]

        :returns: The package manager process' exit code and output.
        :rtype: tuple(int, str)
        """
        raise NotImplementedError()

    def uninstall_packages(self, packages):
        """
        Uninstalls the specified packages.

        :type packages: [str]

        :returns: The package manager process' exit code and output.
        :rtype: tuple(int, str)
        """
        raise NotImplementedError()

    def update_packages(self, packages):
        """
        Updates the specified packages.

        :type packages: [str]

        :returns: The package manager process' exit code and output.
        :rtype: tuple(int, str)
        """
        raise NotImplementedError()

    def _run_command(self, program, args):
        self.last_command = ' '.join([program] + args)
        _logger().debug('package manager command: %s', self.last_command)
        process = utils.BlockingProcess(print_output=False, working_dir=os.path.expanduser('~'))
        exit_code, output = process.run(program, args)
        _logger().debug('exit code: %d', exit_code)
        _logger().debug('output:\n%s', output)
        return exit_code, output


def check(interpreter):
    """
    Check if the interpreter instance works. The result is cached to prevent testing configurations that have already
    been tested.

    :raises: InterpreterCheckFailedError
    """
    classname = interpreter.__class__.__name__
    json_config = interpreter.config.to_json()
    _perform_check(classname, json_config, interpreter=interpreter)


def get_version(interpreter, include_all=False):
    """
    Gets the version of the specified compiler and cache the results to prevent from running the compiler process
    uselessy.

    :returns: the compiler's version
    """
    path = interpreter.config.command
    return _get_version(path, include_all, interpreter=interpreter)


@utils.memoize_args
def _perform_check(classname, json_config, interpreter=None):
    if interpreter:
        interpreter.check()


@utils.memoize_args
def _get_version(interpreter_path, include_all, interpreter=None):
    if interpreter:
        return interpreter.get_version(include_all=include_all)
    return ''


def _logger():
    return logging.getLogger(__name__)
