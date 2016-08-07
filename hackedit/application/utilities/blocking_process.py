import locale
import sys

from PyQt5 import QtCore


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
        else:  # pragma: no cover
            return self._CRASH_CODE

    def _read_output(self):
        # get compiler output
        raw_output = self.readAllStandardOutput().data()
        try:
            output = raw_output.decode(locale.getpreferredencoding()).replace('\r', '')
        except UnicodeDecodeError:  # pragma: no cover
            # This is a hack to get a meaningful output when compiling a file
            # from UNC path using a batch file on some systems, see
            # https://github.com/OpenCobolIDE/OpenCobolIDE/issues/188
            output = str(raw_output).replace("b'", '')[:-1].replace('\\r\\n', '\n').replace('\\\\', '\\')
        return output

    def _quoted(self, string):
        if ' ' in string:
            string = '"%s"' % string
        return string