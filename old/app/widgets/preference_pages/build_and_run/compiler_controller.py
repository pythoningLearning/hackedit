from PyQt5 import QtWidgets

from hackedit.api import compiler, plugins, system, utils
from hackedit.app import settings

from .base import BuildAndRunTabController


class CompilersController(BuildAndRunTabController):
    def __init__(self, ui):
        super().__init__(plugins.get_compiler_plugins, plugins.get_compiler_plugin_by_typename,
                         compiler.check_compiler, settings.load_compiler_configurations,
                         settings.save_compiler_configurations, settings.get_default_compiler,
                         settings.set_default_compiler, ui, ui.tree_compilers, ui.bt_add_compiler,
                         ui.bt_clone_compiler, ui.bt_delete_compiler, ui.bt_make_default_compiler,
                         ui.bt_check_compiler, ui.tab_compiler_settings, _('Check compilation'))

    def _get_updated_config(self):
        cfg = self.ui.stacked_compiler_options.current_widget.get_config()
        cfg.compiler = self.ui.edit_compiler.text().strip()
        env_vars = {}
        for i in range(self.ui.table_env_vars.rowCount()):
            k = self.ui.table_env_vars.item(i, 0).text()
            v = self.ui.table_env_vars.item(i, 1).text()
            env_vars[k] = v
        cfg.environment_variables = env_vars
        cfg.vcvarsall = self.ui.edit_vcvarsall.text()
        cfg.vcvarsall_arch = self.ui.combo_vcvarsall_arch.currentText().strip()
        return cfg

    def _display_config(self, config, widget_class, *args):
        if config is None:
            config = compiler.CompilerConfig()
        self.ui.edit_compiler.setText(config.compiler)
        self.ui.table_env_vars.clearContents()
        self.ui.table_env_vars.setRowCount(0)
        for k, v in sorted(config.environment_variables.items(), key=lambda x: x[0]):
            index = self.ui.table_env_vars.rowCount()
            self.ui.table_env_vars.insertRow(index)
            key = QtWidgets.QTableWidgetItem()
            key.setText(k)
            value = QtWidgets.QTableWidgetItem()
            value.setText(v)
            self.ui.table_env_vars.setItem(index, 0, key)
            self.ui.table_env_vars.setItem(index, 1, value)
        self.ui.edit_vcvarsall.setText(config.vcvarsall)
        self.ui.combo_vcvarsall_arch.setCurrentText(config.vcvarsall_arch)
        self.ui.group_msvc.setChecked(bool(config.vcvarsall))
        self.ui.group_msvc.setVisible(system.WINDOWS)
        # clear stacked widget used to display the custom editor default settings widget
        while self.ui.stacked_compiler_options.count():
            self.ui.stacked_compiler_options.removeWidget(self.ui.stacked_compiler_options.widget(0))
        self.ui.stacked_compiler_options.current_widget = None
        if widget_class:
            widget = widget_class(parent=self.ui.stacked_compiler_options)
            self.ui.stacked_compiler_options.addWidget(widget)
            self.ui.stacked_compiler_options.setCurrentIndex(0)
            self.ui.stacked_compiler_options.current_widget = widget
            widget.set_config(config)
            # trick to force qt to adjust the settings tab widget size
            index = self.ui.tab_compiler_settings.currentIndex()
            self.ui.tab_compiler_settings.setCurrentIndex(1)
            self.ui.tab_compiler_settings.setCurrentIndex(0)
            self.ui.tab_compiler_settings.setCurrentIndex(index)
        self._update_env_var_buttons()

    def _get_plugin_type_name(self, plugin):
        return plugin.get_compiler().type_name

    def _get_plugin_icon(self, plugin):
        return plugin.get_compiler_icon()

    def _get_status_icon_and_tooltip(self, plugin, config):
        comp = plugin.get_compiler()(config)
        comp.print_output = False
        icon, tooltip = self._get_success_status_meta(plugin.get_compiler_icon())
        try:
            compiler.check_compiler(comp)
        except utils.ProgramCheckFailedError as e:
            icon, tooltip = self._get_error_status_meta(e)
        return icon, tooltip

    def _get_version(self, plugin, config):
        comp = plugin.get_compiler()(config)
        comp.print_output = False
        return compiler.get_version(comp, include_all=False)

    def _get_program_runner(self, config, plugin):
        return plugin.get_compiler()(config, print_output=False)

    def _connect_slots(self):
        super()._connect_slots()
        self.ui.bt_select_compiler.clicked.connect(self._select_compiler)
        self.ui.bt_select_vcvarsall.clicked.connect(self._select_vcvarsall)
        self.ui.group_msvc.toggled.connect(self._on_msvc_support_togggled)
        self.ui.bt_add_env_var.clicked.connect(self._add_env_var)
        self.ui.bt_rm_env_var.clicked.connect(self._rm_env_var)
        self.ui.table_env_vars.itemSelectionChanged.connect(self._update_env_var_buttons)
        self.ui.table_env_vars.itemChanged.connect(self._update_current_config_meta)
        self.ui.edit_compiler.textChanged.connect(self._update_current_config_meta)

    def _select_compiler(self):
        status, path = self._select_path(self.ui.bt_select_compiler, _('Select compiler'),
                                         directory=self.ui.edit_compiler.text())
        if status and path:
            self.ui.edit_compiler.setText(path)

    def _on_msvc_support_togggled(self, state):
        if not state:
            self.ui.edit_vcvarsall.clear()

    def _add_env_var(self):
        utils.add_environment_var_to_table(self.ui.table_env_vars)
        self._update_current_config_meta()

    def _rm_env_var(self):
        utils.remove_selected_environment_var_from_table(self.ui.table_env_vars)
        self._update_current_config_meta()

    def _update_env_var_buttons(self):
        r = self.ui.table_env_vars.currentRow()
        self.ui.bt_rm_env_var.setEnabled(r != -1)

    def _select_vcvarsall(self):
        status, path = self._select_path(self.ui.bt_select_vcvarsall, _('Select vcvarsall.bat'),
                                         self.ui.edit_vcvarsall.text())
        if status and path:
            self.ui.edit_vcvarsall.setText(path)
