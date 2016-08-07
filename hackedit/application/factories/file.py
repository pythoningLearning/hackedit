from hackedit.application.models.file import FileModel, ScriptModel, CompilableFileModel


class FileModelFactory:
    _file_types = {}

    @classmethod
    def register(cls, type_name, type_class):
        cls._file_types[type_name] = type_class

    def create(self, type_name):
        return self._file_types[type_name]()

    def deserialize(self, data):
        model = self.create(data['type'])
        return model.deserialize(data)


FileModelFactory.register('File', FileModel)
FileModelFactory.register('Script', ScriptModel)
FileModelFactory.register('Compilable', CompilableFileModel)
