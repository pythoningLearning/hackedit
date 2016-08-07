class QtAppFactory:
    def __call__(self):  # pragma: no cover
        from hackedit.infrastructure.qt_app import QtApplication
        return QtApplication()
