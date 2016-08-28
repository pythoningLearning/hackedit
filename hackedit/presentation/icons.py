"""
This module contains utility function to retrieve common icons.

Icons are always loaded from an icon theme (the system icon theme on Linux
and the embedded Breeze theme on Windows and OSX)
"""
import logging
import os
import sys

from PyQt5.QtGui import QIcon

from hackedit.application import system


class Icons:
    ORIGINAL_THEME_NAME = QIcon.themeName()

    def __init__(self):
        self._init_search_path()

    @staticmethod
    def icon_themes():
        themes = []
        for path in QIcon.themeSearchPaths():
            try:
                dirs = os.listdir(path)
            except OSError:
                _logger().debug('failed to list icons in path %r', path)
            else:
                for d in dirs:
                    pth = os.path.join(path, d)
                    if os.path.isfile(pth):
                        continue
                    try:
                        files = os.listdir(pth)
                    except OSError:
                        pass
                    else:
                        if 'cursors' not in files and 'index.theme' in files:
                            themes.append(d)
        return sorted(list(set(themes)))

    @staticmethod
    def system_icon_theme():
        """
        Gets the system icon theme (this is only useful on linux).
        """
        theme = QIcon.themeName()
        if theme == '':
            if system.LINUX:
                theme = 'default'
            else:
                theme = 'breeze' if not system.is_dark_theme() else 'breeze-dark'
        return theme

    @staticmethod
    def set_icon_theme(icon_theme):
        if icon_theme:
            QIcon.setThemeName(icon_theme)
            _logger().debug('icon theme: %s', icon_theme)

    @staticmethod
    def _init_search_path():
        paths = QIcon.themeSearchPaths()
        paths.append(os.path.join(sys.prefix, 'share', 'hackedit', 'icons'))
        paths.append('/usr/local/share/hackedit/icons')
        QIcon.setThemeSearchPaths(list(set(paths)))
        _logger().debug('icon theme path: %r', paths)

    @staticmethod
    def configure_icon(build=False):
        """
        Gets the "configure" icon (for actions like configure project/build,...)
        """
        if build and QIcon.hasThemeIcon('run-build-configure'):
            return QIcon.fromTheme('run-build-configure')  # pragma: no cover
        if QIcon.hasThemeIcon('configure'):
            return QIcon.fromTheme('configure')
        else:  # pragma: no cover
            return QIcon.fromTheme('apps-system')

    @staticmethod
    def run_icon():
        """
        Gets the "run" icon (for actions like run script,...)

        :param build: True to get the run build icon.
        """
        if QIcon.hasThemeIcon('debug-run'):
            return QIcon.fromTheme('system-run')
        else:
            return QIcon(':/icons/special/start.png')

    @staticmethod
    def run_debug_icon():
        """
        Gets the "debug" icon (for actions like start debugging,...)
        """
        if QIcon.hasThemeIcon('debug-run'):
            return QIcon.fromTheme('debug-run')
        else:
            return QIcon(':/icons/special/debugger_start.png')

    @staticmethod
    def class_icon():
        """
        Gets the icon used to represent a "class" item.
        """
        return QIcon.fromTheme(
            'code-class', QIcon(':/icons/special/class.png'))

    @staticmethod
    def variable_icon():
        """
        Gets the icon used to represent a "variable".
        """
        return QIcon.fromTheme(
            'code-variable', QIcon(':/icons/special/var.png'))

    @staticmethod
    def function_icon():
        """
        Gets the icon used to represent a "function".
        """
        return QIcon.fromTheme(
            'code-function', QIcon(':/icons/special/func.png'))

    @staticmethod
    def namespace_icon():
        """
        Gets the icon used to represent a "namespace".
        """
        return QIcon.fromTheme(
            'code-context',
            QIcon(':/icons/special/namespace.png'))

    @staticmethod
    def object_locked():
        """
        Gets the object-locked icon.
        """
        if QIcon.hasThemeIcon('object-locked'):
            icon_lock = QIcon.fromTheme('object-locked')
        else:
            return QIcon(':/icons/special/lock.png')
        return icon_lock

    @staticmethod
    def object_unlocked():
        """
        Gets the object-unlocked icon.
        """
        if QIcon.hasThemeIcon('object-unlocked'):
            icon_unlock = QIcon.fromTheme('object-unlocked')
        else:
            return QIcon(':/icons/special/unlock.png')
        return icon_unlock

    @staticmethod
    def debug_step_into_icon():
        """
        Gets the "step into" debug icon.
        """
        if QIcon.hasThemeIcon('debug-step-into'):
            return QIcon.fromTheme('debug-step-into')
        else:
            return QIcon(':/icons/special/debug-step-into.png')

    @staticmethod
    def debug_step_over_icon():
        """
        Gets the "step over" debug icon.
        """
        if QIcon.hasThemeIcon('debug-step-over'):
            return QIcon.fromTheme('debug-step-over')
        else:
            return QIcon(':/icons/special/debug-step-over.png')

    @staticmethod
    def debug_step_out_icon():
        """
        Gets the "step out" debug icon.
        """
        if QIcon.hasThemeIcon('debug-step-out'):
            return QIcon.fromTheme('debug-step-out')
        else:
            return QIcon(':/icons/special/debug-step-out.png')

    @staticmethod
    def breakpoint_icon():
        """
        Gets the icon used to represent a breakpoint.
        """
        return QIcon(':/icons/special/breakpoint.png')

    @staticmethod
    def edit_breakpoints_icon():
        """
        Gets the icons used for the edit breakpoints action.
        """
        return QIcon(':/icons/special/breakpoints.png')

    @staticmethod
    def run_build():
        if QIcon.hasThemeIcon('run-build'):
            return QIcon.fromTheme('run-build')
        else:
            return QIcon.fromTheme('system-run')

    @staticmethod
    def build_clean():
        if QIcon.hasThemeIcon('run-build-clean'):
            return QIcon.fromTheme('run-build-clean')
        else:
            return QIcon.fromTheme('edit-clear')

    @staticmethod
    def app_menu():
        if QIcon.hasThemeIcon('application-menu'):
            return QIcon.fromTheme('application-menu')
        else:
            return QIcon.fromTheme('open-menu-symbolic')


def _logger():
    return logging.getLogger(__name__)
