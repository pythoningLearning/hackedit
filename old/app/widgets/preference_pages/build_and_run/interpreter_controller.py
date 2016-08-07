from PyQt5 import QtWidgets

from hackedit.api import interpreter, plugins, utils
from hackedit.app import settings

from .base import BuildAndRunTabController


class InterpreterController(BuildAndRunTabController):
    def __init__(self, ui):
        super().__init__(plugins.get_interpreter_plugins, plugins.get_interpreter_plugin_by_typename,
                         interpreter.check,
                         settings.load_interpreter_configurations, settings.save_interpreter_configurations,
                         settings.get_default_interpreter, settings.set_default_interpreter,
                         ui, ui.tree_interpreters, ui.bt_add_interpreter,
                         ui.bt_clone_interpreter, ui.bt_delete_interpreter, ui.bt_make_default_interpreter,
                         ui.bt_check_interpreter, ui.tab_widget_interpreter_settings, _('Check interpreter'))

    def _get_updated_config(self):
        cfg = self._current_config.copy()
        cfg.command = self.ui.edit_interpreter.text().strip()
        env_vars = {}
        for i in range(self.ui.table_interpreter_env_vars.rowCount()):
            k = self.ui.table_interpreter_env_vars.item(i, 0).text()
            v = self.ui.table_interpreter_env_vars.item(i, 1).text()
            print(env_vars, k, v)
            env_vars[k] = v
        cfg.environment_variables = env_vars
        return cfg

    def _display_config(self, config, widget_class, editable):
        if config is None:
            config = interpreter.InterpreterConfig()
        self.ui.edit_interpreter.setText(config.command)
        self._display_environment_vars(config)
        package_manager = self._get_package_manager(config)
        self._display_package_manager(package_manager)
        self._update_settings_tabs_state(editable, package_manager)
        self._update_env_var_buttons()

    def _display_environment_vars(self, config):
        self.ui.table_interpreter_env_vars.clearContents()
        self.ui.table_interpreter_env_vars.setRowCount(0)
        for k, v in sorted(config.environment_variables.items(), key=lambda x: x[0]):
            index = self.ui.table_interpreter_env_vars.rowCount()
            self.ui.table_interpreter_env_vars.insertRow(index)
            key = QtWidgets.QTableWidgetItem()
            key.setText(k)
            value = QtWidgets.QTableWidgetItem()
            value.setText(v)
            self.ui.table_interpreter_env_vars.setItem(index, 0, key)
            self.ui.table_interpreter_env_vars.setItem(index, 1, value)

    def _display_package_manager(self, package_manager):
        self.ui.package_manager_widget.set_package_manager(package_manager)

    def _update_settings_tabs_state(self, editable, package_manager):
        enable_package_manager = package_manager is not None
        self.ui.tab_widget_interpreter_settings.setEnabled(True)
        self.ui.tab_widget_interpreter_settings.setTabEnabled(1, enable_package_manager)
        if editable or not enable_package_manager:
            self.ui.tab_widget_interpreter_settings.setCurrentIndex(0)
        else:
            self.ui.tab_widget_interpreter_settings.setCurrentIndex(1)
        self.ui.tab_interpreter_setup.setEnabled(editable)

    def _get_package_manager(self, config):
        plugin = plugins.get_interpreter_plugin_by_typename(config.type_name)
        package_manager = None
        if plugin:
            package_manager = plugin.get_package_manager(config)
        return package_manager

    def _get_plugin_type_name(self, plugin):
        return plugin.get_interpreter_type_name()

    def _get_plugin_icon(self, plugin):
        return plugin.get_interpreter_icon()

    def _get_status_icon_and_tooltip(self, plugin, config):
        interpr = interpreter.Interpreter(config)
        interpr.print_output = False
        icon, tooltip = self._get_success_status_meta(self._get_plugin_icon(plugin))
        try:
            interpreter.check(interpr)
        except utils.ProgramCheckFailedError as e:
            icon, tooltip = self._get_error_status_meta(e)
        return icon, tooltip

    def _get_version(self, plugin, config):
        interpr = interpreter.Interpreter(config)
        interpr.print_output = False
        return interpreter.get_version(interpr, include_all=False)

    def _get_program_runner(self, config, *args):
        return interpreter.Interpreter(config, print_output=False)

    def _connect_slots(self):
        super()._connect_slots()
        self.ui.bt_select_interpreter.clicked.connect(self._select_interpreter)
        self.ui.bt_add_interpreter_env_var.clicked.connect(self._add_env_var)
        self.ui.bt_rm_interpreter_env_var.clicked.connect(self._rm_env_var)
        self.ui.table_interpreter_env_vars.itemSelectionChanged.connect(self._update_env_var_buttons)
        self.ui.table_interpreter_env_vars.itemChanged.connect(self._update_current_config_meta)
        self.ui.edit_interpreter.textChanged.connect(self._update_current_config_meta)

    def _select_interpreter(self):
        status, path = self._select_path(self.ui.bt_select_interpreter, _('Select interpreter'),
                                         directory=self.ui.edit_interpreter.text())
        if status and path:
            self.ui.edit_interpreter.setText(path)

    def _add_env_var(self):
        utils.add_environment_var_to_table(self.ui.table_interpreter_env_vars)
        self._update_current_config_meta()

    def _rm_env_var(self):
        utils.remove_selected_environment_var_from_table(self.ui.table_interpreter_env_vars)
        self._update_current_config_meta()

    def _update_env_var_buttons(self):
        r = self.ui.table_interpreter_env_vars.currentRow()
        self.ui.bt_rm_interpreter_env_var.setEnabled(r != -1)
