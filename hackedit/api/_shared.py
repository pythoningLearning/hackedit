"""
**Internal** helper module shared by most api modules to retrieve the current
MainWindow instance.
"""
import inspect

from PyQt5 import QtWidgets


APP = None


def _window():
    """
    Retrieves window instance from the caller object (usually a WorkspacePlugin
    or a WindowPlugin).

    If there is no caller object, the active window is used, this allow
    to hack HackEdit from the IPython console!

    This is used to simplify the public API: plugins don't need to pass
    the `window` parameter to the public API functions everytime...

    :rtype: hackedit.app.gui.main_window.MainWindow
    """
    def caller():
        frame = inspect.stack()[3][0]
        caller = frame.f_locals.get('self')
        return caller

    try:
        w = caller().window
        if w:
            return w
        raise AttributeError('window is None')
    except (AttributeError, IndexError):
        # not from a plugin, use active window instead
        w = QtWidgets.qApp.activeWindow()

        from hackedit.app.main_window import MainWindow

        if not isinstance(w, MainWindow):
            try:
                w = APP.editor_windows[0]
            except IndexError:
                w = None
            if w is None:
                w = APP.last_window
        if isinstance(w, MainWindow):
            return w
        return None
