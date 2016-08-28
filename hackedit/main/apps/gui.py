import os
import sys

from hackedit.api import system
from hackedit.containers import Services, View
from hackedit.presentation.forms import hackedit_rc

from .base import BaseApplication

assert hackedit_rc


class GuiApplication(BaseApplication):
    def __init__(self):
        super().__init__()
        self._init_standard_streams()
        self._init_icons()
        self._init_mimetypes()
        self._welcome_window = View.welcome_window()

    def _init_mimetypes(self):
        self._mimetypes = Services.mime_types()

    def _init_icons(self):
        View.icons().set_icon_theme(Services.settings().environment.icon_theme)

    def _init_standard_streams(self):  # pragma: no cover
        # Use a file for stdout/stderr if sys.stdout/sys.stderr is None
        # This happens when running the app on Windows with pythow.exe or when
        # running from the native launcher.
        app_data = system.get_app_data_directory()
        stdout_path = os.path.join(app_data, 'stdout-pid%d' % os.getpid())
        stderr_path = os.path.join(app_data, 'stderr-pid%d' % os.getpid())
        if sys.stdout is None:
            sys.stdout = open(stdout_path, 'w')
        if sys.stderr is None:
            sys.stderr = open(stderr_path, 'w')

    def run(self):  # pragma: no cover
        self._welcome_window.show()
        self.exec_()
