import logging
import mimetypes

from PyQt5 import QtCore, QtGui, QtWidgets
from dependency_injector.injections import inject
from hackedit.application import plugins
from hackedit.containers import Services
from pyqode.core.api import utils


class FileIconProvider(QtWidgets.QFileIconProvider):
    """
    Provides file/folder icons based on their mimetype.

    To extend this class, just create a FileIconProviderPlugin
    """

    @inject(plugin_manager=Services.plugin_manager)
    def __init__(self, plugin_manager):
        super().__init__()
        self.plugins = plugin_manager.get_plugins(plugins.FileIconProviderPlugin.METADATA.category).values()

    @staticmethod
    def mimetype_icon(path, fallback=None):
        """
        Tries to create an icon from theme using the file mimetype.

        E.g.::

            return self.mimetype_icon(
                path, fallback=':/icons/text-x-python.png')

        :param path: file path for which the icon must be created
        :param fallback: fallback icon path (qrc or file system)
        :returns: QIcon
        """
        if 'CMakeLists.txt' not in path:
            path = 'file.%s' % QtCore.QFileInfo(path).suffix()
        return _get_mimetype_icon(path, fallback)

    def icon(self, type_or_info):
        if isinstance(type_or_info, str):
            type_or_info = QtCore.QFileInfo(type_or_info)
        if isinstance(type_or_info, QtCore.QFileInfo):
            if type_or_info.isDir():
                return QtGui.QIcon.fromTheme('folder')
            else:
                for plugin in self.plugins:
                    ret_val = plugin.icon(type_or_info)
                    if ret_val is not None:
                        return ret_val
                return self.mimetype_icon(type_or_info.absoluteFilePath())
        else:
            theme_map = {
                FileIconProvider.File: 'text-x-generic',
                FileIconProvider.Folder: 'folder',
            }
            try:
                return QtGui.QIcon.fromTheme(theme_map[type_or_info])
            except KeyError:
                return super().icon(type_or_info)


@utils.memoized
def _get_mimetype_icon(path, fallback):
    if 'CMakeLists.txt' in path:
        mime = 'text/x-cmake'
    else:
        mime = mimetypes.guess_type(path)[0]
    if mime:
        icon = mime.replace('/', '-')
        gicon = 'gnome-mime-%s' % icon
        has_icon = QtGui.QIcon.hasThemeIcon(icon)
        if QtGui.QIcon.hasThemeIcon(gicon) and not has_icon:
            return QtGui.QIcon.fromTheme(gicon)
        elif has_icon:
            return QtGui.QIcon.fromTheme(icon)
    if fallback:
        return fallback
    return QtGui.QIcon.fromTheme('text-x-generic')


def _logger():
    return logging.getLogger(__name__)
