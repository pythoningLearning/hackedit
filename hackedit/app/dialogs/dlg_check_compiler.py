import os
from PyQt5 import QtCore, QtWidgets


from hackedit.api.compiler import CompilerCheckFailedError, check_compiler
from hackedit.app.forms import dlg_check_compiler_ui


class DlgCheckCompiler(QtWidgets.QDialog):
    def __init__(self, compiler, parent):
        super().__init__(
            parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.ui = dlg_check_compiler_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.compiler = compiler
        button = self.get_check_compilation_button()
        button.setText(_('Check compilation'))
        button.clicked.connect(self._check_compiler)
        if not os.path.exists(compiler.get_full_compiler_path()):
            self.ui.textEdit.setText(_('Compiler not found'))
            button.setDisabled(True)
        else:
            version = self.compiler.get_version(include_all=True)
            self.ui.textEdit.setText(version if version else _('Unable to find compiler version'))

    def get_check_compilation_button(self):
        return self.ui.buttonBox.button(self.ui.buttonBox.Apply)

    def _check_compiler(self):
        QtWidgets.qApp.setOverrideCursor(QtCore.Qt.WaitCursor)
        try:
            check_compiler(self.compiler)
        except CompilerCheckFailedError as e:
            self.ui.textEdit.setText(_('<h1 style="color:red;">Compiler check failed!</h1>'))
            self.ui.textEdit.append(_('<h2>Exit code<b>:</h2><p>%d</p>' % e.return_code))
            self.ui.textEdit.append(_('<h2>Output:</h2>'))
            self.ui.textEdit.append('<p>%s</p>' % e.message.replace('\n', '<br>'))
            tips = _('<h2>Tips:</h2><p><i>  - You might need to adapt the '
                     'environment variables set by the IDE to make it work.'
                     '</i></p>')
            self.ui.textEdit.append(tips)
        else:
            msg = _('<h1 style="color:green;">Compiler check succeeded!</h1>')
            self.ui.textEdit.setText(msg)
        finally:
            QtWidgets.qApp.restoreOverrideCursor()
        tc = self.ui.textEdit.textCursor()
        tc.setPosition(0)
        self.ui.textEdit.setTextCursor(tc)

    @classmethod
    def check(cls, parent, compiler):
        dlg = cls(compiler, parent)
        return dlg.exec_() == dlg.Accepted
