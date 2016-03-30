import os
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqode.core.widgets import FileSystemTreeView

import pytest_hackedit

from hackedit.api import editor, window


DATA_FILES_PATH = os.path.join(os.getcwd(), 'tests', 'data')
PROJ_PATH = os.path.join(DATA_FILES_PATH, 'FooBarProj')
FILE1 = os.path.join(PROJ_PATH, 'module.py')
FILE2 = os.path.join(PROJ_PATH, 'setup.py')
PATH2 = os.path.join(DATA_FILES_PATH, 'SpamEggsProj')


def test_add_tab_widget_context_menu_action(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    window.add_tab_widget_context_menu_action(QtWidgets.QAction('Test', w))
    pytest_hackedit.close_main_window(w)


def test_get_tab_under_context_menu(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    editor.open_file(FILE1)
    assert window.get_tab_under_context_menu() is None
    pytest_hackedit.close_main_window(w)


def test_add_dock_widget(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    editor.open_file(FILE1)
    dw = window.add_dock_widget(
        QtWidgets.QPushButton(), 'FooDock',
        QtGui.QIcon.fromTheme('document-save'),
        QtCore.Qt.BottomDockWidgetArea)
    assert dw is not None
    assert isinstance(dw, QtWidgets.QDockWidget)
    pytest_hackedit.close_main_window(w)


def test_remove_dock_widget(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    editor.open_file(FILE1)
    dw = window.add_dock_widget(
        QtWidgets.QPushButton(), 'FooDock2',
        QtGui.QIcon.fromTheme('document-save'),
        QtCore.Qt.BottomDockWidgetArea)
    window.remove_dock_widget(dw)
    pytest_hackedit.close_main_window(w)


def test_get_dock_widget(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    editor.open_file(FILE1)
    dw = window.add_dock_widget(
        QtWidgets.QPushButton(), 'FooDock',
        QtGui.QIcon.fromTheme('document-save'),
        QtCore.Qt.BottomDockWidgetArea)
    ret_val = window.get_dock_widget('FooDock')
    assert ret_val == dw
    pytest_hackedit.close_main_window(w)


def test_get_main_window(qtbot):
    ref = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    w = window.get_main_window()
    assert w == ref
    pytest_hackedit.close_main_window(ref)


def test_get_toolbar(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    tb = window.get_toolbar('toolBarFile', 'FileToolBar')
    assert isinstance(tb, QtWidgets.QToolBar)
    pytest_hackedit.close_main_window(w)


def test_add__action(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    window.add_action(QtWidgets.QAction('Test', w))
    pytest_hackedit.close_main_window(w)


def test_get_menu(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    mnu = window.get_menu(_('Edit'))
    assert mnu is not None
    assert isinstance(mnu, QtWidgets.QMenu)
    pytest_hackedit.close_main_window(w)


def test_get_project_treeview(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    assert isinstance(window.get_project_treeview(), FileSystemTreeView)
    pytest_hackedit.close_main_window(w)


def test_add_statusbar_widget(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    lbl = QtWidgets.QLabel()
    window.add_statusbar_widget(lbl)
    pytest_hackedit.close_main_window(w)
