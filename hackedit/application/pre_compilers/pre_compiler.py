import logging
import mimetypes
import os
import re
import tempfile

from hackedit.application.errors import PreCompilerCheckFailed
from hackedit.application.utils import BlockingProcess, CommandBuilder, is_outdated


def _logger():
    return logging.getLogger(__name__)


class PreCompiler:
    """
    Pre-compiles a source file of one type into a source file of another type.

    The entire pre-compile process is driven by the precompiler config.
    """
    def __init__(self, config, working_dir=os.path.expanduser('~'), print_output=True):
        """
        :type config: PreCompilerConfig
        """
        self.print_output = print_output
        self.working_dir = working_dir
        self.config = config

    def get_output_file_name(self, input_file_path):
        """
        Gets the output filename for the specified input input_file_path.
        """
        input_file_name = os.path.splitext(os.path.split(input_file_path)[1])[0]
        command_builder = CommandBuilder(self.config.output_pattern, {
            'input_file_name': input_file_name,
            })
        return command_builder.as_string()

    def get_output_path(self, input_file_path):
        file_name = self.get_output_file_name(input_file_path)
        return os.path.join(self.working_dir, file_name)

    def get_version(self, include_all=False):
        """
        Gets the precompiler version using config.version_command_args and config.version_regex
        """
        def get_version_number(text):
            for l in text.splitlines():
                prog = re.compile(self.config.version_regex)
                m = prog.match(l)
                for m in prog.finditer(l):
                    if m:
                        try:
                            return m.group('version')
                        except IndexError:
                            _logger().warn('matched regex does not contain a capute groupe named "version"')
                            continue
            return text.splitlines()[0]

        _logger().info('getting pre-compiler version: %s', ' '.join(self.config.version_command_args))
        ret_val = _('version not found')
        exists = os.path.exists(self.config.path)
        if exists and self.config.version_command_args:
            status, output = self._run_command(self.config.version_command_args)
            if status == 0 and output:
                ret_val = output if include_all else get_version_number(output)
        elif not exists:
            ret_val = _('PreCompiler not found')
        _logger().info('pre-compiler version: %s', ret_val)
        return ret_val

    def pre_compile_file(self, file):
        """
        Pre-compile the specified file.

        The command is built using the config.command_pattern.
        """
        output_path = self.get_output_file_name(file)
        command = self._make_command(file, output_path)
        if not self._is_outdated(file, output_path):
            if self.print_output:
                print(command.as_string())
                print('pre-compilation skipped, up to date')
            return 0, 'pre-compilation skipped, up to date'
        return self._run_command(command.as_list())

    def check_pre_compiler(self):
        """
        Checks if pre-compiler works.
        """
        def rm_file(path):
            path = resolve_path(path)
            if os.path.exists(path):
                try:
                    os.remove(resolve_path(path))
                except OSError:
                    return False
            return True

        def resolve_path(path):
            return os.path.join(self.working_dir, path)

        def create_test_file():
            mtype = self.config.mimetypes[0]
            file_name = 'test' + mimetypes.guess_extension(mtype)
            path = resolve_path(file_name)
            rm_file(path)
            with open(path, 'w') as f:
                f.write(self.config.test_file_content)
            return file_name

        def perform_check():
            self.working_dir = tempfile.gettempdir()
            input_path = create_test_file()
            output_path = self.get_output_file_name(input_path)
            abs_output_path = resolve_path(output_path)
            if not rm_file(output_path):  # pragma: no cover
                raise PreCompilerCheckFailed(
                    _('Failed to remove %r before checking if pre-compilation works.\n'
                      'Please remove this file before attempting a new pre-compilation check!') %
                    abs_output_path, -1, error_level=PreCompilerCheckFailed.WARNING)
            exit_code, output = self.pre_compile_file(input_path)
            if exit_code != 0 or not os.path.exists(abs_output_path):
                raise PreCompilerCheckFailed(output, exit_code)
            with open(abs_output_path) as fout:
                content = fout.read()
            if not content:
                raise PreCompilerCheckFailed(_('PreCompiler output file is empty. This may indicate a configuration '
                                               'issue.\n\nTest Output:\n%r') % output, exit_code)
            # check succeeded, clean up time
            rm_file(input_path)
            rm_file(output_path)

        _logger().info('checking pre-compiler config %r: %s', self.config.name, self.config.to_json())
        if not os.path.exists(self.config.path):
            raise PreCompilerCheckFailed(_('PreCompiler path does not exists'), -1)
        if not self.config.mimetypes:
            raise PreCompilerCheckFailed(_('There is no associated mime types'), -1)
        if not self.config.output_pattern:
            raise PreCompilerCheckFailed(_('There is no output pattern'), -1)
        if not self.config.command_pattern:
            raise PreCompilerCheckFailed(_('There is no command pattern'), -1)
        if self.config.test_file_content:
            try:
                perform_check()
            except OSError as e:
                raise PreCompilerCheckFailed(_('An unexpected error occured: %s') % e, -1)
            else:
                _logger().info('pre-compiler check succeeded')
        else:
            raise PreCompilerCheckFailed(_(
                "Cannot perform pre-compiler check because we don't know how to create a validation test for this "
                'type of pre-compiler.\n'
                'The configuration seems correct but the pre-compiler might not work...'),
                0, error_level=PreCompilerCheckFailed.WARNING)

    def _is_outdated(self, source, destination):
        return is_outdated(source, destination, working_dir=self.working_dir)

    def _make_command(self, input_path, output_path):
        options = {
            'input_file': input_path,
            'input_file_name': os.path.splitext(input_path)[0],
            'output_file': output_path,
            'output_file_name': os.path.splitext(output_path)[0],
            'flags': self.config.flags
        }
        builder = CommandBuilder(self.config.command_pattern, options)
        return builder

    def _run_command(self, args):
        _logger().debug('pre-compiler command: %s', ' '.join([self.config.path] + args))
        process = BlockingProcess(working_dir=self.working_dir, print_output=self.print_output)
        exit_code, output = process.run(self.config.path, args)
        _logger().debug('exit code: %d', exit_code)
        _logger().debug('output:\n%s', output)
        return exit_code, output
