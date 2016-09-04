import pytest
from PyQt5.QtGui import QIcon
from hackedit.containers import View


class TestIcons:
    @classmethod
    def setup_class(cls):
        cls.icons = View.icons()

    def test_icon_themes_not_empty(self):
        assert len(self.icons.icon_themes()) > 0

    @pytest.mark.parametrize('method_name, argument, use_theme', [
        ('configure_icon', False, True),
        ('configure_icon', False, False),
        ('configure_icon', True, True),
        ('configure_icon', True, False),
        ('configure_icon', None, True),
        ('configure_icon', None, False),

        ('run_icon', None, True),
        ('run_icon', None, False),

        ('run_debug_icon', None, True),
        ('run_debug_icon', None, False),

        ('class_icon', None, True),
        ('class_icon', None, False),

        ('variable_icon', None, True),
        ('variable_icon', None, False),

        ('function_icon', None, True),
        ('function_icon', None, False),

        ('namespace_icon', None, True),
        ('namespace_icon', None, False),

        ('object_locked', None, True),
        ('object_locked', None, False),

        ('object_unlocked', None, True),
        ('object_unlocked', None, False),

        ('debug_step_into_icon', None, True),
        ('debug_step_into_icon', None, False),

        ('debug_step_over_icon', None, True),
        ('debug_step_over_icon', None, False),

        ('debug_step_out_icon', None, True),
        ('debug_step_out_icon', None, False),

        ('breakpoint_icon', None, True),
        ('breakpoint_icon', None, False),

        ('edit_breakpoints_icon', None, True),
        ('edit_breakpoints_icon', None, False),

        ('run_build', None, True),
        ('run_build', None, False),

        ('build_clean', None, True),
        ('build_clean', None, False),

        ('app_menu', None, True),
        ('app_menu', None, False),
    ])
    def test_get_xxx_icon(self, mock, method_name, argument, use_theme):
        mock.patch('PyQt5.QtGui.QIcon.hasThemeIcon')
        QIcon.hasThemeIcon.return_value = use_theme
        method = getattr(self.icons, method_name)
        if argument:
            icon = method(argument)
        else:
            icon = method()
        assert isinstance(icon, QIcon)

