"""
A set of utility functions that plugin would use.
"""
import functools
import sys
import locale
import copy
import json
import os
from fnmatch import fnmatch

from PyQt5 import QtCore, QtWidgets

from hackedit.app import settings, mime_types


def add_mimetype_extension(mimetype, extension):
    """
    Adds an extension to an existing mimetype. If the mimetypes does not
    exists it is automatically added to the mimetypes database.

    :param mimetype: mimetype to modify
    :param extension: extension to add
    :return:
    """
    exts = mime_types.get_extensions(mimetype)
    exts.append(extension)
    exts = list(set(exts))
    mime_types.set_extensions(mimetype, exts)


def remove_mimetype_extension(mimetype, extension):
    exts = mime_types.get_extensions(mimetype)
    try:
        exts.remove(extension)
    except ValueError:
        return
    else:
        exts = list(set(exts))
        print(exts, mimetype)
        mime_types.set_extensions(mimetype, exts)


def get_mimetype_filter(mtype):
    """
    Gets the open file dialog filter for a given mimetype.

    :param mtype: Mime type (e.g. 'text/x-python' or 'text/x-cobol').
    """
    exts = ' '.join(mime_types.get_extensions(mtype))
    return '%s (%s)' % (mtype, exts)


def get_ignored_patterns():
    """
    Gets the list of ignored patterns.

    :return: a list of ignored patterns (fnmatch)
    """
    return settings.ignored_patterns()


def get_cmd_open_folder_in_terminal():
    """
    Returns the command to use to open a folder in a terminal.

    This takes the user's preferences into account.
    """
    return settings.get_cmd_open_folder_in_terminal()


def get_cmd_run_command_in_terminal():
    """
    Returns the command to use to run a file in a terminal

    This takes the user's preferences into account.
    """
    return settings.get_cmd_run_command_in_terminal()


def get_cmd_open_in_explorer():
    """
    Returns the command used to show a file/folder in the file explorer.
    """
    return settings.file_manager_cmd()


def color_scheme():
    """
    Returns the color scheme chosen by the usser
    """
    return settings.color_scheme()


def is_dark_color_scheme(scheme):
    """
    Checks if a given color scheme is a dark or not

    :param scheme: color scheme to test

    :return: True if scheme is a dark color scheme.
    """
    return settings.is_dark_color_scheme(scheme=scheme)


def is_dark_theme():
    """
    Checks if the dark theme is ON.

    Dark theme is either set by a stylesheet or by a gtk/kde color scheme.

    This function takes both into account.

    :return: True if the IDE is running in dark mode, False otherwise.
    """
    dark_stylesheet = settings.dark_theme()
    if not dark_stylesheet:
        dark_stylesheet = \
            QtWidgets.qApp.palette().base().color().lightness() < 128
    return dark_stylesheet


def editor_font():
    """
    Returns the editor font chose by the user.
    """
    return settings.editor_font()


def editor_font_size():
    """
    Returns the editor font chose by the user.
    """
    return settings.editor_font_size()


class block_signals:
    """
    Context manager that calls blockSignals on the QObject passed in
    parameters.

    Usage::

        with block_signals(qobject):
            pass  # do some stuff

    This is equivalent to::

        qobject.blockSignals(True)
        pass  # do some stuff
        qobject.blockSignals(False)

    """
    def __init__(self, qobject):
        self.qobject = qobject

    def __enter__(self):
        self.qobject.blockSignals(True)

    def __exit__(self, *args, **kwargs):
        self.qobject.blockSignals(False)


def is_ignored_path(path, ignore_patterns=None):
    """
    Utility function that checks if a given path should be ignored.

    A path is ignored if it matches one of the ignored_patterns.

    :param path: the path to check.
    :param ignore_patterns: The ignore patters to respect.
        If none, :func:hackedit.api.settings.ignore_patterns() is used instead.
    :returns: True if the path is in an directory that must be ignored
        or if the file name matches an ignore pattern, otherwise False.
    """
    if ignore_patterns is None:
        ignore_patterns = get_ignored_patterns()

    def ignore(name):
        for ptrn in ignore_patterns:
            if fnmatch(name, ptrn):
                return True

    for part in os.path.normpath(path).split(os.path.sep):
        if part and ignore(part):
            return True
    return False


def add_environment_var_to_table(table):
    assert isinstance(table, QtWidgets.QTableWidget)
    key, ok = QtWidgets.QInputDialog.getText(table, "Add environment variable", "Key:")
    if not ok:
        return
    value, ok = QtWidgets.QInputDialog.getText(table, "Add environment variable", "Value:")
    if not ok:
        return
    index = table.rowCount()
    table.insertRow(index)
    key_item = QtWidgets.QTableWidgetItem()
    key_item.setText(key)
    value_item = QtWidgets.QTableWidgetItem()
    value_item.setText(value)
    table.setItem(index, 0, key_item)
    table.setItem(index, 1, value_item)
    table.selectRow(index)


def remove_selected_environment_var_from_table(table):
    assert isinstance(table, QtWidgets.QTableWidget)
    row = table.currentRow()
    if row == -1:
        return
    table.removeRow(row)
    row -= 1
    if row != -1:
        table.selectRow(row)


class JSonisable:
    def to_json(self):
        """
        Converts the configuration to a json object
        """
        return json.dumps(self.__dict__, sort_keys=True)

    def from_json(self, json_content):
        """
        Import config values from a json object.
        """
        content = json.loads(json_content)
        for k, v in content.items():
            setattr(self, k, v)
        return self


class Copyable:
    def copy(self):
        """
        Returns a copy of the configuration that can be changed without altering this instance.
        """
        return copy.deepcopy(self)


class BlockingProcess(QtCore.QProcess):
    """
    Extends QProcess to easily run command in a subprocess.

    .. note:: the subprocess execution is blocking
    """
    _CRASH_CODE = 139

    def __init__(self, working_dir=None,  environment=None, print_output=True):
        super().__init__()
        if working_dir:
            self.setWorkingDirectory(working_dir)
        if environment:
            self.setProcessEnvironment(environment)
        self.setProcessChannelMode(self.MergedChannels)
        self.print_output = print_output

    def run(self, program, arguments):
        """
        Run a command in a subprocess and returns its return code and output.

        .. note:: The output will be printed to stdout if the ``print_output`` parameter of the constructor has been
            set to True.

        :param args: compiler arguments.
        :returns: (return_code, output)
        :rtype: (int, str)
        """
        if not program:
            raise ValueError('program cannot be empty')

        if not arguments:
            raise ValueError('arguments cannot be empty')

        program = self._quoted(program)
        self.start(program, arguments)
        self.waitForFinished(sys.maxsize)
        exit_code = self._get_exit_code()
        output = self._read_output()

        if self.print_output:
            print(' '.join([program] + arguments))
            print(output)

        if exit_code != 0 and not output and self.error() != self.UnknownError:
            output = self.errorString()
        return exit_code, output

    def _get_exit_code(self):
        if self.exitStatus() != self.Crashed:
            return self.exitCode()
        else:
            return self._CRASH_CODE

    def _read_output(self):
        # get compiler output
        raw_output = self.readAllStandardOutput().data()
        try:
            output = raw_output.decode(locale.getpreferredencoding()).replace('\r', '')
        except UnicodeDecodeError:
            # This is a hack to get a meaningful output when compiling a file
            # from UNC path using a batch file on some systems, see
            # https://github.com/OpenCobolIDE/OpenCobolIDE/issues/188
            output = str(raw_output).replace("b'", '')[:-1].replace('\\r\\n', '\n').replace('\\\\', '\\')
        return output

    def _quoted(self, string):
        if ' ' in string:
            string = '"%s"' % string
        return string


class CommandBuildFailedError(Exception):
    def __init__(self, message):
        self.message = message


class CommandBuilder:
    """
    Build a command based on a pattern and a dict of options.

    The pattern is a list of string with substitutable options: $xyz where xyz is a key of the options_dict.

    Example::

        >>> builder = CommandBuilder('-o $output_file_name -i $input_file_name', {
                'output_file_name': 'bin/test',
                'input_file_name': 'test.cbl'
            })
        >>> builder.as_list()
        ['-o', 'bin/test', '-i', 'test.cbl']
        >>> builder.as_string()
        '-o bin/test -i test.cbl'

    """
    def __init__(self, pattern, options_dict):
        """
        :param pattern: the command pattern string.
        :type pattern: str
        :param options_dict: the options_dict
        :type options_dict: dict
        """
        self._result = None
        self._pattern = pattern
        self._options_dict = options_dict

    def as_string(self):
        """
        Returns the built command as a single string.
        """
        self._build()
        return ' '.join(self.as_list())

    def as_list(self):
        """
        Returns the built command as a list.
        """
        self._build()
        return [t.strip() for t in self._result.strip().split(' ') if t]

    def _build(self):
        if self._result is not None:
            return
        args = []
        for pattern in self._pattern.strip().split(' '):
            if '$' in pattern:
                args.append(self._build_pattern(pattern))
            else:
                args.append(pattern)
        self._result = ' '.join(args)

    def _build_pattern(self, pattern):
        index = pattern.find('$')
        key = pattern[index + 1:]
        option = pattern[:index]
        k = self.find_closest_key(key)
        if k:
            value = self._options_dict[k]
            remaining = key.replace(k, '')
            if option:
                return self._get_value_with_option(option, value, remaining)
            else:
                return self._get_value(value, remaining)
        else:
            raise CommandBuildFailedError(_('Pattern %r not found in options dict') % pattern)

    def find_closest_key(self, key):
        """
        :type key: str
        """
        try:
            key = key[:key.index('.')]
        except ValueError:
            pass
        found = {}
        for k in self._options_dict.keys():
            if k in key:
                found[len(k)] = k
        for klen in sorted(found.keys()):
            if klen >= len(key):
                return found[klen]
        return None

    @staticmethod
    def _get_value(value, remaining):
        if isinstance(value, list):
            return ' '.join([v + remaining for v in value])
        else:
            return str(value) + remaining

    @staticmethod
    def _get_value_with_option(option, value, remaining):
        if isinstance(value, list):
            return ' '.join([option + v + remaining + ' ' for v in value])
        else:
            return option + str(value) + remaining


def is_outdated(source, destination, working_dir=''):
    """
    Checks if the destination is outdated (i.e. the source is newer than the destination).
    """
    try:
        if not os.path.isabs(source):
            source = os.path.join(working_dir, source)
        if not os.path.isabs(destination):
            destination = os.path.join(working_dir, destination)
        try:
            return os.path.getmtime(source) > os.path.getmtime(destination)
        except OSError:
            return True
    except (TypeError, AttributeError):
        raise ValueError('Invalid source and destinations')


class ProgramCheckFailedError(Exception):
    WARNING = 0
    ERROR = 1

    def __init__(self, program, logger, message, return_code=None, error_level=None):
        if error_level is None:
            error_level = self.ERROR
        self.error_level = error_level
        self.message = message
        self.return_code = return_code
        if self.error_level == self.WARNING:
            log_fct = logger().warn
        else:
            log_fct = logger().error
        log_fct('%s check failed: %r' % (program, self.message))


def memoize_args(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            try:
                ret = obj(*args, **kwargs)
            except Exception as e:
                ret = e
            finally:
                cache[args] = ret
        ret = cache[args]
        if isinstance(ret, Exception):
            raise ret
        return ret
    return memoizer
