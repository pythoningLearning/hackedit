"""
API modules that provides the base classes for adding support for a new pre-compiler in hackedit.

A pre-compiler is any tool that convert a source file of some type to a source file of another type (e.g. sass, bison,
flex or all the COBOL preparsers tools).
"""
import logging
import re
import os
from hackedit.api import utils
import tempfile


class PreCompilerConfig(utils.JSonisable, utils.Copyable):
    def __init__(self):
        #: name of the configuration
        self.name = ''

        #: path of the pre-compiler
        self.path = ''

        #: the list of associated extensions
        self.associated_extensions = []

        #: the list of pre-compiler flags
        self.flags = []

        #: the pre-compiler output pattern, used to deduce the pre-compiler output file path
        #:
        #: E.g.::
        #:
        #:    $input_file_name.abc (file.xyz -> file.abc)
        #:
        self.output_pattern = ''

        #: describes how to build the pre compiler command
        #: the following macros can be used:
        #:    - $input_file
        #:    - $input_file_name
        #:    - $output_file
        #:    - $output_file_name
        #:    - $flags
        #:
        self.command_pattern = ''

        #: set whether the command pattern is editable, False by default
        self.command_pattern_editable = False

        #: the content of the test file used to test the pre-compiler automatically
        self.test_file_content = ''

        #: the arguments needed to check the version:
        self.version_command_args = []

        #: the regex used to extract the version info from the version_command output
        self.version_regex = r'(?P<version>\d\.\d\.\d)'

        #: PreCompiler type name
        self.type_name = ''


class PreCompilerCheckFailed(utils.ProgramCheckFailedError):
    def __init__(self, *args, **kwargs):
        super().__init__('PreCompiler', _logger, *args, **kwargs)


class PreCompiler:
    """
    Pre-compiles a source file of one type into a source file of another type.

    The entire pre-compile process is driven by the precompiler config.
    """
    def __init__(self, config, working_dir=os.path.expanduser('~'), print_output=True):
        """
        :type config: PreCompilerConfig
        """
        self.print_output = print_output
        self.working_dir = working_dir
        self.config = config

    def get_output_file_name(self, input_file_path):
        """
        Gets the output filename for the specified input input_file_path.
        """
        input_file_name = os.path.splitext(os.path.split(input_file_path)[1])[0]
        # todo use a command builder and also use it in the compiler API
        command_builder = utils.CommandBuilder(self.config.output_pattern, {
            'input_file_name': input_file_name,
            })
        return command_builder.as_string()

    def get_output_path(self, input_file_path):
        file_name = self.get_output_file_name(input_file_path)
        return os.path.join(self.working_dir, file_name)

    def get_version(self, include_all=False):
        """
        Gets the precompiler version using config.version_command_args and config.version_regex
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

        _logger().info('getting pre-compiler version: %s', ' '.join(self.config.version_command_args))
        ret_val = _('version not found')
        exists = os.path.exists(self.config.path)
        if exists and self.config.version_command_args:
            status, output = self._run_command(self.config.version_command_args)
            if status == 0 and output:
                ret_val = output if include_all else get_version_number(output)
        elif not exists:
            ret_val = _('PreCompiler not found')
        _logger().info('pre-compiler version: %s', ret_val)
        return ret_val

    def pre_compile_file(self, file):
        """
        Pre-compile the specified file.

        The command is built using the config.command_pattern.
        """
        output_path = self.get_output_file_name(file)
        command = self._make_command(file, output_path)
        if not self._is_outdated(file, output_path):
            if self.print_output:
                print(command.as_string())
                print('pre-compilation skipped, up to date')
            return 0, 'pre-compilation skipped, up to date'
        return self._run_command(command.as_list())

    def check_pre_compiler(self):
        """
        Checks if pre-compiler works.
        """
        def rm_file(path):
            path = resolve_path(path)
            if os.path.exists(path):
                try:
                    os.remove(resolve_path(path))
                except OSError:
                    return False
            return True

        def resolve_path(path):
            return os.path.join(self.working_dir, path)

        def create_test_file():
            ext = self.config.associated_extensions[0].replace('*', '')
            file_name = 'test' + ext
            path = resolve_path(file_name)
            rm_file(path)
            with open(path, 'w') as f:
                f.write(self.config.test_file_content)
            return file_name

        def perform_check():
            self.working_dir = tempfile.gettempdir()
            input_path = create_test_file()
            output_path = self.get_output_file_name(input_path)
            abs_output_path = resolve_path(output_path)
            if not rm_file(output_path):
                raise PreCompilerCheckFailed(
                    _('Failed to remove %r before checking if pre-compilation works.\n'
                      'Please remove this file before attempting a new pre-compilation check!') %
                    abs_output_path, -1, error_leve=PreCompilerCheckFailed.WARNING)
            exit_code, output = self.pre_compile_file(input_path)
            if exit_code != 0 or not os.path.exists(abs_output_path):
                raise PreCompilerCheckFailed(output, exit_code)
            with open(abs_output_path) as fout:
                content = fout.read()
            if not content:
                raise PreCompilerCheckFailed(_('PreCompiler output file is empty. This may indicate a configuration '
                                               'issue.\n\nTest Output:\n%r') % output, exit_code)
            # check succeeded, clean up time
            rm_file(input_path)
            rm_file(output_path)

        _logger().info('checking pre-compiler config %r: %s', self.config.name, self.config.to_json())
        if not os.path.exists(self.config.path):
            raise PreCompilerCheckFailed(_('PreCompiler path does not exists'), -1)
        if not self.config.associated_extensions:
            raise PreCompilerCheckFailed(_('There is no associated extensions'), -1)
        if not self.config.output_pattern:
            raise PreCompilerCheckFailed(_('There is no output pattern'), -1)
        if not self.config.command_pattern:
            raise PreCompilerCheckFailed(_('There is no command pattern'), -1)
        if self.config.test_file_content:
            try:
                perform_check()
            except OSError as e:
                raise PreCompilerCheckFailed(_('An unexpected error occured: %s') % e, -1)
            else:
                _logger().info('pre-compiler check succeeded')
        else:
            raise PreCompilerCheckFailed(_(
                "Cannot perform pre-compiler check because we don't know how to create a validation test for this "
                'type of pre-compiler.\n'
                'The configuration seems correct but the pre-compiler might not work...'),
                0, error_level=PreCompilerCheckFailed.WARNING)

    def _is_outdated(self, source, destination):
        return utils.is_outdated(source, destination, working_dir=self.working_dir)

    def _make_command(self, input_path, output_path):
        options = {
            'input_file': input_path,
            'input_file_name': os.path.splitext(input_path)[0],
            'output_file': output_path,
            'output_file_name': os.path.splitext(output_path)[0],
            'flags': self.config.flags
        }
        builder = utils.CommandBuilder(self.config.command_pattern, options)
        return builder

    def _run_command(self, args):
        _logger().debug('pre-compiler command: %s', ' '.join([self.config.path] + args))
        process = utils.BlockingProcess(working_dir=self.working_dir, print_output=self.print_output)
        exit_code, output = process.run(self.config.path, args)
        _logger().debug('exit code: %d', exit_code)
        _logger().debug('output:\n%s', output)
        return exit_code, output


def check_pre_compiler(pre_compiler):
    """
    Check if the compiler instance works. The result is cached to prevent testing configurations that have already
    been tested.

    :raises: CompilerCheckFailedError in case of failure
    """
    classname = pre_compiler.__class__.__name__
    json_config = pre_compiler.config.to_json()
    _perform_check(classname, json_config, pre_compiler=pre_compiler)


def get_version(pre_compiler, include_all=False):
    """
    Gets the version of the specified compiler and cache the results to prevent from running the compiler process
    uselessy.

    :returns: the compiler's version
    """
    path = pre_compiler.config.path
    return _get_version(path, include_all, pre_compiler=pre_compiler)


@utils.memoize_args
def _perform_check(classname, json_config, pre_compiler=None):
    if pre_compiler:
        pre_compiler.check_pre_compiler()


@utils.memoize_args
def _get_version(compiler_path, include_all, pre_compiler=None):
    if pre_compiler:
        return pre_compiler.get_version(include_all=include_all)
    return ''


def _logger():
    return logging.getLogger(__name__)
