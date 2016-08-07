class RecentFilesManagerFactory:
    def __call__(self):
        from pyqode.core.widgets import RecentFilesManager
        return RecentFilesManager('HackEdit', 'HackEdit')
