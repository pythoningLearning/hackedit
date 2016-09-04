from PyQt5 import QtWidgets

from hackedit.containers import Services, View
from pyqode.core.widgets import RecentFilesManager


class TestWelcomeWindow:
    @classmethod
    def setup_class(cls):
        cls.recent_projects = Services.recent_projects()
        cls.window = View.welcome_window()

    def setup_method(self, *_):
        self.recent_projects.clear()
        self.recent_projects.open_file(__file__)
        self.recent_projects.open_file(QtWidgets.__file__)
        self.window.update_recents()

    def test_show(self, mock, qtbot):
        mock.spy(self.window, 'setGeometry')
        self.window.show()
        assert self.window.setGeometry.call_count == 1
        self.window.hide()

    def test_click_on_quit(self, mock):
        mock.patch.object(QtWidgets.qApp, 'quit')
        self.window._ui.bt_quit.click()
        assert QtWidgets.qApp.quit.call_count == 1

    def test_remove_current_requested(self):
        # this is normally done by the context menu of the recents file list
        assert self.window._ui.list_recents.count() == 2
        assert len(self.recent_projects.get_recent_files()) == 2
        self.window._ui.list_recents.setCurrentRow(0)
        self.window.on_list_recents_remove_current_requested()
        assert self.window._ui.list_recents.count() == 1
        assert len(self.recent_projects.get_recent_files()) == 1

    def test_clear_requested(self):
        # this is normally done by the context menu of the recents file list
        assert self.window._ui.list_recents.count() == 2
        assert len(self.recent_projects.get_recent_files()) == 2
        self.window.on_list_recents_clear_requested()
        assert self.window._ui.list_recents.count() == 0
        assert len(self.recent_projects.get_recent_files()) == 0
