import pytest
from PyQt5 import QtWidgets

from hackedit.api import utils
from hackedit.app import mime_types, settings


def test_add_mimetype_extension():
    settings.load()
    settings._SETTINGS.clear()
    mtype = 'text/x-own'
    ext = '.own'
    assert ext not in mime_types.get_extensions(mtype)
    utils.add_mimetype_extension(mtype, ext)
    assert ext in mime_types.get_extensions(mtype)


def test_get_mimetype_filter():
    ret = utils.get_mimetype_filter('text/x-python')
    assert 'text/x-python (*.py *.pyw ' in ret


def test_get_ignored_patterns():
    patterns = utils.get_ignored_patterns()
    assert len(patterns) > 1


def test_get_cmd_open_folder_in_terminal():
    cmd = utils.get_cmd_open_folder_in_terminal()
    assert cmd != ''


def test_get_cmd_run_command_in_terminal():
    cmd = utils.get_cmd_run_command_in_terminal()
    assert cmd != ''


def test_get_cmd_open_in_explorer():
    cmd = utils.get_cmd_open_in_explorer()
    assert cmd != ''


def test_get_color_scheme():
    scheme = utils.color_scheme()
    assert isinstance(scheme, str)
    assert scheme in ['aube', 'crepuscule']


def test_is_dark_color_scheme():
    assert utils.is_dark_color_scheme('aube') is False
    assert utils.is_dark_color_scheme('crepuscule') is True


def test_editor_font():
    assert utils.editor_font() == 'Hack'


def test_editor_font_size():
    assert utils.editor_font_size() == 10


toggled = False


def on_toggle():
    global toggled
    toggled = True


def test_block_signal(qtbot):
    checkbox = QtWidgets.QCheckBox()
    checkbox.toggled.connect(on_toggle)
    with utils.block_signals(checkbox):
        checkbox.toggle()
    assert toggled is False
    checkbox.toggle()
    assert toggled is True


def test_is_ignored_path():
    assert utils.is_ignored_path('file.pyc') is True
    assert utils.is_ignored_path('file.py') is False


class TestCommandBuilder:
    def test_command_builder_get_pattern_option(self):
        assert utils.CommandBuilder.get_pattern_option('-I$includes', '$includes') == '-I'
        assert utils.CommandBuilder.get_pattern_option('-I $includes', '$includes') == ''

    def test_simple_command(self):
        options_dict = {
            'output_file_name': 'bin/test',
            'input_file_name': 'test.cbl'
        }
        pattern = '-o $output_file_name -i $input_file_name'
        builder = utils.CommandBuilder(pattern, options_dict)
        assert builder.as_list() == ['-o', 'bin/test', '-i', 'test.cbl']
        assert builder.as_string() == '-o bin/test -i test.cbl'

    def test_command_with_non_string_args(self):
        options_dict = {
            'output': 'bin/test',
            'inputs': ['test.cbl', 'hello.cbl'],
            'opt_level': 2
        }
        pattern = '-O$opt_level -o $output -i $inputs '
        builder = utils.CommandBuilder(pattern, options_dict)
        assert builder.as_list() == ['-O2', '-o', 'bin/test', '-i', 'test.cbl', 'hello.cbl']
        assert builder.as_string() == '-O2 -o bin/test -i test.cbl hello.cbl'

    def test_repeat_option(self):
        # if a pattern is not separated by a whitepsace from the preceding option and the option value is a list,
        # the option must be repeated for each value in the list (we check this with 'includes')
        # if the option value list is empty the option must not appear in the result (we check this with 'libraries')
        pattern = '-x -I$includes -l$libraries -o $output -i $inputs '
        options_dict = {
            'output': 'bin/test',
            'inputs': ['test.cbl', 'hello.cbl'],
            'includes': ['/usr/share/include', '/usr/local/share/include'],  # -> -Ivalue -Ivalue
            'libraries': []  # -> must not appear in result
        }
        builder = utils.CommandBuilder(pattern, options_dict)
        assert builder.as_list() == ['-x', '-I/usr/share/include', '-I/usr/local/share/include', '-o', 'bin/test',
                                     '-i', 'test.cbl', 'hello.cbl']
        assert builder.as_string() == '-x -I/usr/share/include -I/usr/local/share/include ' \
            '-o bin/test -i test.cbl hello.cbl'

    def test_build_failure(self):
        # this command should fail to build because not all patterns can be substituted
        pattern = '$flags -o $output_file_name -i $input_file_name'
        options_dict = {
            'output_file_name': 'bin/test',
            'input_file_name': 'test.cbl'
        }
        with pytest.raises(utils.CommandBuildFailedError):
            utils.CommandBuilder(pattern, options_dict)
