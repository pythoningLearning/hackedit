import pytest
from hackedit.application.utilities.command_builder import CommandBuilder
from hackedit.application.errors import CommandBuildFailedError


class TestCommandBuilder:
    def test_simple_command(self):
        options_dict = {
            'output_file_name': 'bin/test',
            'input_file_name': 'test.cbl'
        }
        pattern = '-o $output_file_name -i $input_file_name'
        builder = CommandBuilder(pattern, options_dict)
        assert builder.as_list() == ['-o', 'bin/test', '-i', 'test.cbl']
        assert builder.as_string() == '-o bin/test -i test.cbl'

    def test_similar_options(self):
        options_dict = {
            'output_file': 'bin/test.py',
            'output_file_name': 'bin/test',
            'input_file': 'test.cbl',
            'input_file_name': 'test'
        }
        pattern = '-o $output_file_name.cob -i $input_file_name.scb'
        builder = CommandBuilder(pattern, options_dict)
        print(builder.as_list())
        assert builder.as_list() == ['-o', 'bin/test.cob', '-i', 'test.scb']
        assert builder.as_string() == '-o bin/test.cob -i test.scb'

    def test_command_with_non_string_args(self):
        options_dict = {
            'output': 'bin/test',
            'inputs': ['test.cbl', 'hello.cbl'],
            'opt_level': 2
        }
        pattern = '-O$opt_level -o $output -i $inputs '
        builder = CommandBuilder(pattern, options_dict)
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
        builder = CommandBuilder(pattern, options_dict)
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
        with pytest.raises(CommandBuildFailedError):
            CommandBuilder(pattern, options_dict).as_list()
        with pytest.raises(CommandBuildFailedError):
            CommandBuilder(pattern, options_dict).as_string()
