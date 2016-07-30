from hackedit.api import pre_compiler, plugins, utils
from hackedit.app import settings

from .base import BuildAndRunTabController


class PreCompilersController(BuildAndRunTabController):
    def __init__(self, ui):
        """
        :type ui: hackedit.app.forms.settings_page_build_and_run_ui.Ui_Form
        """
        super().__init__(plugins.get_pre_compiler_plugins, plugins.get_pre_compiler_plugin,
                         pre_compiler.check_pre_compiler, settings.load_pre_compiler_configurations,
                         settings.save_pre_compiler_configurations,  settings.get_default_pre_compiler,
                         settings.set_default_pre_compiler, ui, ui.tree_pre_compilers, ui.bt_add_pre_compiler,
                         ui.bt_clone_pre_compiler, ui.bt_delete_pre_compiler, ui.bt_make_default_pre_compiler,
                         ui.bt_check_pre_compiler, ui.group_pre_compiler_settings, _('Check pre-compilation'))

    def _get_updated_config(self):
        cfg = self._current_config.copy()
        cfg.name = self._current_config.name
        cfg.path = self.ui.edit_pre_compiler_path.text().strip()
        cfg.associated_extensions = [t for t in self.ui.edit_pre_compiler_extensions.text().strip().split(';') if t]
        cfg.flags = [t for t in self.ui.edit_pre_compiler_flags.text().strip().split(' ') if t]
        cfg.command_pattern = self.ui.edit_command_pattern.text().strip()
        cfg.output_pattern = self.ui.edit_pre_compiler_output_pattern.text().strip()
        return cfg

    def _display_config(self, config, *args):
        if config is None:
            config = pre_compiler.PreCompilerConfig()
        self.ui.edit_pre_compiler_path.setText(config.path)
        self.ui.edit_command_pattern.setText(config.command_pattern)
        self.ui.edit_command_pattern.setVisible(config.command_pattern_editable)
        self.ui.lbl_command_pattern.setVisible(config.command_pattern_editable)
        self.ui.edit_pre_compiler_extensions.setText(';'.join(config.associated_extensions))
        self.ui.edit_pre_compiler_flags.setText(' '.join(config.flags))
        self.ui.edit_pre_compiler_output_pattern.setText(config.output_pattern)

    def _get_plugin_type_name(self, plugin):
        return plugin.get_pre_compiler_type_name()

    def _get_plugin_icon(self, plugin):
        return plugin.get_pre_compiler_icon()

    def _get_status_icon_and_tooltip(self, plugin, config):
        precompiler = pre_compiler.PreCompiler(config, print_output=False)
        icon, tooltip = self._get_success_status_meta(plugin.get_pre_compiler_icon())
        try:
            pre_compiler.check_pre_compiler(precompiler)
        except utils.ProgramCheckFailedError as e:
            icon, tooltip = self._get_error_status_meta(e)
        return icon, tooltip

    def _get_version(self, _, config):
        precompiler = pre_compiler.PreCompiler(config, print_output=False)
        return pre_compiler.get_version(precompiler, include_all=False)

    def _get_program_runner(self, config, *args):
        return pre_compiler.PreCompiler(config)

    def _connect_slots(self):
        super()._connect_slots()
        self.ui.bt_select_pre_compiler_path.clicked.connect(self._select_pre_compiler_path)
        self.ui.edit_pre_compiler_path.textChanged.connect(self._update_current_config_meta)
        self.ui.edit_pre_compiler_extensions.textChanged.connect(self._update_current_config_meta)
        self.ui.edit_pre_compiler_output_pattern.textChanged.connect(self._update_current_config_meta)

    def _select_pre_compiler_path(self):
        status, path = self._select_path(self.ui.bt_select_pre_compiler_path, _('Select pre-compiler'),
                                         directory=self.ui.edit_pre_compiler_path.text())
        if status and path:
            self.ui.edit_pre_compiler_path.setText(path)
