import os
import sys
import tempfile

import pytest

from hackedit.api import interpreter


class PythonSysConfig(interpreter.InterpreterConfig):
    def __init__(self):
        super().__init__()
        self.name = 'Python (System)'
        self.command = 'python3'
        self.mimetypes = ['text/x-python']
        self.test_command = ['-c', '"import sys;print(sys.version_info)"']
        self.type_name = 'Python'


class PythonConfig(interpreter.InterpreterConfig):
    def __init__(self):
        super().__init__()
        self.name = 'Python'
        self.command = sys.executable
        self.mimetypes = ['text/x-python']
        self.test_command = ['-c', '"import sys;print(sys.version_info)"']
        self.type_name = 'Python'


class TestInterpreterConfig:
    def test_default(self):
        config = interpreter.InterpreterConfig()

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
        config.to_json() == interpreter.InterpreterConfig().from_json(config.to_json())

    def test_copy(self):
        config = PythonConfig()
        cpy = config.copy()
        assert config != cpy
        assert config.to_json() == cpy.to_json()


class TestIntepreter:
    @classmethod
    def setup_class(cls):
        cls.interpreter = interpreter.Interpreter(PythonConfig(), working_directory=tempfile.gettempdir())
        cls.sys_interpreter = interpreter.Interpreter(PythonSysConfig(), working_directory=tempfile.gettempdir())
        cls.broken_interpreter = interpreter.Interpreter(interpreter.InterpreterConfig())

    def test_get_version(self):
        version = interpreter.get_version(self.interpreter, include_all=True)
        expected_short_version = '.'.join([str(n) for n in sys.version_info[:3]])
        expected_long_version = 'Python %s\n' % expected_short_version
        assert len(version.splitlines()) == 1
        assert version == expected_long_version
        version = interpreter.get_version(self.interpreter, include_all=False)
        print(version)
        assert len(version.splitlines()) == 1
        assert version == expected_short_version

        assert self.broken_interpreter.get_version() == 'Interpreter not found'

    def test_get_full_path(self):
        assert self.interpreter.get_full_path() == os.path.realpath(sys.executable)
        assert not os.path.exists(self.sys_interpreter.config.command)
        assert os.path.exists(self.sys_interpreter.get_full_path())

    def test_check(self):
        interpreter.check(self.interpreter)
        interpreter.check(self.sys_interpreter)
        with pytest.raises(interpreter.InterpreterCheckFailed):
            interpreter.check(self.broken_interpreter)

    def test_make_command(self):
        command = self.interpreter.make_command('file.py', ['--verbose'], ['-Oo'])
        assert command == [self.interpreter.config.command, '-Oo', 'file.py', '--verbose']
        command = self.sys_interpreter.make_command('file.py', ['--verbose'], ['-Oo'])
        assert command == ['python3', '-Oo', 'file.py', '--verbose']
