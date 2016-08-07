class RunConfigModel:
    def __init__(self):
        self.name = ''
        self.program = ''
        self.program_arguments = []
        self.environment_variables = {}
        self.working_directory = ''

    def deserialize(self, data):
        self.name = data['name']
        self.program = data['program']
        self.program_arguments = data['program-arguments']
        self.environment_variables = data['environment-variables']
        self.working_directory = data['working-directory']
        return self

    def serialize(self):
        return {
            'name': self.name,
            'program': self.program,
            'program-arguments': self.program_arguments,
            'environment-variables': self.environment_variables,
            'working-directory': self.working_directory
        }


class ScriptRunConfigModel:
    def __init__(self):
        self.name = ''
        self.interpreter_arguments = []
        self.script = ''
        self.script_arguments = []
        self.environment_variables = {}
        self.working_directory = ''

    def deserialize(self, data):
        self.name = data['name']
        self.script = data['script']
        self.script_arguments = data['script-arguments']
        self.interpreter_arguments = data['interpreter-arguments']
        self.environment_variables = data['environment-variables']
        self.working_directory = data['working-directory']
        return self

    def serialize(self):
        return {
            'name': self.name,
            'interpreter-arguments': self.interpreter_arguments,
            'script': self.script,
            'script-arguments': self.script_arguments,
            'environment-variables': self.environment_variables,
            'working-directory': self.working_directory
        }
