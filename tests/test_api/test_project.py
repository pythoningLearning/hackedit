import os
import shutil

from PyQt5 import QtTest

import pytest_hackedit
from hackedit.api import project
from hackedit.app import settings

PATH1 = os.path.join(os.getcwd(), 'tests', 'data', 'SpamEggsProj2')
PATH2 = os.path.join(os.getcwd(), 'tests', 'data', 'SpamEggsProj3')


def test_open_proj_current_window(qtbot):
    w = pytest_hackedit.main_window(qtbot, PATH1,
                                    remove_project_folder=True)
    settings.set_open_mode(settings.OpenMode.CURRENT_WINDOW)
    assert settings.open_mode() == settings.OpenMode.CURRENT_WINDOW
    assert len(project.get_projects()) == 1
    project.open_project(PATH2, sender=w)
    assert len(project.get_projects()) == 2
    QtTest.QTest.qWait(1000)
    pytest_hackedit.close_main_window(w)


def test_add_project(qtbot):
    w = pytest_hackedit.main_window(qtbot, PATH1, remove_project_folder=True)
    assert len(project.get_projects()) == 1
    project.add_project(PATH2)
    assert len(project.get_projects()) == 2
    pytest_hackedit.close_main_window(w)


def test_open_proj_new_window(qtbot):
    w = pytest_hackedit.main_window(qtbot, PATH1,
                                    remove_project_folder=True)
    settings.set_open_mode(settings.OpenMode.NEW_WINDOW)
    assert len(project.get_projects()) == 1
    project.open_project(PATH2, sender=w)
    assert len(w.app.editor_windows) == 2
    assert len(project.get_projects()) == 1
    pytest_hackedit.close_main_window(w)

    pytest_hackedit.close_main_window(pytest_hackedit.app().editor_windows[0])


def setup():
    try:
        shutil.rmtree(os.path.join(PATH1, project.FOLDER))
    except OSError:
        pass


def test_user_config():
    settings.load()
    data = project.load_user_config(PATH1)
    assert data == {}
    data = {'Foo': 'bar', 'Spam': 4, 'Eggs': [1, 2, 3]}
    project.save_user_config(PATH1, data)
    usd = project.load_user_config(PATH1)
    assert data == usd
    usd['Foo'] = 'BAR'
    project.save_user_config(PATH1, usd)
