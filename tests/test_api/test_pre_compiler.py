import os
import pytest
import sys
import argparse
import tempfile
from hackedit.api import pre_compiler


class EchoPrecompilerConfig(pre_compiler.PreCompilerConfig):
    def __init__(self):
        super().__init__()
        self.name = 'Echo'
        self.command_pattern = '%s $flags -o $output_file_name -i $input_file_name' % __file__
        self.version_command_args = [__file__, '--version']
        self.version_regex = r'.*(?P<version>\d\.\d\.\d).*'
        self.output_pattern = '$input_file_name.py'
        self.path = sys.executable
        self.associated_extensions = ['.pye']
        with open(__file__) as ftest:
            self.test_file_content = ftest.read()
        self.type_name = 'Echo'


class TestPreCompilerConfig:
    def test_default(self):
        config = pre_compiler.PreCompilerConfig()

        assert config.name == ''
        assert config.path == ''
        assert config.associated_extensions == []
        assert config.flags == []
        assert config.output_pattern == ''
        assert config.command_pattern == ''
        assert config.command_pattern_editable is False
        assert config.test_file_content == ''
        assert config.version_command_args == []
        assert config.version_regex == r'(?P<version>\d\.\d\.\d)'
        assert config.type_name == ''

    def test_custom(self):
        config = pre_compiler.CustomPreCompilerConfig()

        assert config.name == ''
        assert config.path == ''
        assert config.associated_extensions == []
        assert config.flags == []
        assert config.output_pattern == ''
        assert config.command_pattern == '$flags -o $output_file_name -i $input_file_name'
        assert config.command_pattern_editable is True
        assert config.test_file_content == ''
        assert config.version_command_args == []
        assert config.version_regex == r'(?P<version>\d\.\d\.\d)'
        assert config.type_name == 'Custom'

    def test_serialization(self):
        config = EchoPrecompilerConfig()
        config.to_json() == pre_compiler.PreCompilerConfig().from_json(config.to_json())

    def test_copy(self):
        config = EchoPrecompilerConfig()
        cpy = config.copy()
        assert config != cpy
        assert config.to_json() == cpy.to_json()


class TestPreCompiler:
    @classmethod
    def setup_class(cls):
        cls.precompiler = pre_compiler.PreCompiler(EchoPrecompilerConfig(), working_dir=tempfile.gettempdir())
        cls.broken_precompiler = pre_compiler.PreCompiler(pre_compiler.CustomPreCompilerConfig())

    def test_get_version(self):
        version = pre_compiler.get_version(self.precompiler, include_all=True)
        assert len(version.splitlines()) == 2
        version = pre_compiler.get_version(self.precompiler, include_all=False)
        print(version)
        assert len(version.splitlines()) == 1
        assert version == '1.0.0'

        assert self.broken_precompiler.get_version() == '-'

        test_precompiler = pre_compiler.PreCompiler(pre_compiler.CustomPreCompilerConfig())
        test_precompiler.config.version_command_args = ['--version']
        assert test_precompiler.get_version() == 'PreCompiler not found'

        test_precompiler = pre_compiler.PreCompiler(pre_compiler.CustomPreCompilerConfig())
        test_precompiler.config.path = sys.executable
        test_precompiler.config.version_command_args = ['--version']
        test_precompiler.config.version_regex = ''
        assert test_precompiler.get_version()

    def test_check(self):
        pre_compiler.check_pre_compiler(self.precompiler)
        with pytest.raises(pre_compiler.PreCompilerCheckFailed):
            pre_compiler.check_pre_compiler(self.broken_precompiler)

    def test_get_output_file_name(self):
        assert self.precompiler.get_output_file_name('file.pye') == 'file.py'
        assert self.precompiler.get_output_file_name('/usr/file.pye') == 'file.py'

    def test_get_output_file_path(self):
        abs_output_path = os.path.join(self.precompiler.working_dir, 'file.py')
        assert self.precompiler.get_output_path('file.pye') == abs_output_path
        assert self.precompiler.get_output_path('/usr/file.pye') == abs_output_path

    def test_precompile_file(self):
        self.precompiler.pre_compile_file(__file__)
        output_path = os.path.join(self.precompiler.working_dir, 'test_pre_compiler.py')
        assert os.path.exists(output_path)
        mtime = os.path.getmtime(output_path)
        self.precompiler.pre_compile_file(__file__)
        # ensure we check for mtime in order to avoid useless compilations
        assert mtime == os.path.getmtime(output_path)
        try:
            os.remove(output_path)
        except OSError:
            return


def echo_precompiler():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-file', help='Output file')
    parser.add_argument('-i', '--input-file', help='Input file')
    parser.add_argument('-V', '--version', help='Show version', action='store_true')
    args = parser.parse_args()
    if args.version:
        print('Echo preparser v1.0.0')
        print('Waow, such a great program! ^^')
        sys.exit()
    with open(args.input_file, 'r') as fin, open(args.output_file, 'w') as fout:
        fout.write(fin.read())


if __name__ == '__main__':
    echo_precompiler()
