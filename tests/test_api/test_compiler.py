import time
import sys
import os
import re

import pytest

import pytest_hackedit
from hackedit.api import compiler


def create_test_config():
    cfg = compiler.CompilerConfiguration()
    cfg.name = 'Test'
    cfg.compiler = __file__
    cfg.compiler_flags = ['-debug']
    cfg.compiler_include_path = ['/usr/share/include']
    cfg.compiler_library_path = ['/usr/lib']
    cfg.compiler_libraries = ['QtCore']
    cfg.compiler_environment_variables = {'COB_CONFIG_DIR': '/usr/share/gnu-cobol/config/'}
    cfg.vcvarsall = ''
    cfg.vcvarsall_arch = 'x86'
    cfg.compiler_type_name = 'GnuCOBOL'
    cfg.custom_options = {}

    return cfg


class TestCompilerConfig:
    def test_default(self):
        cfg = compiler.CompilerConfiguration()
        assert cfg.name == ''
        assert cfg.compiler == ''
        assert cfg.compiler_flags == []
        assert cfg.compiler_include_path == []
        assert cfg.compiler_library_path == []
        assert cfg.compiler_libraries == []
        assert cfg.compiler_environment_variables == {}
        assert cfg.vcvarsall == ''
        assert cfg.vcvarsall_arch == 'x86'
        assert cfg.compiler_type_name == ''
        assert cfg.custom_options == {}

    def test_custom_config(self):
        cfg = create_test_config()
        assert cfg.name == 'Test'
        assert cfg.compiler == __file__
        assert cfg.compiler_flags == ['-debug']
        assert cfg.compiler_include_path == ['/usr/share/include']
        assert cfg.compiler_library_path == ['/usr/lib']
        assert cfg.compiler_libraries == ['QtCore']
        assert cfg.compiler_environment_variables == {'COB_CONFIG_DIR': '/usr/share/gnu-cobol/config/'}
        assert cfg.vcvarsall == ''
        assert cfg.vcvarsall_arch == 'x86'
        assert cfg.compiler_type_name == 'GnuCOBOL'
        assert cfg.custom_options == {}

    def test_serialization(self):
        cfg = create_test_config()
        assert cfg.to_json() == compiler.CompilerConfiguration().from_json(cfg.to_json()).to_json()

    def test_copy(self):
        cfg = create_test_config()
        cpy = cfg.copy()
        assert cfg != cpy
        assert cfg.to_json() == cpy.to_json()


def test_compiler_config_widget(qtbot):
    widget = compiler.CompilerConfigurationWidget()
    qtbot.addWidget(widget)
    cfg = create_test_config()
    widget.set_config(cfg)
    assert widget.is_dirty() is False
    assert widget.get_config().to_json() == cfg.to_json()


def test_generic_compiler_config_widget(qtbot):
    """
    :type qtbot: pytestqt.qtbot.QtBot
    """
    widget = compiler.GenericCompilerCongigWidget()
    widget.show()
    qtbot.addWidget(widget)
    cfg = create_test_config()
    widget.set_config(cfg)

    assert widget.is_dirty() is False
    assert widget.get_config().to_json() == cfg.to_json()

    assert widget.ui.list_include_paths.count() == 1
    widget.ui.list_include_paths.addItem('../include')
    assert widget.ui.list_include_paths.count() == 2
    widget.ui.list_lib_paths.addItem('../libs')
    widget.ui.edit_flags.setText(widget.ui.edit_flags.text() + ' -Wall --verbose ')
    widget.ui.edit_libs.setText(widget.ui.edit_libs.text() + ' QtWidgets QtGui    ')

    assert widget.is_dirty() is True
    assert widget.get_config().to_json() != cfg.to_json()
    updated_cfg = widget.get_config()
    assert updated_cfg.compiler_include_path == ['/usr/share/include', '../include']
    assert updated_cfg.compiler_library_path == ['/usr/lib', '../libs']
    assert updated_cfg.compiler_flags == ['-debug', '-Wall', '--verbose']
    assert updated_cfg.compiler_libraries == ['QtCore', 'QtWidgets', 'QtGui']


def test_parser_gcc():
    gcc_sample_output = '''test.cbl: 1: Error: PROGRAM-ID header missing
test.cbl: 1: Error: PROCEDURE DIVISION header missing
test.cbl: 1: Error: syntax error, unexpected Literal
test.cbl: 2: Error: syntax error, unexpected Identifier
In file included from /usr/include/stdio.h:27:0,
                 from /tmp/cob17702_0.c:8:

/usr/include/features.h:331:4: attention : #warning _FORTIFY_SOURCE requires compiling with optimization (-O) [-Wcpp]
 #  warning _FORTIFY_SOURCE requires compiling with optimization (-O)
    ^
'''
    from pyqode.core.modes import CheckerMessage, CheckerMessages

    parser = compiler.CompilerOutputParser()
    parser.patterns.insert(0,  re.compile('.*'))  # invalid regex because it miss the msg capture group

    messages = parser.parse(gcc_sample_output, '~/Documents', use_tuples=True)
    assert len(messages) == 5
    assert isinstance(messages[0], tuple)
    messages = parser.parse(gcc_sample_output, '~/Documents', use_tuples=False)
    assert len(messages) == 5
    assert isinstance(messages[0], CheckerMessage)

    assert messages[0].line == 0
    assert messages[3].line == 1
    assert messages[0].path == os.path.normpath(os.path.expanduser('~/Documents/test.cbl'))
    assert messages[0].status == CheckerMessages.ERROR
    assert messages[-1].status == CheckerMessages.WARNING


def test_compiler_check_failed_error():
    err = compiler.CompilerCheckFailedError('blabla', -1)
    assert err.message == 'blabla'
    assert err.return_code == -1


wd = os.path.dirname(__file__)
cfg = create_test_config()
my_compiler = compiler.Compiler(cfg, working_dir=wd)


class TestCompilerBaseClass:
    def test_compile(self):
        with pytest.raises(NotImplementedError):
            my_compiler.compile_files(['test.cbl'], 'bin', 'test', target_type=compiler.TargetType.SHARED_LIBRARY)

    def test_constructor(self):
        c = compiler.Compiler(compiler.CompilerConfiguration())
        assert c.working_dir == os.path.expanduser('~')
        assert c.print_output is True

        c = compiler.Compiler(compiler.CompilerConfiguration(), working_dir=wd)
        assert c.working_dir == wd
        assert c.print_output is True

        c = compiler.Compiler(compiler.CompilerConfiguration(), working_dir=wd, print_output=False)
        assert c.working_dir == wd
        assert c.print_output is False

    def test_get_full_compiler_path(self):
        # using an absolute path is the easiest case
        my_compiler.get_full_compiler_path() == __file__

        # resolve full name using PATH
        cfg.compiler = 'python'
        assert os.path.exists(my_compiler.get_full_compiler_path())

        # should return an empty string if program path cannot be resolved using PATH
        cfg.compiler = 'foo'
        assert my_compiler.get_full_compiler_path() == ''

        cfg.compiler == __file__

    def test_make_destination_folder(self):
        # absolute dest folder
        path = os.path.join(wd, 'bin1')
        assert os.path.exists(path) is False
        my_compiler.make_destination_folder(path)
        assert os.path.exists(path) is True
        os.rmdir(path)

        # special case where user must be expanded
        path = '~/bin1'
        expanded_path = os.path.expanduser(path)
        assert os.path.exists(path) is False
        my_compiler.make_destination_folder(path)
        assert os.path.exists(expanded_path) is True
        os.rmdir(expanded_path)

        # relative dest folder
        name = 'bin1'
        path = os.path.join(wd, name)
        assert os.path.exists(path) is False
        my_compiler.make_destination_folder(name)
        assert os.path.exists(path) is True
        os.rmdir(path)

    def test_is_outdated(self):
        source = 'test.cbl'
        dest = 'test.exe'
        source_path = os.path.join(wd, source)
        destination_path = os.path.join(wd, dest)
        with open(source_path, 'w'):
            pass
        time.sleep(0.1)
        with open(destination_path, 'w'):
            pass

        outdated = my_compiler.is_outdated(source_path, destination_path)
        assert outdated is False
        outdated = my_compiler.is_outdated(destination_path, source_path)
        assert outdated is True

        # this should work with relative paths as well
        outdated = my_compiler.is_outdated(source, dest)
        assert outdated is False
        outdated = my_compiler.is_outdated(dest, source)
        assert outdated is True

        # check corner cases (things that do not exist or strange args)
        outdated = my_compiler.is_outdated('/foo/bar', '')
        assert outdated is True
        outdated = my_compiler.is_outdated('', '')
        assert outdated is False
        with pytest.raises(ValueError):
            outdated = my_compiler.is_outdated(None, None)
        with pytest.raises(ValueError):
            outdated = my_compiler.is_outdated(4, 5.2)

        os.remove(source_path)
        os.remove(destination_path)

    def test_setup_environment(self):
        cfg.compiler = __file__
        cfg.compiler_environment_variables['PATH'] = wd
        cfg.compiler_environment_variables['EMPTY'] = ''
        env = my_compiler.setup_environment()
        assert env.contains('PATH')
        assert env.value('PATH').startswith(wd)

    def test_run_compiler_command(self):
        my_compiler.config.compiler = 'python'
        ret, output = my_compiler.run_compiler_command(['-c', '"import sys; print(sys.executable)"'])
        assert ret == 0
        assert output != ''
        with pytest.raises(ValueError):
            my_compiler.config.compiler = ''
            my_compiler.run_compiler_command(['-c', '"import sys; print(sys.executable)"'])
        with pytest.raises(ValueError):
            my_compiler.config.compiler = 'python'
            my_compiler.run_compiler_command([])

        # cover the case where "" must be appended to the program name but hard to test
        my_compiler.config.compiler = 'py thon'
        ret, output = my_compiler.run_compiler_command(['--version'])


def test_get_configurations_by_mtype():
    try:
        import hackedit_cobol
    except ImportError:
        return
    else:
        assert hackedit_cobol
        pytest_hackedit.app()
        configs = compiler.get_configurations('text/x-cobol')
        assert len(configs) >= 1
