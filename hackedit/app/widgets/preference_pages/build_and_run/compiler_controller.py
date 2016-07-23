from PyQt5 import QtCore, QtWidgets

from hackedit.api import compiler, plugins, system, utils
from hackedit.app import settings
from hackedit.app.dialogs import dlg_check_compiler


ITEM_AUTO_DETECTED = 0
ITEM_MANUAL = 1


class CompilersController(QtCore.QObject):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self._current_config = None
        self._current_config_editable = False
        self._connect_slots()

    def _connect_slots(self):
        self.ui.tree_compilers.itemSelectionChanged.connect(self._update_compiler_config)
        self.ui.bt_clone_compiler.clicked.connect(self._clone_compiler)
        self.ui.bt_delete_compiler.clicked.connect(self._delete_compiler)
        self.ui.bt_check_compiler.clicked.connect(self._check_compiler)
        self.ui.bt_select_compiler.clicked.connect(self._select_compiler)
        self.ui.bt_select_vcvarsall.clicked.connect(self._select_vcvarsall)
        self.ui.group_msvc.toggled.connect(self._on_msvc_support_togggled)
        self.ui.bt_add_env_var.clicked.connect(self._add_env_var)
        self.ui.bt_rm_env_var.clicked.connect(self._rm_env_var)
        self.ui.table_env_vars.itemSelectionChanged.connect(self._update_env_var_buttons)

    def reset(self):
        self.names = set()
        mnu_compiler_types = QtWidgets.QMenu()
        self.ui.bt_add_compiler.setMenu(mnu_compiler_types)
        # fill compiler tree widget
        for item_type in [ITEM_AUTO_DETECTED, ITEM_MANUAL]:
            item = self.ui.tree_compilers.topLevelItem(item_type)
            while item.childCount():
                item.removeChild(item.child(0))
        # add autodetected confis
        for plugin in plugins.get_compiler_plugins():
            action = mnu_compiler_types.addAction(plugin.get_compiler().type_name)
            action.triggered.connect(self._add_compiler)
            for config in plugin.get_auto_detected_configs():
                self._add_config_item(config, item_type=ITEM_AUTO_DETECTED, plugin=plugin)
        self.ui.tree_compilers.setCurrentItem(None)
        # add user defined configuration
        self.user_configs = settings.load_compiler_configurations()
        for key, value in sorted(self.user_configs.items(), key=lambda x: x[0]):
            self._add_config_item(value)
        self.ui.tree_compilers.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.tree_compilers.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ui.tree_compilers.expandAll()
        self._update_compiler_config()

    def restore_defaults(self):
        settings.save_compiler_configurations({})

    def apply(self):
        self._save_current_config()
        settings.save_compiler_configurations(self.user_configs)

    def _add_config_item(self, config, item_type=ITEM_MANUAL, plugin=None):
        parent = self.ui.tree_compilers.topLevelItem(item_type)
        if plugin is None:
            plugin = plugins.get_compiler_plugin(config.type_name)
        if plugin is None:
            return
        icon = plugin.get_compiler_icon()
        item = QtWidgets.QTreeWidgetItem()
        item.setIcon(0, icon)
        item.setText(0, config.name)
        item.setText(1, config.type_name)
        item.setData(0, QtCore.Qt.UserRole, plugin.get_compiler_config_widget())
        item.setData(1, QtCore.Qt.UserRole, config)
        self.names.add(config.name)
        parent.addChild(item)
        return item

    def _add_compiler(self):
        compiler_type_name = self.sender().text()
        ok, name = self._get_name(compiler_type_name)
        if not ok:
            return
        ok, path = self._select_compiler_path()
        if not ok:
            return
        plugin = plugins.get_compiler_plugin(compiler_type_name)
        config = plugin.create_new_configuration(name, path)
        self.user_configs[config.name] = config
        item = self._add_config_item(config, plugin=plugin)
        item.setSelected(True)
        self.ui.tree_compilers.setCurrentItem(item)
        self._update_compiler_config()

    def _clone_compiler(self):
        cloned_config = self._current_config.copy()
        plugin = plugins.get_compiler_plugin(cloned_config.type_name)
        ok, name = self._get_name(cloned_config.type_name)
        if not ok:
            return
        assert isinstance(cloned_config, compiler.CompilerConfig)
        cloned_config.name = name
        self.user_configs[name] = cloned_config
        item = self._add_config_item(cloned_config, plugin=plugin)
        item.setSelected(True)
        self.ui.tree_compilers.setCurrentItem(item)
        self._update_compiler_config()

    def _delete_compiler(self):
        answer = QtWidgets.QMessageBox.question(
            self.ui.bt_delete_compiler, "Remove compiler",
            'Are you sure you want to remove the compiler configuration %r' % self._current_config.name)
        if answer == QtWidgets.QMessageBox.No:
            return
        item = self.ui.tree_compilers.currentItem()
        self.user_configs.pop(self._current_config.name)
        self._current_config = None
        parent = item.parent()
        parent.removeChild(item)
        self._update_compiler_config()

    def _check_compiler(self):
        cfg = self._get_updated_config()
        plugin = plugins.get_compiler_plugin(cfg.type_name)
        compiler = plugin.get_compiler()(cfg, print_output=False)
        dlg_check_compiler.DlgCheckCompiler.check(self.ui.bt_check_compiler, compiler)

    def _select_compiler(self):
        status, path = self._select_compiler_path()
        if status:
            self.ui.edit_compiler.setText(path)

    def _on_msvc_support_togggled(self, state):
        if not state:
            self.ui.edit_vcvarsall.clear()

    def _add_env_var(self):
        utils.add_environment_var_to_table(self.ui.table_env_vars)

    def _rm_env_var(self):
        utils.remove_selected_environment_var_from_table(self.ui.table_env_vars)

    def _update_env_var_buttons(self):
        r = self.ui.table_env_vars.currentRow()
        print(r)
        self.ui.bt_rm_env_var.setEnabled(r != -1)

    def _select_vcvarsall(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.ui.bt_select_vcvarsall, 'Select vcvarsall.bat', 'C:\\')
        if path:
            self.ui.edit_vcvarsall.setText(path)

    def _select_compiler_path(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.ui.bt_add_compiler, 'Select compiler', self.ui.edit_compiler.text())
        if path:
            return True, path
        return False, ''

    def _get_name(self, compiler_type_name):
        name = ''
        while not self._check_name(name):
            if name:
                QtWidgets.QMessageBox.warning(self.ui.bt_add_compiler, 'Invalid name',
                                              'The name %r is already used for another configuration' % name)
            name, ok = QtWidgets.QInputDialog.getText(self.ui.bt_add_compiler,
                                                      'Add new compiler', 'Name:', QtWidgets.QLineEdit.Normal,
                                                      self._suggest_name(compiler_type_name))
            if not ok:
                return False, ''
        return True, name

    def _suggest_name(self, name):
        i = 1
        original = name
        while not self._check_name(name):
            name = original + '_%d' % (i + 1)
            i += 1
        return name

    def _check_name(self, name):
        return name != '' and name not in self.names

    def _save_current_config(self):
        if self._current_config and self._current_config_editable:
            cfg = self._get_updated_config()
            cfg.name = self._current_config.name

            # save config changes in temporary map
            self.user_configs[self._current_config.name] = cfg

            # update associate item data to keep in sync
            manual = self.ui.tree_compilers.topLevelItem(ITEM_MANUAL)
            for index in range(manual.childCount()):
                item = manual.child(index)
                if item.text(0) == cfg.name:
                    item.setData(1, QtCore.Qt.UserRole, cfg)

    def _get_updated_config(self):
        cfg = self.ui.stacked_compiler_options.current_widget.get_config()
        assert isinstance(cfg, compiler.CompilerConfig)
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

    def _update_compiler_config(self, *args):
        self._save_current_config()
        current_item = self.ui.tree_compilers.currentItem()
        if current_item is None or current_item.parent() is None:
            # no item selected or top level item
            self.ui.tab_compiler_settings.hide()
            editable = False
            clonable = False
            self._current_config = None
            self._display_config(None, None)
        else:
            clonable = True
            self.ui.tab_compiler_settings.show()
            config = current_item.data(1, QtCore.Qt.UserRole)
            widget_class = current_item.data(0, QtCore.Qt.UserRole)
            self._display_config(config, widget_class)
            # prevent user from editing an auto detected configuration
            parent_item = current_item.parent()
            parent_item_index = self.ui.tree_compilers.indexOfTopLevelItem(parent_item)
            editable = parent_item_index != ITEM_AUTO_DETECTED
            # self._current_config = config if editable else None
            self._current_config_editable = editable
            self._current_config = config
        self.ui.tab_default_options.setEnabled(editable)
        self.ui.tab_compiler_setup.setEnabled(editable)
        self.ui.bt_delete_compiler.setEnabled(editable)
        self.ui.bt_check_compiler.setEnabled(clonable)
        self.ui.bt_clone_compiler.setEnabled(clonable)

    def _display_config(self, config, widget_class):
        if config is None:
            config = compiler.CompilerConfig()
        else:
            assert isinstance(config, compiler.CompilerConfig)
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
            self.ui.tab_compiler_settings.setCurrentIndex(1)
            self.ui.tab_compiler_settings.setCurrentIndex(0)
        self._update_env_var_buttons()