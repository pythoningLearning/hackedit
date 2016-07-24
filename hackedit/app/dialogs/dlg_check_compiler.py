import os
from PyQt5 import QtCore, QtWidgets


from hackedit.api.utils import ProgramCheckFailedError
from hackedit.api.compiler import check_compiler
from hackedit.app.forms import dlg_check_compiler_ui


class DlgCheckCompiler(QtWidgets.QDialog):
    def __init__(self, compiler, parent, bt_check_message, check_function):
        super().__init__(
            parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.ui = dlg_check_compiler_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.compiler = compiler
        self.check_function = check_function
        button = self.get_check_compilation_button()
        button.setText(bt_check_message)
        button.clicked.connect(self._check_compiler)
        version = self.compiler.get_version(include_all=True)
        self.ui.textEdit.setText(version)

    def get_check_compilation_button(self):
        return self.ui.buttonBox.button(self.ui.buttonBox.Apply)

    def _check_compiler(self):
        QtWidgets.qApp.setOverrideCursor(QtCore.Qt.WaitCursor)
        try:
            self.check_function(self.compiler)
        except ProgramCheckFailedError as e:
            colors = {e.ERROR: 'red', e.WARNING: 'yellow'}
            self.ui.textEdit.setText(_('<h1 style="color:%s;">Check failed!</h1>') % colors[e.error_level])
            self.ui.textEdit.append(_('<h2>Output:</h2><p>%s</p>') % e.message.replace('\n', '<br>'))
            if e.return_code is not None:
                self.ui.textEdit.append(_('<h2>Exit code<b>:</h2><p>%d</p>' % e.return_code))
        else:
            msg = _('<h1 style="color:green;">Check succeeded!</h1><p>All checks passed...</p>')
            self.ui.textEdit.setText(msg)
        finally:
            QtWidgets.qApp.restoreOverrideCursor()
        tc = self.ui.textEdit.textCursor()
        tc.setPosition(0)
        self.ui.textEdit.setTextCursor(tc)

    @classmethod
    def check(cls, parent, compiler, bt_check_message=_('Check compilation'), check_function=check_compiler):
        dlg = cls(compiler, parent, bt_check_message, check_function)
        return dlg.exec_() == dlg.Accepted
