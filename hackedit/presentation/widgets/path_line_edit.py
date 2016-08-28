import os

from PyQt5 import QtWidgets
from hackedit.presentation.icon_provider import FileIconProvider


class PathLineEdit(QtWidgets.QLineEdit):
    """
    Line edit specialised for choosing a path.

    Features:
        - use QCompleter with a QDirModel to automatically complete paths.
        - allow user to drop files and folders to set url text
    """
    class Completer(QtWidgets.QCompleter):
        def splitPath(self, path):
            path = os.path.split(os.pathsep)[-1]
            return super().splitPath(path)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        completer = self.Completer()
        model = QtWidgets.QDirModel(completer)
        model.setIconProvider(FileIconProvider())
        completer.setModel(model)
        self.setCompleter(completer)
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            # for some reason, this doubles up the intro slash
            filepath = urls[0].path()
            if os.system.windows and filepath.startswith('/'):
                filepath = filepath[1:]
                filepath = os.path.normpath(filepath)
            self.setText(filepath)
            self.setFocus()
