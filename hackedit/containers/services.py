from dependency_injector import containers, providers


from ._factories.logging import LoggingSystemFactory
from ._factories.mime_types import MimeTypesServiceFactory
from ._factories.recents import RecentFilesManagerFactory
from ._factories.settings import SettingsFactory


class Services(containers.DeclarativeContainer):
    """
    Contains the application services/objects.
    """

    logging = providers.Singleton(LoggingSystemFactory())
    """
    The logging system let you control the current logging level, get the current application log content,...

    Use ``logging.getLogger(__name__)`` to get a logger for your module.

    :rtype logger: hackedit.application.compilers.logger.ILoggingSystem
    """

    recent_projects = providers.Singleton(RecentFilesManagerFactory())
    """
    Gets the recent projects manager.

    :rtype recent_projects: pyqode.core.widgets.RecentFilesManager
    """

    settings = providers.Singleton(SettingsFactory())
    """
    Gets the application settings

    :type settings: hackedit.application.services.settings.Settings
    """

    mime_types = providers.Singleton(MimeTypesServiceFactory())