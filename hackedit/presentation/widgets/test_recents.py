from PyQt5 import QtCore, QtGui, QtWidgets

from hackedit.presentation.widgets.recents import RecentFilesListWidget

class TestRecentsFilesListWidget:
    def get_widget(self, qtbot):
        widget = RecentFilesListWidget()
        qtbot.addWidget(widget)
        return widget

    def test_show_context_menu(self, qtbot, mock):
        def close_menu():
            QtWidgets.qApp.closeAllWindows()

        mock.spy(QtWidgets, 'QAction')

        widget = self.get_widget(qtbot)
        QtCore.QTimer.singleShot(100, close_menu)
        widget.show_context_menu(QtCore.QPoint())
        QtWidgets.QAction.call_count == 2

    def test_mouse_move_event_with_item(self, qtbot, mock):
        widget = self.get_widget(qtbot)
        widget.show()
        qtbot.waitForWindowShown(widget)
        item = QtWidgets.QListWidgetItem()
        widget.addItem(item)

        mock.patch.object(widget, 'itemAt')
        widget.itemAt.return_value = item
        mock.spy(widget, 'setCursor')

        event = QtGui.QMouseEvent(QtGui.QMouseEvent.MouseMove, QtCore.QPointF(), QtCore.Qt.RightButton,
                                  QtCore.Qt.NoButton, QtCore.Qt.NoModifier)
        widget.mouseMoveEvent(event)

        widget.setCursor.assert_called_once_with(QtCore.Qt.PointingHandCursor)
        assert widget.currentRow() == widget.row(item)
