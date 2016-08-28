import locale
import logging

import pytest
from PyQt5 import QtCore
from hackedit.api import system
from hackedit.api.constants import OpenMode
from hackedit.application.services.settings.editor import EditorSettingsSection
from hackedit.application.services.settings.environment import EnvironmentSettingsSection
from hackedit.application.services.settings.section import SettingsSection
from hackedit.containers import Services, View
from pyqode.core.managers import FileManager
from pyqode.core.modes import CodeCompletionMode


class MySection(SettingsSection):
    INITIAL_BOOL_VALUE = True
    INITIAL_INT_VALUE = 4
    INITIAL_STR_VALUE = 'spam'

    def get_defaults(self):
        return {
            'test_bool': self.INITIAL_BOOL_VALUE,
            'test_int': self.INITIAL_INT_VALUE,
            'test_str': self.INITIAL_STR_VALUE
        }


class TestSettingsSection:
    @classmethod
    def setup_class(cls):
        cls.section = MySection('Test', QtCore.QSettings())

    def test_add_bool_property(self):
        assert isinstance(self.section.test_bool, bool)
        assert self.section.test_bool == MySection.INITIAL_BOOL_VALUE

    def test_change_bool_property(self):
        self.section.test_bool = False
        assert self.section.test_bool is False
        self.section.test_bool = MySection.INITIAL_BOOL_VALUE

    def test_add_int_property(self):
        assert isinstance(self.section.test_int, int)
        assert self.section.test_int == MySection.INITIAL_INT_VALUE

    def test_change_int_property(self):
        self.section.test_int = 5
        assert self.section.test_int == 5
        self.section.test_int = MySection.INITIAL_INT_VALUE

    def test_add_string_property(self):
        assert isinstance(self.section.test_str, str)
        assert self.section.test_str == MySection.INITIAL_STR_VALUE

    def test_change_string_property(self):
        self.section.test_str = 'eggs'
        assert self.section.test_str == 'eggs'
        self.section.test_str = MySection.INITIAL_STR_VALUE

    def test_add_invalid_property(self):
        with pytest.raises(ValueError):
            self.section.add_property("test", None)
        with pytest.raises(ValueError):
            self.section.add_property('test', TestSettingsBase())

    def test_restore_defaults(self):
        self.section.test_int = 1000
        self.section.restore_defaults()
        assert self.section.test_int == MySection.INITIAL_INT_VALUE


class TestSettingsBase:
    @classmethod
    def setup_class(cls):
        cls.settings = Services.settings()


class TestSettings(TestSettingsBase):
    def test_file_name(self):
        assert 'HackEdit-Tests' in self.settings._qsettings.fileName()

    def test_environment_section_exists(self):
        assert self.settings.environment is not None

    def test_clear(self):
        settings = self.settings
        settings._qsettings.setValue('testFlag', '1')
        settings.clear()
        assert settings._qsettings.value('testFlag', '0') == '0'

    def test_add_section(self):
        TestSettingsSection.setup_class()
        self.settings.add_section('test', TestSettingsSection.section)
        assert 'test' in self.settings.sections
        assert hasattr(self.settings, 'test')
        assert hasattr(self.settings.test, 'test_bool')


class TestEnvironmentSettings(TestSettingsBase):
    def test_settings_has_environment_section(self):
        assert isinstance(self.settings.environment, EnvironmentSettingsSection)

    @pytest.mark.parametrize('name, default, opposite', [
        ('show_menu', False, True),
        ('widescreen_layout', EnvironmentSettingsSection.is_wide_screen(), not EnvironmentSettingsSection.is_wide_screen()),
        ('show_tray_icon', False, True),
        ('icon_theme', View.icons().system_icon_theme(), 'unknown'),
        ('dark_theme', False, True),
        ('toolbar_icon_size', 22, 24),
        ('restore_session', True, False),
        ('file_manager_command', EnvironmentSettingsSection.get_default_file_manager_command(), 'cmd'),
        ('cmd_open_folder_in_terminal', system.get_cmd_open_folder_in_terminal(), 'cmd'),
        ('cmd_run_command_in_terminal', system.get_cmd_run_command_in_terminal(), 'cmd'),
        ('locale', 'default', 'fr'),
        ('use_default_browser', 1 if not system.DARWIN else 0, 0 if not system.DARWIN else 1),
        ('custom_browser_command', EnvironmentSettingsSection.get_default_browser_commands(), 'cmd'),
        ('show_splashscreen', True, False),
        ('automatically_check_for_updates', EnvironmentSettingsSection.get_default_automatically_check_for_updates(),
         not EnvironmentSettingsSection.get_default_automatically_check_for_updates()),
        ('restore_last_window', False, True),
        ('confirm_application_exit', True, True),
        ('open_mode', OpenMode.ASK_EACH_TIME, OpenMode.NEW_WINDOW),
        ('ignored_patterns', EnvironmentSettingsSection.IGNORE_PATTERNS_STR, ''),
        ('show_notification_in_sytem_tray', True, False),
        ('auto_open_info_notification', True, False),
        ('auto_open_warning_notification', True, False),
        ('auto_open_error_notification', True, False),
        ('log_level', logging.INFO, logging.DEBUG),
        ('indexing_enabled', True, False)
    ])
    def test_properties(self, mocker, name, default, opposite):
        self.settings.environment.restore_defaults()
        assert hasattr(self.settings.environment, name)

        mocker.spy(self.settings._qsettings, 'value')
        mocker.spy(self.settings._qsettings, 'setValue')
        assert getattr(self.settings.environment, name) == default

        self.settings._qsettings.value.assert_called_once_with('env/' + name, default)
        setattr(self.settings.environment, name, opposite)
        self.settings._qsettings.setValue.assert_called_once_with('env/' + name, opposite)
        assert getattr(self.settings.environment, name) == opposite


class TestEditorSettings(TestSettingsBase):
    def test_settings_has_environment_section(self):
        assert isinstance(self.settings.editor, EditorSettingsSection)

    @pytest.mark.parametrize('name, default, opposite', [
        ('margin_position', 119, 79),
        ('tab_length', 4, 8),
        ('use_spaces', True, False),
        ('center_on_scroll', True, False),
        ('highlight_caret_scope', False, True),
        ('highlight_caret_line', True, False),
        ('highlight_parentheses', True, False),
        ('convert_tabs', True, False),
        ('clean_trailing_whitespaces', True, False),
        ('restore_cursor', True, False),
        ('safe_save', True, False),
        ('default_encoding', locale.getpreferredencoding(), 'ascii'),
        ('eol_convention', FileManager.EOL.System, FileManager.EOL.Linux),
        ('autodetect_eol', True, False),
        ('code_completion_trigger_len', 0, 3),
        ('code_completion_filter_mode', CodeCompletionMode.FILTER_FUZZY, CodeCompletionMode.FILTER_PREFIX),
        ('code_completion_show_tooltips', False, True),
        ('code_completion_case_sensitive', False, True),
        ('show_line_numbers_panel', True, False),
        ('show_folding_panel', True, False),
        ('show_errors_panel', True, False),
        ('show_global_panel', True, False),
        ('enable_text_wrapping', False, True),
        ('show_right_margin', True, False),
        ('auto_indent', True, False),
        ('auto_complete', True, False),
        ('backspace_unindents', True, False),
        ('color_scheme', 'aube' if not system.is_dark_theme() else 'crepuscule', 'monokai'),
        ('font', 'Hack', 'monospace'),
        ('font_size', 10, 12),
        ('show_whitespaces', False, True)
    ])
    def test_properties(self, mocker, name, default, opposite):
        self.settings.editor.restore_defaults()
        assert hasattr(self.settings.editor, name)

        mocker.spy(self.settings._qsettings, 'value')
        mocker.spy(self.settings._qsettings, 'setValue')
        assert getattr(self.settings.editor, name) == default

        self.settings._qsettings.value.assert_called_once_with('editor/' + name, default)
        setattr(self.settings.editor, name, opposite)
        self.settings._qsettings.setValue.assert_called_once_with('editor/' + name, opposite)
        assert getattr(self.settings.editor, name) == opposite
