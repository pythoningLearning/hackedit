import os

import pytest
from hackedit.presentation.icon_provider import FileIconProvider, _get_mimetype_icon

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFileInfo


class TestFileIconProvider:
    @classmethod
    def setup_class(cls):
        cls.icon_provider = FileIconProvider()

    def test_mimetype_icon(self, mock):
        mock.spy(QIcon, 'fromTheme')
        icon = self.icon_provider.mimetype_icon('file.py', fallback=None)
        assert isinstance(icon, QIcon)
        QIcon.fromTheme.assert_called_once_with('text-x-python')

    def test_mimetype_icon_for_cmake(self, mock):
        mock.spy(QIcon, 'fromTheme')
        icon = self.icon_provider.mimetype_icon('CMakeLists.txt', fallback=None)
        assert isinstance(icon, QIcon)
        QIcon.fromTheme.assert_called_once_with('text-x-cmake')

    def test_mimetype_icon_for_invalid_mimetype_without_fallback(self, mock):
        mock.spy(QIcon, 'fromTheme')
        icon = self.icon_provider.mimetype_icon('file.xyz', fallback=None)
        assert isinstance(icon, QIcon)
        QIcon.fromTheme.assert_called_once_with('text-x-generic')

    def test_mimetype_icon_for_invalid_mimetype_with_fallback(self, mock):
        fallback = QIcon.fromTheme('edit-undo')
        mock.spy(QIcon, 'fromTheme')
        icon = self.icon_provider.mimetype_icon('file.xyz', fallback=fallback)
        assert isinstance(icon, QIcon)
        assert icon == fallback
        assert QIcon.fromTheme.call_count == 0

    @pytest.mark.parametrize('icon_type, icon_theme_name', [
        (FileIconProvider.Computer, None),
        (FileIconProvider.File, 'text-x-generic'),
        (FileIconProvider.Folder, 'folder')
    ])
    def test_icon_from_type(self, mock, icon_type, icon_theme_name):
        self.perform_icon_check(icon_theme_name, icon_type, mock)

    def perform_icon_check(self, expected, type_or_info_or_str, mock):
        _get_mimetype_icon.cache.clear()
        mock.spy(QIcon, 'fromTheme')
        icon = self.icon_provider.icon(type_or_info_or_str)
        assert isinstance(icon, QIcon)
        if expected:
            QIcon.fromTheme.assert_called_once_with(expected)
        else:
            assert QIcon.fromTheme.call_count == 0

    @pytest.mark.parametrize('file_info, icon_theme_name', [
        (QFileInfo(__file__), 'text-x-python'),
        (QFileInfo(os.path.dirname(__file__)), 'folder'),
    ])
    def test_icon_from_qfileinfo(self, mock, file_info, icon_theme_name):
        self.perform_icon_check(icon_theme_name, file_info, mock)

    @pytest.mark.parametrize('file_info, icon_theme_name', [
        (__file__, 'text-x-python'),
        (os.path.dirname(__file__), 'folder'),
    ])
    def test_icon_from_str(self, mock, file_info, icon_theme_name):
        self.perform_icon_check(icon_theme_name, file_info, mock)

    def test_icon_from_plugin(self, mock):
        self.perform_icon_check(None, "file.cbl", mock)
