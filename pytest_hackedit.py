"""
This module contains a bunch of utility functions for testing HackEdit (and its
plugins). This module is part of the hackedit distribution. To use it, just
import pytest_hackedit and use one of the available functions.
"""
import os
import shutil
import sys

from PyQt5 import QtCore, QtWidgets, QtTest

from hackedit.api import project
from hackedit.app import settings


APP = None
WINDOWS = {}


def main_window(qtbot, path, remove_project_folder=False):
    """
    Creates a MainWindow with the given path.

    :param qtbot: qtbot fixture from pytest-qtbot
    :param path: path of the project to open
    :param remove_project_folder: True to remove .hackedit folder in the
                                  specified path.
    """
    global WINDOWS
    if remove_project_folder:
        try:
            shutil.rmtree(os.path.join(path, project.FOLDER))
        except OSError:
            pass
    a = app()
    settings.load()
    QtCore.QSettings().clear()
    settings.set_confirm_app_exit(False)
    if path not in WINDOWS.keys():
        a.open_path(path)
        WINDOWS[path] = a.editor_windows[-1]
    w = WINDOWS[path]
    w.tab_widget.close_all()
    QtWidgets.qApp.setActiveWindow(w)
    QtTest.QTest.qWaitForWindowExposed(w)
    return w


def close_main_window(main_window):
    """
    Close the specified main window.

    :param main_window: the main window instance to close.
    """
    global WINDOWS
    try:
        WINDOWS.pop(main_window._open_projects[0])
    except KeyError:
        pass
    main_window.close()


def app():
    """
    Get the hackedit application instance.
    """
    from hackedit.app.application import Application
    from hackedit.app import argparser
    global APP
    if APP is None:
        sys.argv = [sys.argv[0]]
        APP = Application(QtWidgets.qApp, None, args=argparser.parse_args())
    return APP
