"""
This module contains a plugin that is able to render the html preview of
the current editor.
"""
from PyQt5 import QtGui, QtCore, QtWidgets
from pyqode.core.widgets import HtmlPreviewWidget

from hackedit import api


class HtmlPreview(api.plugins.WorkspacePlugin):
    def activate(self):
        self.preview = HtmlPreviewWidget()
        self._dock = api.window.add_dock_widget(
            self.preview, _('HTML Preview'), icon=QtGui.QIcon.fromTheme(
                'text-html'), area=QtCore.Qt.RightDockWidgetArea)
        api.signals.connect_slot(api.signals.CURRENT_EDITOR_CHANGED,
                                 self.preview.set_editor)
        self.preview.hide_requested.connect(self._dock.hide)
        self.preview.show_requested.connect(self._dock.show)
        self.preview.set_editor(None)

        if api.utils.is_dark_theme():
            p = self.preview.palette()
            p.setColor(QtGui.QPalette.Base, QtCore.Qt.white)
            self.preview.setPalette(p)

        self._dock.hide()
