from hackedit.api.errors import CommandBuildFailedError


class CommandBuilder:
    """
    Build a command based on a pattern and a dict of options.

    The pattern is a list of string with substitutable options: $xyz where xyz is a key of the options_dict.

    Example::

        >>> builder = CommandBuilder('-o $output_file_name -i $input_file_name', {
                'output_file_name': 'bin/test',
                'input_file_name': 'test.cbl'
            })
        >>> builder.as_list()
        ['-o', 'bin/test', '-i', 'test.cbl']
        >>> builder.as_string()
        '-o bin/test -i test.cbl'

    """
    def __init__(self, pattern, options_dict):
        """
        :param pattern: the command pattern string.
        :type pattern: str
        :param options_dict: the options_dict
        :type options_dict: dict
        """
        self._result = None
        self._pattern = pattern
        self._options_dict = options_dict

    def as_string(self):
        """
        Returns the built command as a single string.
        """
        self._build()
        return ' '.join(self.as_list())

    def as_list(self):
        """
        Returns the built command as a list.
        """
        self._build()
        return [t.strip() for t in self._result.strip().split(' ') if t]

    def _build(self):
        if self._result is not None:
            return
        args = []
        for pattern in self._pattern.strip().split(' '):
            if '$' in pattern:
                args.append(self._build_pattern(pattern))
            else:
                args.append(pattern)
        self._result = ' '.join(args)

    def _build_pattern(self, pattern):
        index = pattern.find('$')
        key = pattern[index + 1:]
        option = pattern[:index]
        k = self.find_closest_key(key)
        if k:
            value = self._options_dict[k]
            remaining = key.replace(k, '')
            if option:
                return self._get_value_with_option(option, value, remaining)
            else:
                return self._get_value(value, remaining)
        else:
            raise CommandBuildFailedError(_('Pattern %r not found in options dict') % pattern)

    def find_closest_key(self, key):
        """
        :type key: str
        """
        try:
            key = key[:key.index('.')]
        except ValueError:
            pass
        found = {}
        for k in self._options_dict.keys():
            if k in key:
                found[len(k)] = k
        for klen in sorted(found.keys()):
            if klen >= len(key):
                return found[klen]
        return None

    @staticmethod
    def _get_value(value, remaining):
        if isinstance(value, list):
            return ' '.join([v + remaining for v in value])
        else:
            return str(value) + remaining

    @staticmethod
    def _get_value_with_option(option, value, remaining):
        if isinstance(value, list):
            return ' '.join([option + v + remaining + ' ' for v in value])
        else:
            return option + str(value) + remaining