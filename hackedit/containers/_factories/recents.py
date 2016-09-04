from PyQt5.QtWidgets import qApp

class RecentFilesManagerFactory:
    def __call__(self):
        from pyqode.core.widgets import RecentFilesManager
        return RecentFilesManager(qApp.organizationName(), qApp.organizationName())
