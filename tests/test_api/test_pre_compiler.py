import os
import sys
import tempfile

import pytest
from hackedit import containers
from hackedit.api import pre_compilers
from hackedit.api.errors import PreCompilerCheckFailed

containers.Services.mime_types().add_mimetype_extension('text/x-precompiler-test', '*.pye')

echo_pre_compiler = os.path.join(os.path.dirname(__file__), 'echo_pre_compiler.py')
broken_echo_pre_compiler = os.path.join(os.path.dirname(__file__), 'broken_echo_pre_compiler.py')


class EchoPrecompilerConfig(pre_compilers.PreCompilerConfig):
    def __init__(self):
        super().__init__()
        self.name = 'Echo'
        self.command_pattern = '%s $flags -o $output_file -i $input_file' % echo_pre_compiler
        self.version_command_args = [echo_pre_compiler, '--version']
        self.version_regex = r'.*(?P<version>\d\.\d\.\d).*'
        self.output_pattern = '$input_file_name.py'
        self.path = sys.executable
        self.mimetypes = ['text/x-precompiler-test']
        with open(__file__) as ftest:
            self.test_file_content = ftest.read()
        self.type_name = 'Echo'


class TestPreCompilerConfig:
    def test_default(self):
        config = pre_compilers.PreCompilerConfig()

        assert config.name == ''
        assert config.path == ''
        assert config.mimetypes == []
        assert config.flags == []
        assert config.output_pattern == ''
        assert config.command_pattern == ''
        assert config.test_file_content == ''
        assert config.version_command_args == []
        assert config.version_regex == r'(?P<version>\d\.\d\.\d)'
        assert config.type_name == ''

    def test_serialization(self):
        config = EchoPrecompilerConfig()
        config.to_json() == pre_compilers.PreCompilerConfig().from_json(config.to_json())

    def test_copy(self):
        config = EchoPrecompilerConfig()
        cpy = config.copy()
        assert config != cpy
        assert config.to_json() == cpy.to_json()


class TestPreCompiler:
    @classmethod
    def setup_class(cls):
        cls.precompiler = pre_compilers.PreCompiler(EchoPrecompilerConfig(), working_dir=tempfile.gettempdir())
        cls.broken_precompiler = pre_compilers.PreCompiler(pre_compilers.PreCompilerConfig())

    def test_get_version(self):
        version = pre_compilers.get_pre_compiler_version(self.precompiler, include_all=True)
        assert len(version.splitlines()) == 2
        version = pre_compilers.get_pre_compiler_version(self.precompiler, include_all=False)
        print(version)
        assert len(version.splitlines()) == 1
        assert version == '1.0.0'

        assert self.broken_precompiler.get_version() == 'PreCompiler not found'

        test_precompiler = pre_compilers.PreCompiler(EchoPrecompilerConfig())
        test_precompiler.config.path = sys.executable
        test_precompiler.config.version_command_args = ['--version']
        test_precompiler.config.version_regex = ''
        assert test_precompiler.get_version()

    def test_check_ok(self):
        pre_compilers.check_pre_compiler(self.precompiler)

    def test_check_broken(self, mock):
        self.broken_precompiler.test_file_content = None
        with pytest.raises(PreCompilerCheckFailed):
            pre_compilers.check_pre_compiler(self.broken_precompiler)
        self.broken_precompiler.config.path = echo_pre_compiler
        with pytest.raises(PreCompilerCheckFailed):
            pre_compilers.check_pre_compiler(self.broken_precompiler)
        self.broken_precompiler.config.mimetypes = ['test/x-python']
        with pytest.raises(PreCompilerCheckFailed):
            pre_compilers.check_pre_compiler(self.broken_precompiler)
        self.broken_precompiler.config.output_pattern = 'file.egg'
        with pytest.raises(PreCompilerCheckFailed):
            pre_compilers.check_pre_compiler(self.broken_precompiler)
        self.broken_precompiler.config.command_pattern = 'qziodjqozijd'
        with pytest.raises(PreCompilerCheckFailed):
            pre_compilers.check_pre_compiler(self.broken_precompiler)
        self.broken_precompiler.config.mimetypes = ['text/x-python']
        self.broken_precompiler.config.path = sys.executable
        self.broken_precompiler.config.test_file_content = 'qziodjqozijd'
        with pytest.raises(PreCompilerCheckFailed):
            pre_compilers.check_pre_compiler(self.broken_precompiler)
        # emtpy result
        self.broken_precompiler.config.command_pattern = '%s $flags -o $output_file -i $input_file' % \
                                                         broken_echo_pre_compiler
        self.broken_precompiler.config.path = sys.executable
        with pytest.raises(PreCompilerCheckFailed):
            pre_compilers.check_pre_compiler(self.broken_precompiler)

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


# todo
# @pytest.mark.skipif(sys.platform == 'win32', reason='No precompiler on Windows yet')
# def test_get_configs_for_mimetype():
#     pytest_hackedit.app()
#     plugin = plugins.get_pre_compiler_plugin_by_typename('SQL COBOL - dbpre')
#     config = plugin.create_new_configuration('name', 'path', extra_options=('obj', 'copyboks'))
#     settings.save_pre_compiler_configurations({'test': config})
#     mtype_cfgs = pre_compilers.get_configs_for_mimetype(config.mimetypes[0])
#     assert mtype_cfgs[0].to_json() == config.to_json()
