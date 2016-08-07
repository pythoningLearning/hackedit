from dependency_injector import containers, providers


from ._factories.file_factory import FileFactoryFactory


class Factories(containers.DeclarativeContainer):
    """
    Contains the different object factories of the application
    """
    file_model_factory = providers.Singleton(FileFactoryFactory())
