class FileFactoryFactory:
    def __call__(self):
        from hackedit.application.factories.file import FileModelFactory
        return FileModelFactory()
