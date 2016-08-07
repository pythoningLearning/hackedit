class BuildConfigModel:
    def __init__(self):
        self.name = ''
        self.overrides = {}
        self.output_directory = ''
        self.build_steps = {
            'pre': '',
            'post': ''
        }

    def serialize(self):
        return {
            'name': self.name,
            'output-directory': self.output_directory,
            'overrides': self.overrides,
            'build-steps': self.build_steps
        }

    def deserialize(self, data):
        self.name = data['name']
        self.output_directory = data['output-directory']
        self.overrides = data['overrides']
        self.build_steps = data['build-steps']
        return self
