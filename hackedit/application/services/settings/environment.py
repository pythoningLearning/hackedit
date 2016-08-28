import logging

from PyQt5 import QtWidgets
from hackedit.api import system
from hackedit.api.constants import OpenMode
from hackedit.containers import View
from pyqode.core.widgets import FileSystemContextMenu

from .section import SettingsSection


class EnvironmentSettingsSection(SettingsSection):
    DEFAULT_IGNORE_PATTERNS = [
        '.git', '.hg', '.svn', '_svn', '.hackedit', '.tox', '.cache', '*~',
        '*.pyc', '*.pyo', '*.coverage', '.DS_Store', '__pycache__'
    ]

    IGNORE_PATTERNS_STR = ';'.join(DEFAULT_IGNORE_PATTERNS)

    def __init__(self, qsettings):
        super().__init__('env', qsettings)

    def get_defaults(self):
        return {
            'show_menu': False,
            'widescreen_layout': self.is_wide_screen(),
            'show_tray_icon': False,
            'icon_theme': View.icons().system_icon_theme(),
            'dark_theme': False,
            'toolbar_icon_size': 22,
            'restore_session': True,
            'file_manager_command': self.get_default_file_manager_command(),
            'cmd_open_folder_in_terminal': system.get_cmd_open_folder_in_terminal(),
            'cmd_run_command_in_terminal': system.get_cmd_run_command_in_terminal(),
            'locale': 'default',
            'use_default_browser': 1 if not system.DARWIN else 0,
            'custom_browser_command': self.get_default_browser_commands(),
            'show_splashscreen': True,
            'automatically_check_for_updates': self.get_default_automatically_check_for_updates(),
            'restore_last_window': False,
            'confirm_application_exit': True,
            'open_mode': OpenMode.ASK_EACH_TIME,
            'ignored_patterns': self.IGNORE_PATTERNS_STR,
            'show_notification_in_sytem_tray': True,
            'auto_open_info_notification': True,
            'auto_open_warning_notification': True,
            'auto_open_error_notification': True,
            'log_level': logging.INFO,
            'indexing_enabled': True,
            'mimetypes': '{}'
        }

    @staticmethod
    def is_wide_screen():
        rec = QtWidgets.qApp.desktop().screenGeometry()
        ratio = rec.width() / rec.height()
        wide = False
        if ratio > 4 / 3:
            wide = True
        return wide

    @staticmethod
    def get_default_file_manager_command():
        return FileSystemContextMenu.get_file_explorer_command()

    @staticmethod
    def get_default_browser_commands():
        default = 'firefox %s'
        if system.DARWIN:
            default = 'open -b com.apple.Safari %s'
        return default

    @staticmethod
    def get_default_automatically_check_for_updates():
        default = True
        if system.LINUX:
            # on linux, package manager should be preferred
            default = False
        return default