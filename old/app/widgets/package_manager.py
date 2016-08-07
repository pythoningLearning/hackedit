import logging
from PyQt5 import QtCore, QtGui, QtWidgets

from hackedit.app.forms import widget_package_manager_ui
from hackedit.api.widgets import DlgProcessOutput
from hackedit.api.interpreter import PackageManager, Package

COL_NAME = 0
COL_VERSION = 1
COL_LATEST = 2


class _DlgProcessError(QtWidgets.QDialog):
    def __init__(self, parent, message, process_outpude):
        super().__init__(self)


class _BackgroundThread(QtCore.QThread):
    finished = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.function = None
        self.parameter = None

    def run(self):
        if not self.function:
            return
        if self.parameter:
            ret_val = self.function(self.parameter)
        else:
            ret_val = self.function()
        self.finished.emit(ret_val)


class _Operation(QtCore.QObject):
    finished = QtCore.pyqtSignal(object)

    def __init__(self, package_manager_widget, name, function, parameter=None):
        super().__init__()
        assert isinstance(package_manager_widget, PackageManagerWidget)
        self.cancelled = False
        self.name = name
        self._function = function
        self._parameter = parameter
        self._ui = package_manager_widget._ui
        self._package_manager_widget = package_manager_widget

    def start(self):
        self._thread = _BackgroundThread()
        self._thread.finished.connect(self._on_operation_finished)
        self._thread.function = self._function
        self._thread.parameter = self._parameter
        self._thread.start()

    def _on_operation_finished(self, result):
        try:
            if not self.cancelled:
                self._specific_on_operation_finished(result)
            self.finished.emit(self)
        except RuntimeError:
            return

    def _get_packages_list_as_string(self, packages):
        return ', '.join(packages)


class _ListPackagesOperation(_Operation):
    def __init__(self, parent):
        super().__init__(parent, _('Refreshing list of packages'), parent._package_manager.get_installed_packages)

    def _specific_on_operation_finished(self, result):
        self._ui.table_packages.clearContents()
        self._ui.table_packages.setRowCount(0)
        for package in result:
            self.add_package(package)
        self._ui.table_packages.selectRow(self._package_manager_widget._row_to_select)

    def add_package(self, package):
        assert isinstance(package, Package)
        row_index = self._ui.table_packages.rowCount()
        self._ui.table_packages.insertRow(row_index)
        self._ui.table_packages.setItem(row_index, COL_NAME, QtWidgets.QTableWidgetItem(package.name))
        self._ui.table_packages.setItem(row_index, COL_VERSION, QtWidgets.QTableWidgetItem(package.current_version))
        item = QtWidgets.QTableWidgetItem(package.latest_version)
        if package.outdated:
            item.setIcon(QtGui.QIcon.fromTheme('system-software-update'))
        self._ui.table_packages.setItem(row_index, COL_LATEST, item)


class _UpdatePackagesOperation(_Operation):
    def __init__(self, parent, packages):
        super().__init__(parent, _('Updating packages: %s') % self._get_packages_list_as_string(packages),
                         parent._package_manager.update_packages, parameter=packages)

    def _specific_on_operation_finished(self, result):
        self._package_manager_widget.refresh(clear=False)
        exit_code, output = result
        if exit_code != 0:
            DlgProcessOutput.show_dialog(_("Failed to update some packages:"), output,
                                         parent=self._package_manager_widget)


class _InstallPackagesOperation(_Operation):
    def __init__(self, parent, packages):
        super().__init__(parent, _('Installing packages: %s') % self._get_packages_list_as_string(packages),
                         parent._package_manager.install_packages, parameter=packages)

    def _specific_on_operation_finished(self, result):
        self._package_manager_widget.refresh(clear=False)
        exit_code, output = result
        if exit_code != 0:
            DlgProcessOutput.show_dialog(_("Failed to install some packages:"),
                                         output, parent=self._package_manager_widget)


class _UninstallPackagesOperation(_Operation):
    def __init__(self, parent, packages):
        super().__init__(parent, _('Uninstalling packages: %r') % self._get_packages_list_as_string(packages),
                         parent._package_manager.uninstall_packages, parameter=packages)

    def _specific_on_operation_finished(self, result):
        self._package_manager_widget.refresh(clear=False)
        exit_code, output = result
        if exit_code != 0:
            DlgProcessOutput.show_dialog(_("Failed to uninstall some packages:"),
                                         output, parent=self._package_manager_widget)


class PackageManagerWidget(QtWidgets.QWidget):
    state_changed = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._operations = []
        self._package_manager = None
        self.enabled = True
        self.state_changed.connect(self._on_state_changed)
        self._setup_ui()
        self._on_operation_finished(None)

    def _setup_ui(self):
        self._ui = widget_package_manager_ui.Ui_Form()
        self._ui.setupUi(self)
        self._ui.label_status.hide()
        self._ui.progress_bar.hide()
        self._ui.table_packages.horizontalHeader().setSectionResizeMode(COL_NAME, QtWidgets.QHeaderView.Stretch)
        self._ui.table_packages.horizontalHeader().setSectionResizeMode(COL_VERSION,
                                                                        QtWidgets.QHeaderView.ResizeToContents)
        self._ui.table_packages.horizontalHeader().setSectionResizeMode(COL_LATEST,
                                                                        QtWidgets.QHeaderView.ResizeToContents)
        self._ui.bt_update_package.clicked.connect(self._update_selected_packages)
        self._ui.bt_add_packages.clicked.connect(self._install_packages)
        self._ui.bt_rm_package.clicked.connect(self._uninstall_packages)

    def set_package_manager(self, package_manager):
        if self._package_manager and package_manager.config.command == self._package_manager.config.command:
            return
        for op in self._operations:
            op.cancelled = True
            self._operations.remove(op)
        assert isinstance(package_manager, PackageManager)
        self._package_manager = package_manager
        self.refresh()

    def refresh(self, clear=True):
        _logger().info('refreshing packages for interpreter config: %r', self._package_manager.config)
        if clear:
            self._ui.table_packages.clearContents()
            self._ui.table_packages.setRowCount(0)
        self._row_to_select = self._ui.table_packages.currentRow()
        self._run_operation(_ListPackagesOperation(self))

    def _run_operation(self, operation):
        self._ui.label_status.setText(operation.name)
        self._ui.label_status.setVisible(True)
        self._ui.progress_bar.setVisible(True)
        self.state_changed.emit(False)
        self._operations.append(operation)
        operation.finished.connect(self._on_operation_finished)
        operation.start()
        QtWidgets.qApp.restoreOverrideCursor()
        QtWidgets.qApp.setOverrideCursor(QtCore.Qt.WaitCursor)

    def _on_state_changed(self, enabled):
        self.enabled = enabled
        self._ui.bt_add_packages.setEnabled(enabled)
        self._ui.bt_update_package.setEnabled(enabled)
        self._ui.bt_rm_package.setEnabled(enabled)

    def _on_operation_finished(self, operation):
        if operation:
            self._operations.remove(operation)
        if not self._operations:
            self.state_changed.emit(True)
            self._ui.label_status.hide()
            self._ui.progress_bar.hide()
            QtWidgets.qApp.restoreOverrideCursor()

    def _update_selected_packages(self):
        names = self._get_selected_names()
        answer = QtWidgets.QMessageBox.question(
            self, 'Confirm update', 'Are you sure you want to update the following packages:\n '
            '-%s' % '\n -'.join(names))
        if answer == QtWidgets.QMessageBox.No:
            return
        _logger().info('updating packages: %r', names)
        if names:
            self._run_operation(_UpdatePackagesOperation(self, names))

    def _get_selected_names(self):
        names = []
        for item in self._ui.table_packages.selectedItems():
            if item.column() == COL_NAME:
                names.append(item.text())
        return names

    def _install_packages(self):
        packages, status = QtWidgets.QInputDialog.getText(self, _('Install packages'), _('Packages: '))
        if not status or not packages:
            return
        packages = packages.split(' ')
        _logger().info('uninstalling packages: %r', packages)
        self._run_operation(_InstallPackagesOperation(self, packages))

    def _uninstall_packages(self):
        names = self._get_selected_names()
        answer = QtWidgets.QMessageBox.question(
            self, 'Confirm uninstall', 'Are you sure you want to uninstall the following '
            'packages:\n -%s' % '\n -'.join(names))
        if answer == QtWidgets.QMessageBox.No:
            return
        if names:
            _logger().info('uninstalling packages: %r', names)
            self._run_operation(_UninstallPackagesOperation(self, names))


if __name__ == '__main__':
    from hackedit_python.plugins.interpreter import Pip, Python3Config
    app = QtWidgets.QApplication([])
    pm = PackageManagerWidget()
    pm.set_package_manager(Pip(Python3Config()))
    pm.show()
    app.exec_()


def _logger():
    return logging.getLogger(__name__)
