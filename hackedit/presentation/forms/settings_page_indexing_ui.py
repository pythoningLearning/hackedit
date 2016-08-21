# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/Documents/hackedit/data/forms/settings_page_indexing.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(583, 527)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cb_enable_indexing = QtWidgets.QCheckBox(self.groupBox)
        self.cb_enable_indexing.setChecked(False)
        self.cb_enable_indexing.setObjectName("cb_enable_indexing")
        self.verticalLayout_2.addWidget(self.cb_enable_indexing)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.list_projects = QtWidgets.QListWidget(self.groupBox_2)
        self.list_projects.setObjectName("list_projects")
        self.horizontalLayout.addWidget(self.list_projects)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.bt_rm = QtWidgets.QToolButton(self.groupBox_2)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.bt_rm.setIcon(icon)
        self.bt_rm.setObjectName("bt_rm")
        self.verticalLayout_3.addWidget(self.bt_rm)
        self.bt_clear = QtWidgets.QToolButton(self.groupBox_2)
        icon = QtGui.QIcon.fromTheme("edit-clear")
        self.bt_clear.setIcon(icon)
        self.bt_clear.setObjectName("bt_clear")
        self.verticalLayout_3.addWidget(self.bt_clear)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        from hackedit.application.i18n import get_translation
        _ = get_translation(package="hackedit")
        Form.setWindowTitle(_("Form"))
        Form.setToolTip(_("Show notifications in system tray (depends on the OS and whether the tray icon is visible or not)"))
        self.groupBox.setTitle(_("Configure indexing"))
        self.cb_enable_indexing.setToolTip(_("<html><head/><body><p>Enable or disable project indexing. </p><p>If you disable indexing you won\'t be able to use the goto dialog and searching will be a bit slower.</p></body></html>"))
        self.cb_enable_indexing.setText(_("Enable project indexing"))
        self.groupBox_2.setTitle(_("Content"))
        self.list_projects.setToolTip(_("The whole list of indexed locations."))
        self.bt_rm.setToolTip(_("<html><head/><body><p>Remove the selected project from the index database.</p><p>Removing a project from the index will force a full reindexing of that project.</p></body></html>"))
        self.bt_rm.setText(_("..."))
        self.bt_clear.setToolTip(_("<html><head/><body><p>Clear the index database.</p><p>Clearing the index database will force a full reindexing of all open projects.</p></body></html>"))
        self.bt_clear.setText(_("..."))

