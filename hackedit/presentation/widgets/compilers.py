import os

from PyQt5 import QtWidgets
from hackedit.presentation.forms import compiler_config_ui


class CompilerConfigWidget(QtWidgets.QWidget):
    """
    Base class for writing a compiler configuration widget. Such a widget is used to edit the options of a compiler
    configuration (all settings except the compiler directory and the environment variables).
    """
    def is_dirty(self):
        return self._original_config.to_json() != self.get_config().to_json()

    def set_config(self, config):
        """
        Sets the compiler configuration (update widget properties).

        :param config: CompilerConfig
        """
        self._original_config = config
        self._config = config.copy()

    def get_config(self):
        """
        Gets the edited compiler configuration.

        :rtype: CompilerConfig
        """
        return self._config


class GenericCompilerCongigWidget(CompilerConfigWidget):
    """
    Generic _config widgets that let user define the include paths, the library paths, the libraries to link
    with and add custom compiler switches.
    """
    def __init__(self, parent=None, ui_form=None):
        super().__init__(parent=parent)
        if ui_form is None:
            ui_form = compiler_config_ui.Ui_Form()
        self.ui = ui_form
        self.ui.setupUi(self)
        self.ui.bt_abs_include_path.clicked.connect(self._add_abs_include_path)
        self.ui.bt_rel_include_path.clicked.connect(self._add_rel_include_path)
        self.ui.bt_delete_include_path.clicked.connect(self._rm_include_path)
        self.ui.bt_abs_lib_path.clicked.connect(self._add_abs_lib_path)
        self.ui.bt_rel_lib_path.clicked.connect(self._add_rel_lib_path)
        self.ui.bt_delete_lib_path.clicked.connect(self._rm_library_path)

    def set_config(self, config):
        super().set_config(config)
        self.ui.edit_flags.setText(' '.join(config.flags))
        self.ui.list_include_paths.clear()
        for path in config.include_paths:
            item = QtWidgets.QListWidgetItem()
            item.setText(path)
            self.ui.list_include_paths.addItem(item)
        self.ui.list_lib_paths.clear()
        for path in config.library_paths:
            item = QtWidgets.QListWidgetItem()
            item.setText(path)
            self.ui.list_lib_paths.addItem(item)
        self.ui.edit_libs.setText(' '.join(config.libraries))

    def get_config(self):
        self._config.flags = [token for token in self.ui.edit_flags.text().split(' ') if token]
        self._config.libraries = [token for token in self.ui.edit_libs.text().split(' ') if token]
        self._config.include_paths.clear()
        for i in range(self.ui.list_include_paths.count()):
            path = self.ui.list_include_paths.item(i).text()
            if path:
                self._config.include_paths.append(path)
        self._config.library_paths.clear()
        for i in range(self.ui.list_lib_paths.count()):
            path = self.ui.list_lib_paths.item(i).text()
            if path:
                self._config.library_paths.append(path)
        return super().get_config()

    def _add_abs_include_path(self):  # pragma: no cover
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, _('Select an include path'), os.path.expanduser('~'))
        if path:
            self.ui.list_include_paths.addItem(os.path.normpath(path))

    def _add_rel_include_path(self):  # pragma: no cover
        path, status = QtWidgets.QInputDialog.getText(
            self, _('Add relative include path'), 'Path:')
        if status:
            self.ui.list_include_paths.addItem(path)

    def _rm_include_path(self):  # pragma: no cover
        current = self.ui.list_include_paths.currentRow()
        if current != -1:
            self.ui.list_include_paths.takeItem(current)

    def _add_abs_lib_path(self):  # pragma: no cover
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, _('Select a library path'), os.path.expanduser('~'))
        if path:
            self.ui.list_lib_paths.addItem(os.path.normpath(path))

    def _add_rel_lib_path(self):  # pragma: no cover
        path, status = QtWidgets.QInputDialog.getText(
            self, _('Add relative library path'), 'Path:')
        if status:
            self.ui.list_lib_paths.addItem(path)

    def _rm_library_path(self):  # pragma: no cover
        current = self.ui.list_lib_paths.currentRow()
        if current != -1:
            self.ui.list_lib_paths.takeItem(current)