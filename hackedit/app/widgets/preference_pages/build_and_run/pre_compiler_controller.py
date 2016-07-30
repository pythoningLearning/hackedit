from PyQt5 import QtCore, QtGui, QtWidgets

from hackedit.api import pre_compiler, plugins, system, utils
from hackedit.app import settings
from hackedit.app.dialogs import dlg_check_compiler

from .base import BuildAndRunTabController


ITEM_AUTO_DETECTED = 0
ITEM_MANUAL = 1

COL_NAME = 0
COL_TYPE = 1
COL_VERSION = 2

DATA_COL_WIDGET = COL_NAME
DATA_COL_CONFIG = COL_TYPE
DATA_COL_PLUGIN = COL_VERSION


class PreCompilersController(BuildAndRunTabController):
    def __init__(self, ui):
        """
        :type ui: hackedit.app.forms.settings_page_build_and_run_ui.Ui_Form
        """
        super().__init__()
        self.ui = ui
        self._updating_config = False
        self._current_config = None
        self._current_config_editable = False
        self._connect_slots()

    def _connect_slots(self):
        self.ui.tree_pre_compilers.itemSelectionChanged.connect(self._update_config)
        self.ui.bt_clone_pre_compiler.clicked.connect(self._clone_config)
        self.ui.bt_delete_pre_compiler.clicked.connect(self._delete_config)
        self.ui.bt_check_pre_compiler.clicked.connect(self._check_pre_compiler)
        self.ui.bt_select_pre_compiler_path.clicked.connect(self._select_pre_compiler_path)
        self.ui.edit_pre_compiler_path.textChanged.connect(self._update_current_config_meta)
        self.ui.edit_pre_compiler_extensions.textChanged.connect(self._update_current_config_meta)
        self.ui.edit_pre_compiler_output_pattern.textChanged.connect(self._update_current_config_meta)

    def reset(self):
        self.names = set()
        mnu_compiler_types = QtWidgets.QMenu()
        self.ui.bt_add_pre_compiler.setMenu(mnu_compiler_types)
        self.clear_tree()
        # autodetected configs
        for plugin in plugins.get_pre_compiler_plugins():
            action = mnu_compiler_types.addAction(plugin.get_pre_compiler_type_name())
            action.triggered.connect(self._add_config)
            for config in plugin.get_auto_detected_configs():
                self._add_config_item(config, item_type=ITEM_AUTO_DETECTED, plugin=plugin)
        self.ui.tree_pre_compilers.setCurrentItem(None)

        # add user defined configuration
        self.user_configs = settings.load_pre_compiler_configurations()
        for key, value in sorted(self.user_configs.items(), key=lambda x: x[0]):
            self._add_config_item(value)
        self.ui.tree_pre_compilers.header().setStretchLastSection(False)
        self.ui.tree_pre_compilers.header().setDefaultSectionSize(16)
        self.ui.tree_pre_compilers.header().setSectionResizeMode(COL_NAME, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.tree_pre_compilers.header().setSectionResizeMode(COL_TYPE, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.tree_pre_compilers.header().setSectionResizeMode(COL_VERSION, QtWidgets.QHeaderView.Stretch)
        self.ui.tree_pre_compilers.expandAll()
        self._update_config()

    def clear_tree(self):
        for item_type in [ITEM_AUTO_DETECTED, ITEM_MANUAL]:
            item = self.ui.tree_pre_compilers.topLevelItem(item_type)
            while item.childCount():
                item.removeChild(item.child(0))

    def restore_defaults(self):
        settings.save_compiler_configurations({})

    def save(self):
        self._save_current_config()
        settings.save_pre_compiler_configurations(self.user_configs)

    def _add_config(self):
        type_name = self.sender().text()
        ok, name = self.get_name(self.ui.bt_add_pre_compiler, type_name)
        if not ok:
            return
        plugin = plugins.get_pre_compiler_plugin(type_name)
        config = plugin.create_new_configuration_with_dialog(self.ui.bt_add_pre_compiler, name)
        if config is None:
            return
        self.user_configs[config.name] = config
        item = self._add_config_item(config, plugin=plugin)
        item.setSelected(True)
        self.ui.tree_pre_compilers.setCurrentItem(item)
        self._update_config()
        self.names.add(name)

    def _clone_config(self):
        cloned_config = self._current_config.copy()
        plugin = plugins.get_pre_compiler_plugin(cloned_config.type_name)
        ok, name = self.get_name(self.ui.bt_clone_compiler, cloned_config.type_name)
        if not ok:
            return
        cloned_config.name = name
        self.user_configs[name] = cloned_config
        item = self._add_config_item(cloned_config, plugin=plugin)
        item.setSelected(True)
        self.ui.tree_pre_compilers.setCurrentItem(item)
        self._update_config()

    def _delete_config(self):
        answer = QtWidgets.QMessageBox.question(
            self.ui.bt_delete_compiler, "Remove configuration?",
            'Are you sure you want to remove the selected configuration: %r?' % self._current_config.name)
        if answer == QtWidgets.QMessageBox.No:
            return
        item = self.ui.tree_pre_compilers.currentItem()
        self.user_configs.pop(self._current_config.name)
        try:
            self.names.remove(self._current_config.name)
        except ValueError:
            pass
        self._current_config = None
        parent = item.parent()
        parent.removeChild(item)
        self._update_config()

    def _get_pre_compiler_status_meta(self, plugin, config):
        precompiler = pre_compiler.PreCompiler(config)
        icon, tooltip = self.get_success_status_meta(plugin.get_pre_compiler_icon())
        try:
            pre_compiler.check_pre_compiler(precompiler)
        except utils.ProgramCheckFailedError as e:
            icon, tooltip = self.get_error_status_meta(e)
        return icon, tooltip

    def _get_pre_compiler_version(self, config):
        precompiler = pre_compiler.PreCompiler(config)
        return pre_compiler.get_version(precompiler, include_all=False)

    def _add_config_item(self, config, item_type=ITEM_MANUAL, plugin=None):
        parent = self.ui.tree_pre_compilers.topLevelItem(item_type)
        if plugin is None:
            plugin = plugins.get_pre_compiler_plugin(config.type_name)
        if plugin is None:
            return
        item = QtWidgets.QTreeWidgetItem()
        icon, tooltip = self._get_pre_compiler_status_meta(plugin, config)
        version = self._get_pre_compiler_version(config)
        item.setIcon(COL_NAME, icon)
        item.setToolTip(COL_NAME, tooltip)
        item.setText(COL_NAME, config.name)
        item.setText(COL_TYPE, config.type_name)
        item.setText(COL_VERSION, version)
        item.setData(DATA_COL_CONFIG, QtCore.Qt.UserRole, config)
        item.setData(DATA_COL_PLUGIN, QtCore.Qt.UserRole, plugin)
        self.names.add(config.name)
        parent.addChild(item)
        return item

    def _save_current_config(self):
        if self._current_config and self._current_config_editable:
            cfg = self._get_updated_config()
            cfg.name = self._current_config.name

            # save config changes in temporary map
            self.user_configs[self._current_config.name] = cfg

            # update associate item data to keep in sync
            manual = self.ui.tree_pre_compilers.topLevelItem(ITEM_MANUAL)
            for index in range(manual.childCount()):
                item = manual.child(index)
                if item.text(0) == cfg.name:
                    item.setData(DATA_COL_CONFIG, QtCore.Qt.UserRole, cfg)

    def _get_updated_config(self):
        cfg = self._current_config.copy()
        cfg.path = self.ui.edit_pre_compiler_path.text().strip()
        cfg.associated_extensions = [t for t in self.ui.edit_pre_compiler_extensions.text().strip().split(';') if t]
        cfg.flags = [t for t in self.ui.edit_pre_compiler_flags.text().strip().split(' ') if t]
        cfg.command_pattern = self.ui.edit_command_pattern.text().strip()
        cfg.output_pattern = self.ui.edit_pre_compiler_output_pattern.text().strip()
        return cfg

    def _update_config(self, *args):
        self._updating_config = True
        self._save_current_config()
        current_item = self.ui.tree_pre_compilers.currentItem()
        if current_item is None or current_item.parent() is None:
            # no item selected or top level item
            editable = False
            clonable = False
            self._current_config = None
            self._current_config_editable = None
            self._display_config()
        else:
            clonable = True
            config = current_item.data(DATA_COL_CONFIG, QtCore.Qt.UserRole)
            self._display_config(config)
            parent_item = current_item.parent()
            parent_item_index = self.ui.tree_pre_compilers.indexOfTopLevelItem(parent_item)
            editable = parent_item_index != ITEM_AUTO_DETECTED
            self._current_config_editable = editable
            self._current_config = config
        self.ui.bt_delete_pre_compiler.setEnabled(editable)
        self.ui.bt_check_pre_compiler.setEnabled(clonable)
        self.ui.bt_clone_pre_compiler.setEnabled(clonable)
        self._updating_config = False

    def _display_config(self, config=None):
        if config is None:
            self.ui.group_pre_compiler_settings.setVisible(False)
            config = pre_compiler.PreCompilerConfig()
        else:
            self.ui.group_pre_compiler_settings.setVisible(True)
        self.ui.edit_pre_compiler_path.setText(config.path)
        self.ui.edit_command_pattern.setText(config.command_pattern)
        self.ui.edit_command_pattern.setVisible(config.command_pattern_editable)
        self.ui.lbl_command_pattern.setVisible(config.command_pattern_editable)
        self.ui.edit_pre_compiler_extensions.setText(';'.join(config.associated_extensions))
        self.ui.edit_pre_compiler_flags.setText(' '.join(config.flags))
        self.ui.edit_pre_compiler_output_pattern.setText(config.output_pattern)

    def _select_pre_compiler_path(self):
        status, path = self.select_path(self.ui.bt_select_pre_compiler_path, _('Select pre-compiler'),
                                        directory=self.ui.edit_pre_compiler_path.text())
        if status and path:
            self.ui.edit_pre_compiler_path.setText(path)

    def _update_current_config_meta(self):
        if self._updating_config:
            return
        item = self.ui.tree_pre_compilers.currentItem()
        if item is None:
            return
        try:
            config = self._get_updated_config()
        except AttributeError:
            return
        plugin = item.data(DATA_COL_PLUGIN, QtCore.Qt.UserRole)
        if not config or not plugin:
            return
        icon, tooltip = self._get_pre_compiler_status_meta(plugin, config)
        item.setIcon(COL_NAME, icon)
        item.setToolTip(COL_NAME, tooltip)
        item.setText(COL_VERSION, self._get_pre_compiler_version(config))

    def _check_pre_compiler(self):
        cfg = self._get_updated_config()
        precompiler = pre_compiler.PreCompiler(cfg)
        dlg_check_compiler.DlgCheckCompiler.check(
            self.ui.bt_check_pre_compiler, precompiler, bt_check_message=_('Check pre-compilation'),
            check_function=pre_compiler.check_pre_compiler)
