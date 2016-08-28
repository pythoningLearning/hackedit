import os
import re


class CompilerOutputParser:
    """
    Parses output of compiler commands.

    You can extend the output parser capabilities by using different patterns. We highly suggest that you append
    new patterns to :attr:`CompilerOutputParser.OUTPUT_PATTERNS`.
    """
    # Gcc output pattern
    OUTPUT_PATTERN_GCC = re.compile(
        r'^(?P<filename>[\w\.\-_\s/]*):(?P<line>\s*\d*):(?P<column>\s*\d*)?:?(?P<level>[\w\s]*):(?P<msg>.*)$')

    # MSVC output pattern
    OUTPUT_PATTERN_MSVC = re.compile(
        r'^(?P<filename>[\w\.\-_\s]*)\((?P<line>\s*\d*)\):(?P<level>[\w\s]*):'
        '(?P<msg>.*)$')

    #: Default output patterns.
    OUTPUT_PATTERNS = [OUTPUT_PATTERN_GCC, OUTPUT_PATTERN_MSVC]

    def __init__(self, patterns=None):
        if patterns is None:
            patterns = CompilerOutputParser.OUTPUT_PATTERNS
        self.patterns = patterns

    def parse(self, output, working_dir, use_tuples=False):
        """
        Parses compiler command output.

        :param output: compiler output string
        :param working_dir: working directory of the compiler, used to find the absolute path of relative file paths.
        :param use_tuples: True to return a list of tuple instead of a list of
            :class:`pyqode.core.modes.CheckerMessage`
        :returns: a list of messages.
        """
        from pyqode.core.modes import CheckerMessages
        if not use_tuples:
            from pyqode.core.modes import CheckerMessage
        issues = []
        for line in output.splitlines():
            if not line:
                continue
            for ptrn in self.patterns:
                m = ptrn.match(line)
                if m is not None:
                    try:
                        filename = m.group('filename')
                    except IndexError:
                        filename = ''
                    try:
                        line_nbr = int(m.group('line')) - 1
                    except IndexError:
                        line_nbr = 0
                    try:
                        level = m.group('level')
                    except IndexError:
                        level = 'warning'
                    try:
                        message = m.group('msg')
                    except IndexError:
                        continue  # a message capture group is mandatory
                    if 'warning' in level.lower() or 'attention' in level.lower():
                        level = CheckerMessages.WARNING
                    else:
                        level = CheckerMessages.ERROR
                    # make relative path absolute
                    path = '-'
                    if filename:
                        path = os.path.abspath(os.path.join(os.path.expanduser(working_dir), filename))
                    if use_tuples:
                        msg = (message, level, line_nbr, 0, None, None, path)
                    else:
                        msg = CheckerMessage(message, level, line_nbr, path=path)
                    issues.append(msg)
                    break
        return issues