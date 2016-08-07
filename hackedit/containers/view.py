from dependency_injector import containers, providers

from ._factories.welcome_window import WelcomeWindowFactory
from ._factories.icons import IconsFactory


class View(containers.DeclarativeContainer):
    """
    Contains all the views of the application.
    """
    welcome_window = providers.Singleton(WelcomeWindowFactory())
    """
    :type welcome_window: hackedit.presentation.windows.welcome.WelcomeWindow
    """

    icons = providers.Singleton(IconsFactory())
    """
    :type icons: hackedit.presentation.icons.IconsService
    """
