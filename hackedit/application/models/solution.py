class ProjectPathModel:
    def __init__(self):
        self.path = ''
        self.virtual_folder = ''

    def serialize(self):
        return {
            'path': self.path,
            'virtual-folder': self.virtual_folder
        }

    def deserialize(self, data):
        self.path = data['path']
        self.virtual_folder = data['virtual-folder']
        return self


class SolutionModel:
    def __init__(self):
        self.name = ''
        self.projects = []
        self.virtual_folders = []

    def serialize(self):
        return {
            'name': self.name,
            'projects': [p.serialize() for p in self.projects],
            'virtual-folders': self.virtual_folders
        }

    def deserialize(self, data):
        self.name = data['name']
        self.projects = [ProjectPathModel().deserialize(pdata) for pdata in data['projects']]
        self.virtual_folders = data['virtual-folders']
        return self
