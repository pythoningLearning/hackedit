class QtAppFactory:  # pragma: no cover
    def __call__(self):
        from hackedit.infrastructure.qt_app import QtApplication
        return QtApplication()
