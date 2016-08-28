from dependency_injector import containers, providers


from ._factories.logging import LoggingSystemFactory
from ._factories.mime_types import MimeTypesServiceFactory
from ._factories.plugin_loader import PluginLoaderFactory
from ._factories.plugin_manager import PluginManagerFactory
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

    :rtype hackedit.application.compilers.logger.ILoggingSystem
    """

    recent_projects = providers.Singleton(RecentFilesManagerFactory())
    """
    Gets the recent projects manager.

    :rtype pyqode.core.widgets.RecentFilesManager
    """

    settings = providers.Singleton(SettingsFactory())
    """
    Gets the application settings

    :rtype hackedit.application.services.settings.Settings
    """

    mime_types = providers.Singleton(MimeTypesServiceFactory())
    """
    Gets the mime-types service.

    :rtype: hackedit.application.services.mime_types.MimeTypesService
    """

    plugin_loader = providers.Singleton(PluginLoaderFactory())
    """
    Gets the plugin loader.

    :rtype: hackedit.application.interfaces.plugin_loader.IPluginLoader
    """

    plugin_manager = providers.Singleton(PluginManagerFactory())
    """
    Gets the plugin manager.

    :rtype: hackedit.application.services.plugin_manager.PluginManager
    """
