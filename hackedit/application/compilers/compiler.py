import logging
import os

from PyQt5 import QtCore
from hackedit.application import system
from hackedit.application.constants import TargetType
from hackedit.application.utilities import msvc
from hackedit.application.utilities.blocking_process import BlockingProcess


class Compiler:
    """
    Base class for implementingnew compiler, provides some helper methods to run commands in a subprocess (setup
    environemnt, run process and parse its output into checker messages).

    Sucblasses may implement one of the following methods (if they are not implemented, the feature is just disabled):

        - get_version: get the compiler version.
        - check_compiler: check if the compiler is working.
        - check_file: check a file (linter) and report any warnings/errors.
        - compile_file: compile a single file.
        - compile_files: compile a series of file and link them together.

    Helper methods:

        - setup_environemt: setup a QProcessEnvironement based on the compiler config
        -
    """
    #: associated mimetypes
    mimetypes = []

    #: type name of the compiler
    type_name = ''

    def __init__(self, config, working_dir=os.path.expanduser('~'), print_output=True):
        """
        :param config: the associated compiler configuration
        :param working_dir: working directory used to run the compiler process.
        :param print_output: True to print the compiler output to stdout.
        """
        self.print_output = print_output
        self.config = config
        self.working_dir = working_dir

    def get_version(self, include_all=True):
        """
        Gets the compiler version string.

        :param include_all: True to include the whole version information, False to get the version number only.
        """
        raise NotImplementedError()

    def check_compiler(self):
        """
        Checks if the compiler is working.

        :raises: CompilerCheckFailedError if the check failed.
        """
        raise NotImplementedError()

    def compile_files(self, sources, destination, target_name, target_type=TargetType.EXECUTABLE):
        """
        Compile a series of files and link them together (if necessary).
        """
        raise NotImplementedError()

    def get_process_environment(self):
        """
        Returns the process environemnt that needs to be setup to run a compiler command or to run the compiled
        program.

        :rtype: QtCore.QProvessEnvironment
        """
        env = QtCore.QProcessEnvironment()

        # setup system environemnts except PATH
        for k, v in os.environ.items():
            if k != 'PATH':
                env.insert(k, v)

        PATH = os.environ['PATH']

        # Retrieve msvc environment vars if needed
        if system.WINDOWS and self.config.vcvarsall:
            vc_vars = msvc.query_vcvarsall(self.config.vcvarsall, self.config.vcvarsall_arch)
            for k, v in vc_vars.items():
                if k != 'path':
                    env.insert(k, v)
                else:
                    # we can safely replace original env by the one returned
                    # by vcvarsall as it includes what is defined in our
                    # process
                    PATH = v

        # Setup compiler environement variables
        for k, v in self.config.environment_variables.items():
            if not v:
                continue
            if k == 'PATH':
                # special case for PATH, best is to prepend to the existing system path
                PATH = v + os.pathsep + PATH
            env.insert(k, v)

        # Prepend compiler path
        compiler_path = self.get_full_compiler_path()
        if compiler_path and os.path.exists(os.path.dirname(compiler_path)):
            compiler_dir = os.path.dirname(compiler_path)
            PATH = compiler_dir + os.pathsep + PATH

        env.insert('PATH', PATH)

        return env

    def get_full_compiler_path(self):
        """
        Resolves the full compiler path using the PATH environment variable if the compiler command is not an
        absolute path.
        """
        if os.path.exists(self.config.compiler):
            return self.config.compiler
        else:
            try:
                PATH = self.config.environment_variables['PATH']
            except KeyError:
                PATH = ''
            PATH += os.pathsep + os.environ['PATH']
            path = system.which(self.config.compiler, path=PATH)
            if path is None:
                path = ''
            return path

    def _make_destination_folder(self, destination):
        """
        Creates the destination folder, destination may be a relative path (relative to the compiler's working dir).
        """
        destination = os.path.expanduser(destination)
        if os.path.isabs(destination):
            abs_dest = destination
        else:
            abs_dest = os.path.join(self.working_dir, destination)
        if not os.path.exists(abs_dest):
            os.makedirs(abs_dest)

    def _is_outdated(self, source, destination):
        """
        Checks if the destination is outdated (i.e. the source is newer than the destination).
        """
        try:
            if not os.path.isabs(source):
                source = os.path.join(self.working_dir, source)
            if not os.path.isabs(destination):
                destination = os.path.join(self.working_dir, destination)
            try:
                return os.path.getmtime(source) > os.path.getmtime(destination)
            except OSError:
                return True
        except (TypeError, AttributeError):
            raise ValueError('Invalid source and destinations')

    def _run_compiler_command(self, args):
        """
        Run a compiler command in a subprocess and returns its return code and output.

        .. note:: The output will be printed to stdout if the ``print_output`` parameter of the constructor has been
            set to True.

        :param args: compiler arguments.
        :returns: (return_code, output)
        :rtype: (int, str)
        """
        env = self.get_process_environment()
        _logger().debug('compiler command: %s', ' '.join([self.config.compiler] + args))
        _logger().debug('working directory: %s', self.working_dir)
        _logger().debug('compiler environment: %s', env.toStringList())
        process = BlockingProcess(working_dir=self.working_dir, environment=env, print_output=self.print_output)
        exit_code, output = process.run(self.config.compiler, args)
        _logger().debug('exit code: %d', exit_code)
        _logger().debug('output:\n%s', output)
        return exit_code, output


def _logger():
    return logging.getLogger(__name__)