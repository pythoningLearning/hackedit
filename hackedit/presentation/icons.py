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

    def icon_themes(self):
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

    def system_icon_theme(self):
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

    def set_icon_theme(self, icon_theme):
        if icon_theme:
            QIcon.setThemeName(icon_theme)
            _logger().debug('icon theme: %s', icon_theme)

    def _init_search_path(self):
        paths = QIcon.themeSearchPaths()
        paths.append(os.path.join(sys.prefix, 'share', 'hackedit', 'icons'))
        paths.append('/usr/local/share/hackedit/icons')
        QIcon.setThemeSearchPaths(list(set(paths)))
        _logger().debug('icon theme path: %r', paths)


def _logger():
    return logging.getLogger(__name__)
