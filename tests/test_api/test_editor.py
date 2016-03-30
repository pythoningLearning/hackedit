from .test_window import FILE1, FILE2, PROJ_PATH
from hackedit.api import editor
import pytest_hackedit


def test_open_file(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    assert len(editor.get_all_paths()) == 0
    editor.open_file(FILE1)
    assert len(editor.get_all_paths()) == 1
    editor.open_file(FILE2)
    assert len(editor.get_all_paths()) == 2
    pytest_hackedit.close_main_window(w)


def test_get_current_editor(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    assert editor.get_current_editor() is None
    editor.open_file(FILE1)
    assert editor.get_current_editor() is not None
    pytest_hackedit.close_main_window(w)


def test_get_current_path(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    assert editor.get_current_path() is None
    editor.open_file(FILE1)
    assert editor.get_current_path() == FILE1
    pytest_hackedit.close_main_window(w)


def test_get_all_paths(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    editor.open_file(FILE1)
    editor.open_file(FILE2)
    assert len(editor.get_all_editors()) == 2
    assert editor.get_all_paths() == [FILE1, FILE2]
    pytest_hackedit.close_main_window(w)


def test_save_current_editor(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    editor.open_file(FILE1)
    editor.save_current_editor()
    pytest_hackedit.close_main_window(w)


def test_save_all_editors(qtbot):
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    editor.open_file(FILE1)
    editor.open_file(FILE2)
    editor.save_all_editors()
    pytest_hackedit.close_main_window(w)
