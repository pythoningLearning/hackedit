from PyQt5 import QtCore, QtGui, QtWidgets


class BuildAndRunTabController(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.names = set()

    def reset(self):
        pass

    def restore_defaults(self):
        pass

    def save(self):
        pass

    def get_name(self, parent, type_name):
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

    def get_success_status_meta(self, normal_icon):
        tooltip = _('<h3 style="color:green;">Check succeeded</h3><p>All checks passed...</p>')
        return normal_icon, tooltip

    def get_error_status_meta(self, error):
        icon_names = {error.ERROR: 'dialog-error', error.WARNING: 'dialog-warning'}
        colors = {error.ERROR: 'red', error.WARNING: 'yellow'}
        header = _('<h2 style="color:%s;">Check failed:</h2>') % colors[error.error_level]
        icon = QtGui.QIcon.fromTheme(icon_names[error.error_level])
        msg_html = '<p>' + error.message.replace('\n', '</p><p>') + '</p>'
        tooltip = header + msg_html
        return icon, tooltip.replace('\n', '</p><p>')

    def select_path(self, parent, name, directory=''):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(parent, name, directory)
        if path:
            return True, path
        return False, ''
