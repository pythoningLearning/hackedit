from hackedit.api import mixins


class InterpreterConfig(mixins.JSonisable, mixins.Copyable):
    def __init__(self):
        self.name = ''
        self.command = ''
        self.type_name = ''
        self.mimetypes = []
        self.environment_variables = {}
        self.command_pattern = '$command $interpreter_arguments $script $script_arguments'
        self.version_command = ['--version']
        self.version_regex = r'(?P<version>\d\.\d\.\d)'
        self.test_command = []

    def __repr__(self):
        return 'InterpreterConfig(%s)' % self.to_json()

