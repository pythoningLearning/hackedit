import os
import sys
import tempfile

import pytest
from hackedit.application import errors

from hackedit.application import interpreters


class PythonSysConfig(interpreters.InterpreterConfig):
    def __init__(self):
        super().__init__()
        self.name = 'Python (System)'
        self.command = 'python'
        self.mimetypes = ['text/x-python']
        self.test_command = ['-c', '"import sys;print(sys.version_info)"']
        self.type_name = 'Python'
        self.environment_variables = {'TEST': '1'}


class PythonConfig(interpreters.InterpreterConfig):
    def __init__(self):
        super().__init__()
        self.name = 'Python'
        self.command = sys.executable
        self.mimetypes = ['text/x-python']
        self.test_command = ['-c', '"import sys;print(sys.version_info)"']
        self.type_name = 'Python'
        self.environment_variables = {'TEST': '1', 'TEST2': '', 'PATH': '/usr'}


class TestInterpreterConfig:
    def test_default(self):
        config = interpreters.InterpreterConfig()

        assert config.name == ''
        assert config.command == ''
        assert config.mimetypes == []
        assert config.command_pattern == '$command $interpreter_arguments $script $script_arguments'
        assert config.test_command == []
        assert config.version_command == ['--version']
        assert config.version_regex == r'(?P<version>\d\.\d\.\d)'
        assert config.type_name == ''

    def test_serialization(self):
        config = PythonConfig()
        config.to_json() == interpreters.InterpreterConfig().from_json(config.to_json())

    def test_copy(self):
        config = PythonConfig()
        cpy = config.copy()
        assert config != cpy
        assert config.to_json() == cpy.to_json()


class TestIntepreter:
    @classmethod
    def setup_class(cls):
        cls.interpreter = interpreters.Interpreter(PythonConfig(), working_directory=tempfile.gettempdir())
        cls.sys_interpreter = interpreters.Interpreter(PythonSysConfig(), working_directory=tempfile.gettempdir())
        cls.broken_interpreter = interpreters.Interpreter(interpreters.InterpreterConfig())

    def test_get_version(self):
        version = interpreters.get_interpreter_version(self.interpreter, include_all=True)
        expected_short_version = '.'.join([str(n) for n in sys.version_info[:3]])
        expected_long_version = 'Python %s\n' % expected_short_version
        assert len(version.splitlines()) == 1
        assert version == expected_long_version
        version = interpreters.get_interpreter_version(self.interpreter, include_all=False)
        print(version)
        assert len(version.splitlines()) == 1
        assert version == expected_short_version

        assert self.broken_interpreter.get_version() == 'Interpreter not found'
        self.broken_interpreter.config.command = sys.executable
        self.broken_interpreter.config.version_regex = r'\d\.\d\.\d'
        assert self.broken_interpreter.get_version().startswith('Python')

    def test_get_full_path(self):
        assert self.interpreter.get_full_path() == os.path.realpath(sys.executable)
        assert not os.path.exists(self.sys_interpreter.config.command)
        assert os.path.exists(self.sys_interpreter.get_full_path())

    def test_check(self):
        interpreters.check_interpreter(self.interpreter)
        interpreters.check_interpreter(self.sys_interpreter)

    def test_check_broken(self):
        self.broken_interpreter.config.command = ''
        self.broken_interpreter.config.command_pattern = ''
        with pytest.raises(errors.InterpreterCheckFailed):
            interpreters.check_interpreter(self.broken_interpreter)
        self.broken_interpreter.config.command = sys.executable
        with pytest.raises(errors.InterpreterCheckFailed):
            interpreters.check_interpreter(self.broken_interpreter)
        self.broken_interpreter.config.mimetypes = ['text/x-python']
        with pytest.raises(errors.InterpreterCheckFailed):
            interpreters.check_interpreter(self.broken_interpreter)
        self.broken_interpreter.config.command_pattern = '$command $interpreter_arguments $script $script_arguments'
        with pytest.raises(errors.InterpreterCheckFailed):
            interpreters.check_interpreter(self.broken_interpreter)
        self.broken_interpreter.config.test_command = ['-c', '"import sys;print(sys.version_info)"']
        interpreters.check_interpreter(self.broken_interpreter)

    def test_make_command(self):
        command = self.interpreter.make_command('file.py', ['--verbose'], ['-Oo'])
        assert command == [self.interpreter.config.command, '-Oo', 'file.py', '--verbose']
        command = self.sys_interpreter.make_command('file.py', ['--verbose'], ['-Oo'])
        assert command == ['python', '-Oo', 'file.py', '--verbose']


class TestPackageManager:
    @classmethod
    def setup_class(cls):
        cls.package_manager = interpreters.PackageManager(PythonConfig())

    def test_constructor(self):
        assert isinstance(self.package_manager.config, PythonConfig)
        assert self.package_manager.last_command == ''

    def test_run_command(self):
        ret, output = self.package_manager._run_command('pip', ['--version'])
        assert ret == 0
        assert 'pip' in output
        assert self.package_manager.last_command == 'pip --version'

    def test_get_installed_packages(self):
        with pytest.raises(NotImplementedError):
            self.package_manager.get_installed_packages()

    def test_install_packages(self):
        with pytest.raises(NotImplementedError):
            self.package_manager.install_packages(['hackedit', 'hackedit-python'])

    def test_uninstall_packages(self):
        with pytest.raises(NotImplementedError):
            self.package_manager.uninstall_packages(['hackedit', 'hackedit-python'])

    def test_update_packages(self):
        with pytest.raises(NotImplementedError):
            self.package_manager.update_packages(['hackedit', 'hackedit-python'])


def test_package():
    package = interpreters.Package()
    package.name = 'hackedit'
    package.current_version = '1.0a2'
    package.latest_version = '1.0a3'
    assert package.outdated is True
