from hackedit.api import special_icons
from hackedit.api.widgets import PreferencePage
from hackedit.app.forms import settings_page_build_and_run_ui

from .compiler_controller import CompilersController
from .pre_compiler_controller import PreCompilersController


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
        self.controllers = [
            CompilersController(self.ui),
            PreCompilersController(self.ui)
        ]
        self.ui.tab_categories.setCurrentIndex(0)

    def reset(self):
        for controller in self.controllers:
            controller.reset()

    def restore_defaults(self):
        for controller in self.controllers:
            controller.restore_defaults()

    def save(self):
        for controller in self.controllers:
            controller.save()
