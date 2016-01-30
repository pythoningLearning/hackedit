# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/dev/HackEdit/hackedit/data/forms/terminal_widget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.console = InteractiveConsole(Form)
        self.console.setObjectName("console")
        self.verticalLayout.addWidget(self.console)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edit_command = PromptLineEdit(Form)
        self.edit_command.setObjectName("edit_command")
        self.horizontalLayout.addWidget(self.edit_command)
        self.bt_run = QtWidgets.QToolButton(Form)
        self.bt_run.setText("")
        icon = QtGui.QIcon.fromTheme("system-run")
        self.bt_run.setIcon(icon)
        self.bt_run.setObjectName("bt_run")
        self.horizontalLayout.addWidget(self.bt_run)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        from hackedit.api.gettext import translation
        _ = translation(package="hackedit")
        Form.setWindowTitle(_("Form"))
        self.console.setToolTip(_("Command output"))
        self.edit_command.setToolTip(_("Type a command to execute"))
        self.bt_run.setToolTip(_("Run command (keep pressed to access the terminal history)"))

from pyqode.core.widgets import InteractiveConsole, PromptLineEdit
