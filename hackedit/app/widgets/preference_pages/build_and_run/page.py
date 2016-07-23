from hackedit.api import special_icons
from hackedit.api.widgets import PreferencePage
from hackedit.app.forms import settings_page_build_and_run_ui

from .compiler_controller import CompilersController


ITEM_AUTO_DETECTED = 0
ITEM_MANUAL = 1


class BuildAndRun(PreferencePage):
    can_reset = True
    can_restore_defaults = True
    can_apply = True

    def __init__(self):
        super().__init__(_('Build And Run'), icon=special_icons.run_build())
        self.ui = settings_page_build_and_run_ui.Ui_Form()
        self.ui.setupUi(self)
        self.compilers = CompilersController(self.ui)
        self.ui.tab_categories.setCurrentIndex(0)

    def reset(self):
        self.compilers.reset()

    def restore_defaults(self):
        self.compilers.restore_defaults()

    def save(self):
        self.compilers.apply()
