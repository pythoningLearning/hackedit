# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/Documents/hackedit/data/forms/locator.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(698, 274)
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalLayout = QtWidgets.QVBoxLayout(Frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bt_infos = QtWidgets.QToolButton(Frame)
        icon = QtGui.QIcon.fromTheme("dialog-information")
        self.bt_infos.setIcon(icon)
        self.bt_infos.setObjectName("bt_infos")
        self.horizontalLayout.addWidget(self.bt_infos)
        self.lineEdit = PromptLineEdit(Frame)
        self.lineEdit.setMinimumSize(QtCore.QSize(400, 0))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.bt_close = QtWidgets.QToolButton(Frame)
        icon = QtGui.QIcon.fromTheme("window-close")
        self.bt_close.setIcon(icon)
        self.bt_close.setObjectName("bt_close")
        self.horizontalLayout.addWidget(self.bt_close)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.treeWidget = QtWidgets.QTreeWidget(Frame)
        self.treeWidget.setMaximumSize(QtCore.QSize(16777215, 500))
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.treeWidget)
        self.cb_non_project_files = QtWidgets.QCheckBox(Frame)
        self.cb_non_project_files.setObjectName("cb_non_project_files")
        self.verticalLayout.addWidget(self.cb_non_project_files)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        from hackedit.api.i18n import get_translation
        _ = get_translation(package="hackedit")
        Frame.setWindowTitle(_("Frame"))
        self.bt_infos.setToolTip(_("Help"))
        self.bt_infos.setText(_("..."))
        self.bt_close.setToolTip(_("Close"))
        self.bt_close.setText(_("..."))
        self.cb_non_project_files.setText(_("Include non-project files (Shift+Enter)"))

from pyqode.core.widgets import PromptLineEdit
