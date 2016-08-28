import locale

from hackedit.api import system
from pyqode.core.managers.file import FileManager
from pyqode.core.modes import CodeCompletionMode

from .section import SettingsSection


class EditorSettingsSection(SettingsSection):
    def __init__(self, qsettings):
        super().__init__('editor', qsettings)

    def get_defaults(self):
        return {
            'margin_position': 119,
            'tab_length': 4,
            'use_spaces': True,
            'center_on_scroll': True,
            'highlight_caret_scope': False,
            'highlight_caret_line': True,
            'highlight_parentheses': True,
            'convert_tabs': True,
            'clean_trailing_whitespaces': True,
            'restore_cursor': True,
            'safe_save': True,
            'default_encoding': locale.getpreferredencoding(),
            'eol_convention': FileManager.EOL.System,
            'autodetect_eol': True,
            'code_completion_trigger_len': 0,
            'code_completion_filter_mode': CodeCompletionMode.FILTER_FUZZY,
            'code_completion_show_tooltips': False,
            'code_completion_case_sensitive': False,
            'show_line_numbers_panel': True,
            'show_folding_panel': True,
            'show_errors_panel': True,
            'show_global_panel': True,
            'enable_text_wrapping': False,
            'show_right_margin': True,
            'auto_indent': True,
            'auto_complete': True,
            'backspace_unindents': True,
            'color_scheme': 'aube' if not system.is_dark_theme() else 'crepuscule',
            'font': 'Hack',
            'font_size': 10,
            'show_whitespaces': False
        }
