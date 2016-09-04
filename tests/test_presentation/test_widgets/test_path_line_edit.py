import os

from PyQt5.QtWidgets import QDirModel

from hackedit.application import system
from hackedit.presentation.icon_provider import FileIconProvider
from hackedit.presentation.widgets.path_line_edit import PathLineEdit


class FakeDragEvent:
    class Url:
        def scheme(self):
            return 'file'

        def path(self):
            return __file__

    class MimeData:
        def urls(self):
            return [FakeDragEvent.Url()]

    def mimeData(self):
        return FakeDragEvent.MimeData()

    def acceptProposedAction(self):
        pass


class TestPathLineEdit:
    def _get_widget(self, qtbot):
        widget = PathLineEdit()
        qtbot.addWidget(widget)
        return widget

    def test_has_completer(self, qtbot):
        widget = self._get_widget(qtbot)
        assert widget.completer() is not None

    def test_has_dir_model(self, qtbot):
        assert isinstance(self._get_widget(qtbot).completer().model(), QDirModel)

    def test_use_own_icon_provider(self, qtbot):
        assert isinstance(self._get_widget(qtbot).completer().model().iconProvider(), FileIconProvider)

    def test_drag_is_enabled(self, qtbot):
        assert self._get_widget(qtbot).dragEnabled() is True

    def test_completer(self, qtbot):
        widget = self._get_widget(qtbot)
        widget.show()
        qtbot.waitForWindowShown(widget)
        widget.setText(os.path.dirname(__file__))
        assert widget.completer().popup().isVisible() is False
        qtbot.keyPress(widget, '\\' if system.WINDOWS else '/')
        assert widget.completer().popup().isVisible() is True

    def test_drag_and_drop(self, qtbot, mock):
        widget = self._get_widget(qtbot)
        event = FakeDragEvent()
        mock.spy(event, 'acceptProposedAction')

        widget.dragEnterEvent(event)
        assert event.acceptProposedAction.call_count == 1

        widget.dragMoveEvent(event)
        assert event.acceptProposedAction.call_count == 2

        widget.dropEvent(event)
        assert widget.text() == __file__

