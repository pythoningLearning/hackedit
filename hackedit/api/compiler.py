"""
API modules that provides the base classes for adding support for a new compiler in hackedit.
"""
import functools
import copy
import json
import locale
import logging
import os
import re
import sys

from PyQt5 import QtCore, QtWidgets

from hackedit.api import system, utils
from hackedit.app import msvc
from hackedit.app.forms import compiler_config_ui


class TargetType:
    """
    Enumerates the possible target type.
    """
    EXECUTABLE = 0
    SHARED_LIBRARY = 1
    STATIC_LIBRARY = 2
    OBJECT_FILE = 3


class CompilerConfig:
    """
    Stores a compiler configuration.
    """
    def __init__(self):
        #: Name of the configuration
        self.name = ''
        #: Directory where the compiler can be found, use an emtpy path to use the system configuration.
        self.compiler = ''
        #: Compiler flags that will be appended to every compiler command.
        self.flags = []
        #: List of include paths (used for copybooks in COBOL).
        self.include_paths = []
        #: List of libraries to include
        self.library_paths = []
        #: List of libraries to link with
        self.libraries = []
        #: Custom environment variables
        self.environment_variables = {}
        self.vcvarsall = ''
        self.vcvarsall_arch = 'x86'
        #: type_name of the associated compiler
        self.type_name = ''

    def to_json(self):
        """
        Converts the configuration to a json object
        """
        return json.dumps(self.__dict__, indent=4, sort_keys=True)

    def from_json(self, json_content):
        """
        Import config values from a json object.
        """
        content = json.loads(json_content)
        for k, v in content.items():
            setattr(self, k, v)
        return self

    def copy(self):
        """
        Returns a copy of the configuration that can be changed without altering this instance.
        """
        return copy.deepcopy(self)

    def __repr__(self):
        return 'CompilerConfig(' + self.to_json() + ')\n'


class CompilerConfigWidget(QtWidgets.QWidget):
    """
    Base class for writing a compiler configuration widget. Such a widget is used to edit the options of a compiler
    configuration (all settings except the compiler directory and the environment variables).
    """
    def is_dirty(self):
        return self._original_config.to_json() != self.get_config().to_json()

    def set_config(self, config):
        """
        Sets the compiler configuration (update widget properties).

        :param config: CompilerConfig
        """
        self._original_config = config
        self._config = config.copy()

    def get_config(self):
        """
        Gets the edited compiler configuration.

        :rtype: CompilerConfig
        """
        return self._config


class GenericCompilerCongigWidget(CompilerConfigWidget):
    """
    Generic _config widgets that let user define the include paths, the library paths, the libraries to link
    with and add custom compiler switches.
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = compiler_config_ui.Ui_Form()
        self.ui.setupUi(self)
        self.ui.bt_abs_include_path.clicked.connect(self._add_abs_include_path)
        self.ui.bt_rel_include_path.clicked.connect(self._add_rel_include_path)
        self.ui.bt_delete_include_path.clicked.connect(self._rm_include_path)
        self.ui.bt_abs_lib_path.clicked.connect(self._add_abs_lib_path)
        self.ui.bt_rel_lib_path.clicked.connect(self._add_rel_lib_path)
        self.ui.bt_delete_lib_path.clicked.connect(self._rm_library_path)

    def set_config(self, config):
        assert isinstance(config, CompilerConfig)
        super().set_config(config)
        self.ui.edit_flags.setText(' '.join(config.flags))
        self.ui.list_include_paths.clear()
        for path in config.include_paths:
            item = QtWidgets.QListWidgetItem()
            item.setText(path)
            self.ui.list_include_paths.addItem(item)
        self.ui.list_lib_paths.clear()
        for path in config.library_paths:
            item = QtWidgets.QListWidgetItem()
            item.setText(path)
            self.ui.list_lib_paths.addItem(item)
        self.ui.edit_libs.setText(' '.join(config.libraries))

    def get_config(self):
        self._config.flags = [token for token in self.ui.edit_flags.text().split(' ') if token]
        self._config.libraries = [token for token in self.ui.edit_libs.text().split(' ') if token]
        self._config.include_paths.clear()
        for i in range(self.ui.list_include_paths.count()):
            path = self.ui.list_include_paths.item(i).text()
            if path:
                self._config.include_paths.append(path)
        self._config.library_paths.clear()
        for i in range(self.ui.list_lib_paths.count()):
            path = self.ui.list_lib_paths.item(i).text()
            if path:
                self._config.library_paths.append(path)
        return super().get_config()

    def _add_abs_include_path(self):  # pragma: no cover
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, _('Select an include path'), os.path.expanduser('~'))
        if path:
            self.ui.list_include_paths.addItem(os.path.normpath(path))

    def _add_rel_include_path(self):  # pragma: no cover
        path, status = QtWidgets.QInputDialog.getText(
            self, _('Add relative include path'), 'Path:')
        if status:
            self.ui.list_include_paths.addItem(path)

    def _rm_include_path(self):  # pragma: no cover
        current = self.ui.list_include_paths.currentRow()
        if current != -1:
            self.ui.list_include_paths.takeItem(current)

    def _add_abs_lib_path(self):  # pragma: no cover
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, _('Select a library path'), os.path.expanduser('~'))
        if path:
            self.ui.list_lib_paths.addItem(os.path.normpath(path))

    def _add_rel_lib_path(self):  # pragma: no cover
        path, status = QtWidgets.QInputDialog.getText(
            self, _('Add relative library path'), 'Path:')
        if status:
            self.ui.list_lib_paths.addItem(path)

    def _rm_library_path(self):  # pragma: no cover
        current = self.ui.list_lib_paths.currentRow()
        if current != -1:
            self.ui.list_lib_paths.takeItem(current)


class CompilerOutputParser:
    """
    Parses output of compiler commands.

    You can extend the output parser capabilities by using different patterns. We highly suggest that you append
    new patterns to :attr:`CompilerOutputParser.OUTPUT_PATTERNS`.
    """
    # Gcc output pattern
    OUTPUT_PATTERN_GCC = re.compile(
        r'^(?P<filename>[\w\.\-_\s/]*):(?P<line>\s*\d*):(?P<column>\s*\d*)?:?(?P<level>[\w\s]*):(?P<msg>.*)$')

    # MSVC output pattern
    OUTPUT_PATTERN_MSVC = re.compile(
        r'^(?P<filename>[\w\.\-_\s]*)\((?P<line>\s*\d*)\):(?P<level>[\w\s]*):'
        '(?P<msg>.*)$')

    #: Default output patterns.
    OUTPUT_PATTERNS = [OUTPUT_PATTERN_GCC, OUTPUT_PATTERN_MSVC]

    def __init__(self, patterns=None):
        if patterns is None:
            patterns = CompilerOutputParser.OUTPUT_PATTERNS
        self.patterns = patterns

    def parse(self, output, working_dir, use_tuples=False):
        """
        Parses compiler command output.

        :param output: compiler output string
        :param working_dir: working directory of the compiler, used to find the absolute path of relative file paths.
        :param use_tuples: True to return a list of tuple instead of a list of
            :class:`pyqode.core.modes.CheckerMessage`
        :returns: a list of messages.
        """
        from pyqode.core.modes import CheckerMessages
        if not use_tuples:
            from pyqode.core.modes import CheckerMessage
        issues = []
        for line in output.splitlines():
            if not line:
                continue
            for ptrn in self.patterns:
                m = ptrn.match(line)
                if m is not None:
                    try:
                        filename = m.group('filename')
                    except IndexError:
                        filename = ''
                    try:
                        line_nbr = int(m.group('line')) - 1
                    except IndexError:
                        line_nbr = 0
                    try:
                        level = m.group('level')
                    except IndexError:
                        level = 'warning'
                    try:
                        message = m.group('msg')
                    except IndexError:
                        continue  # a message capture group is mandatory
                    if 'warning' in level.lower() or 'attention' in level.lower():
                        level = CheckerMessages.WARNING
                    else:
                        level = CheckerMessages.ERROR
                    # make relative path absolute
                    path = '-'
                    if filename:
                        path = os.path.abspath(os.path.join(os.path.expanduser(working_dir), filename))
                    if use_tuples:
                        msg = (message, level, line_nbr, 0, None, None, path)
                    else:
                        msg = CheckerMessage(message, level, line_nbr, path=path)
                    issues.append(msg)
                    break
        return issues


class CompilerCheckFailedError(Exception):
    def __init__(self, message, return_code):
        self.message = message
        self.return_code = return_code


class Compiler:
    """
    Base class for implementing a new compiler, provides some helper methods to run commands in a subprocess (setup
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
    _CRASH_CODE = 139

    #: associated mimetype
    mimetypes = []

    #: type name of the compiler
    type_name = ''

    def __init__(self, config, working_dir=os.path.expanduser('~'), print_output=True):
        """
        :param config: the associated compiler configuration
        :param working_dir: working directory used to run the compiler process.
        :param print_output: True to print the compiler output to stdout.
        """
        assert isinstance(config, CompilerConfig)
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
        Checks the compiler configuration.

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

        _logger().debug('compiler environment: \n%s' % '\n'.join(env.toStringList()))

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
        def quoted(pgm):
            if ' ' in pgm:
                pgm = '"%s"' % pgm
            return pgm

        def create_process(pgm):
            process = QtCore.QProcess()
            process.setWorkingDirectory(self.working_dir)
            process.setProcessEnvironment(self.get_process_environment())
            process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
            return process

        def get_process_exit_code(process):
            if process.exitStatus() != process.Crashed:
                return process.exitCode()
            else:
                return self._CRASH_CODE

        def get_process_output(process):
            # get compiler output
            raw_output = process.readAllStandardOutput().data()
            try:
                output = raw_output.decode(locale.getpreferredencoding()).replace('\r', '')
            except UnicodeDecodeError:
                # This is a hack to get a meaningful output when compiling a file
                # from UNC path using a batch file on some systems, see
                # https://github.com/OpenCobolIDE/OpenCobolIDE/issues/188
                output = str(raw_output).replace("b'", '')[:-1].replace('\\r\\n', '\n').replace('\\\\', '\\')
            return output

        pgm = quoted(self.config.compiler)
        process = create_process(pgm)
        process.start(pgm, args)
        process.waitForFinished(sys.maxsize)
        exit_code = get_process_exit_code(process)
        output = get_process_output(process)

        if self.print_output:
            print(' '.join([pgm] + args))
            print(output)

        return exit_code, output


def get_configs_for_mimetype(mimetype):
    """
    Gets all the possible compiler configs for the given mimetype.

    I.e. get all gcc configs, all GnuCOBOL configs,...
    """
    from hackedit.api import plugins
    from hackedit.app import settings

    def get_user_configs_for_type_name(type_name):
        ret_val = []
        for config in settings.load_compiler_configurations().values():
            if config.type_name == type_name:
                ret_val.append(config)
        return ret_val

    ret_val = []
    typenames = []
    # gets the list of compiler type names that are available for the mimetype
    for plugin in plugins.get_compiler_plugins():
        compiler = plugin.get_compiler()
        if mimetype in compiler.mimetypes:
            typenames.append(compiler.type_name)
    for type_name in typenames:
        ret_val += plugins.get_compiler_plugin(type_name).get_auto_detected_configs()
        ret_val += get_user_configs_for_type_name(type_name)

    return ret_val


def check_compiler(compiler):
    """
    High level function that checks if a compiler_config works for a the specific compiler klass.

    The result is cached to prevent running checks that have already been tested.
    """
    classname = compiler.__class__.__name__
    json_config = compiler.config.to_json()
    _perform_check(classname, json_config, compiler=compiler)


def _memoize_compiler_config(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer


@_memoize_compiler_config
def _perform_check(classname, json_config, compiler=None):
    if compiler:
        compiler.check_compiler()


def _logger():
    return logging.getLogger(__name__)
