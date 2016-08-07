

class FileModel:
    def __init__(self):
        self.type = 'File'
        self.path = ''
        self.properties = None
        self.virtual_folder = ''

    def deserialize(self, data):
        self.type = data['type']
        self.path = data['path']
        self.virtual_folder = data['virtual-folder']
        return self

    def serialize(self):
        data = {
            'path': self.path,
            'type': self.type,
            'virtual-folder': self.virtual_folder
        }
        return data


class ScriptModel(FileModel):
    def __init__(self):
        super().__init__()
        self.type = 'Script'


class CompilableFileModel(FileModel):
    def __init__(self):
        super().__init__()
        self.overrides = {}
        self.type = 'Compilable'

    def deserialize(self, data):
        super().deserialize(data)
        self.overrides = data['overrides']
        return self

    def serialize(self):
        data = super().serialize()
        data['overrides'] = self.overrides
        return data
