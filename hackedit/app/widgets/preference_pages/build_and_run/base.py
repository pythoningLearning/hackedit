from PyQt5 import QtCore, QtGui, QtWidgets
from hackedit.app.dialogs import dlg_check_compiler


ITEM_AUTO_DETECTED = 0
ITEM_MANUAL = 1

COL_NAME = 0
COL_TYPE = 1
COL_VERSION = 2
COL_DEFAULT = 3

DATA_COL_WIDGET = COL_NAME
DATA_COL_CONFIG = COL_TYPE
DATA_COL_PLUGIN = COL_VERSION


class BuildAndRunTabController(QtCore.QObject):
    def __init__(self, fct_get_plugins, fct_get_plugin_by_typename, fct_check,
                 fct_settings_load, fct_settings_save, fct_settings_get_default,
                 fct_settings_set_default, ui, tree, bt_add, bt_clone, bt_remove, bt_make_default, bt_check,
                 settings_widget, bt_check_message):
        super().__init__()
        self.bt_check_message = bt_check_message
        self.fct_check = fct_check
        self.ui = ui
        self.settings_widget = settings_widget
        self.fct_get_plugins = fct_get_plugins
        self.fct_get_plugin_by_typename = fct_get_plugin_by_typename
        self.fct_settings_get_default = fct_settings_get_default
        self.fct_settings_load = fct_settings_load
        self.fct_settings_save = fct_settings_save
        self.fct_settings_get_default = fct_settings_get_default
        self.fct_settings_set_default = fct_settings_set_default
        self.tree = tree
        self.bt_add = bt_add
        self.bt_remove = bt_remove
        self.bt_clone = bt_clone
        self.bt_make_default = bt_make_default
        self.bt_check = bt_check
        self.names = set()
        self._config_to_select = ''
        self._item_to_select = None
        self._updating_config = False
        self._loading = False
        self._current_config = None
        self._current_config_editable = False
        self._connect_slots()

    def reset(self):
        self._current_config = None
        self._loading = True
        self.names = set()
        mnu_add = QtWidgets.QMenu()
        self.bt_add.setMenu(mnu_add)
        self._clear_tree()
        for plugin in self.fct_get_plugins():
            action = mnu_add.addAction(self._get_plugin_type_name(plugin))
            action.setIcon(self._get_plugin_icon(plugin))
            action.triggered.connect(self._add_config)
            self._add_config_items(plugin.get_auto_detected_configs(), ITEM_AUTO_DETECTED)
        self.user_configs = self.fct_settings_load()
        self._add_config_items(sorted(self.user_configs.values(), key=lambda x: x.name), ITEM_MANUAL)
        self._setup_tree()
        self._loading = False
        self._update_config()

    def restore_defaults(self):
        self.fct_settings_save({})

    def save(self):
        self._save_current_config()
        self.fct_settings_save(self.user_configs)

    def _get_updated_config(self):
        raise NotImplementedError()

    def _display_config(self, config, widget_class):
        raise NotImplementedError()

    def _get_status_icon_and_tooltip(self, plugin, config):
        raise NotImplementedError()

    def _get_version(self, plugin, config):
        raise NotImplementedError()

    def _get_plugin_type_name(self, plugin):
        raise NotImplementedError()

    def _get_plugin_icon(self, plugin):
        raise NotImplementedError()

    def _get_program_runner(self, config, plugin):
        raise NotImplementedError()

    def _connect_slots(self):
        self.tree.itemSelectionChanged.connect(self._update_config)
        self.tree.itemClicked.connect(self._update_config)
        self.bt_clone.clicked.connect(self._clone_config)
        self.bt_remove.clicked.connect(self._remove_config)
        self.bt_make_default.clicked.connect(self._make_default)
        self.bt_check.clicked.connect(self._check_config)

    def _update_config(self, *args):
        if self._loading:
            return
        self._updating_config = True
        self._save_current_config()
        current_item = self.tree.currentItem()
        if current_item is None:
            return
        config = current_item.data(DATA_COL_CONFIG, QtCore.Qt.UserRole)
        widget_class = current_item.data(DATA_COL_WIDGET, QtCore.Qt.UserRole)
        if current_item is None or current_item.parent() is None:
            # no item selected or top level item
            self.settings_widget.hide()
            editable = False
            clonable = False
            self._current_config = None
            self._current_config_editable = None
            self._display_config(None, None)
        else:
            clonable = True
            self.settings_widget.show()
            self._display_config(config, widget_class)
            parent_item = current_item.parent()
            parent_item_index = self.tree.indexOfTopLevelItem(parent_item)
            editable = parent_item_index != ITEM_AUTO_DETECTED
            self._current_config_editable = editable
            self._current_config = config
            self._config_to_select = config.name
        self.settings_widget.setEnabled(editable)
        self.bt_remove.setEnabled(editable)
        self.bt_check.setEnabled(clonable)
        self.bt_clone.setEnabled(clonable)
        self.bt_make_default.setEnabled(clonable)
        self._updating_config = False

    def _save_current_config(self):
        if self._current_config and self._current_config_editable:
            cfg = self._get_updated_config()
            cfg.name = self._current_config.name

            # save config changes in temporary map
            self.user_configs[self._current_config.name] = cfg

            # update associate item data to keep in sync
            manual = self.tree.topLevelItem(ITEM_MANUAL)
            for index in range(manual.childCount()):
                item = manual.child(index)
                if item.text(0) == cfg.name:
                    item.setData(DATA_COL_CONFIG, QtCore.Qt.UserRole, cfg)

    def _add_config(self):
        type_name = self.sender().text()
        ok, name = self._get_name(self.bt_add, type_name)
        if not ok:
            return
        plugin = self.fct_get_plugin_by_typename(type_name)
        config = plugin.create_new_configuration_with_dialog(self.bt_add, name)
        if config is None:
            return
        self.user_configs[config.name] = config
        item = self._add_config_item(config, ITEM_MANUAL)
        item.setSelected(True)
        self.tree.setCurrentItem(item)
        self._update_config()
        self.names.add(name)

    def _clone_config(self):
        cloned_config = self._current_config.copy()
        ok, name = self._get_name(self.bt_clone, cloned_config.type_name)
        if not ok:
            return
        cloned_config.name = name
        self.user_configs[name] = cloned_config
        item = self._add_config_item(cloned_config, ITEM_MANUAL)
        item.setSelected(True)
        self.tree.setCurrentItem(item)
        self._update_config()

    def _remove_config(self):
        answer = QtWidgets.QMessageBox.question(
            self.bt_remove, "Remove configuration?",
            'Are you sure you want to remove the selected configuration: %r?' % self._current_config.name)
        if answer == QtWidgets.QMessageBox.No:
            return
        item = self.tree.currentItem()
        self.user_configs.pop(self._current_config.name)
        try:
            self.names.remove(self._current_config.name)
        except ValueError:
            pass
        self._current_config = None
        parent = item.parent()
        parent.removeChild(item)
        self._update_config()

    def _make_default(self):
        name = self.tree.currentItem().text(COL_NAME)
        config = self.tree.currentItem().data(DATA_COL_CONFIG, QtCore.Qt.UserRole)
        self.fct_settings_set_default(config.type_name, name)
        self._config_to_select = name
        self.save()
        self.reset()

    def _check_config(self):
        config = self._get_updated_config()
        plugin = self.fct_get_plugin_by_typename(config.type_name)
        program_runner = self._get_program_runner(config, plugin)
        dlg_check_compiler.DlgCheckCompiler.check(
            self.bt_check, program_runner, bt_check_message=self.bt_check_message, check_function=self.fct_check)

    def _setup_tree(self):
        self.tree.header().setStretchLastSection(False)
        self.tree.header().setDefaultSectionSize(16)
        self.tree.header().setSectionResizeMode(COL_NAME, QtWidgets.QHeaderView.Stretch)
        self.tree.header().setSectionResizeMode(COL_TYPE, QtWidgets.QHeaderView.ResizeToContents)
        self.tree.header().setSectionResizeMode(COL_VERSION, QtWidgets.QHeaderView.ResizeToContents)
        self.tree.header().setSectionResizeMode(COL_DEFAULT, QtWidgets.QHeaderView.ResizeToContents)
        self.tree.header().setSectionResizeMode(COL_DEFAULT, QtWidgets.QHeaderView.ResizeToContents)
        self.tree.setHeaderLabels(['Name', 'Type', 'Version', ''])
        self.tree.expandAll()
        if self._item_to_select:
            self.tree.setCurrentItem(self._item_to_select)

    def _add_config_items(self, configs, item_type):
        for config in configs:
            type_name = config.type_name
            default = self.fct_settings_get_default(type_name)
            if default is None:
                default = config.name
                self.fct_settings_set_default(type_name, config.name)
            is_default = False
            if default == config.name:
                is_default = True
            if not self._config_to_select:
                self._config_to_select = config.name
            select = False
            if self._config_to_select == config.name:
                select = True
            self._add_config_item(config, item_type, is_default=is_default, select=select)

    def _add_config_item(self, config, item_type, is_default=False, select=False):
        parent = self.tree.topLevelItem(item_type)
        try:
            plugin = self.fct_get_plugin_by_typename(config.type_name)
        except KeyError:
            return
        if plugin is None:
            return
        item = QtWidgets.QTreeWidgetItem()
        icon, tooltip = self._get_status_icon_and_tooltip(plugin, config)
        item.setIcon(COL_NAME, icon)
        item.setToolTip(COL_NAME, tooltip)
        item.setText(COL_NAME, config.name)
        item.setText(COL_TYPE, config.type_name)
        icon = QtGui.QIcon.fromTheme('emblem-favorite') if is_default else QtGui.QIcon()
        item.setIcon(COL_DEFAULT, icon)
        item.setText(COL_VERSION, self._get_version(plugin, config))
        try:
            item.setData(DATA_COL_WIDGET, QtCore.Qt.UserRole, plugin.get_compiler_config_widget())
        except AttributeError:
            pass
        item.setData(DATA_COL_CONFIG, QtCore.Qt.UserRole, config)
        item.setData(DATA_COL_PLUGIN, QtCore.Qt.UserRole, plugin)
        item.setSelected(select)
        if select:
            self._item_to_select = item
        self.names.add(config.name)
        parent.addChild(item)
        return item

    def _clear_tree(self):
        for item_type in [ITEM_AUTO_DETECTED, ITEM_MANUAL]:
            item = self.tree.topLevelItem(item_type)
            while item.childCount():
                item.removeChild(item.child(0))

    def _get_name(self, parent, type_name):
        name = ''
        while not self._check_name(name):
            if name:
                QtWidgets.QMessageBox.warning(parent, 'Invalid name',
                                              'The name %r is already used for another configuration' % name)
            name, ok = QtWidgets.QInputDialog.getText(parent, 'Add new configuration', 'Name:',
                                                      QtWidgets.QLineEdit.Normal, self._suggest_name(type_name))
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

    def _get_success_status_meta(self, normal_icon):
        tooltip = _('<h3 style="color:green;">Check succeeded</h3><p>All checks passed...</p>')
        return normal_icon, tooltip

    def _get_error_status_meta(self, error):
        icon_names = {error.ERROR: 'dialog-error', error.WARNING: 'dialog-warning'}
        colors = {error.ERROR: 'red', error.WARNING: 'yellow'}
        header = _('<h2 style="color:%s;">Check failed:</h2>') % colors[error.error_level]
        icon = QtGui.QIcon.fromTheme(icon_names[error.error_level])
        msg_html = '<p>' + error.message.replace('\n', '</p><p>') + '</p>'
        tooltip = header + msg_html
        return icon, tooltip.replace('\n', '</p><p>')

    def _select_path(self, parent, name, directory=''):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(parent, name, directory)
        if path:
            return True, path
        return False, ''

    def _update_current_config_meta(self):
        if self._updating_config:
            return
        item = self.tree.currentItem()
        if item is None:
            return
        try:
            config = self._get_updated_config()
        except AttributeError:
            return
        plugin = item.data(DATA_COL_PLUGIN, QtCore.Qt.UserRole)
        if not config or not plugin:
            return
        icon, tooltip = self._get_status_icon_and_tooltip(plugin, config)
        item.setIcon(COL_NAME, icon)
        item.setToolTip(COL_NAME, tooltip)
        item.setText(COL_VERSION, self._get_version(plugin, config))
