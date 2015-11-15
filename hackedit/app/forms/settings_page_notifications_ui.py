# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/dev/hackedit/data/forms/settings_page_notifications.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(583, 527)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cb_allow_system_tray = QtWidgets.QCheckBox(Form)
        self.cb_allow_system_tray.setChecked(True)
        self.cb_allow_system_tray.setObjectName("cb_allow_system_tray")
        self.verticalLayout.addWidget(self.cb_allow_system_tray)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cb_info = QtWidgets.QCheckBox(self.groupBox)
        icon = QtGui.QIcon.fromTheme("dialog-information")
        self.cb_info.setIcon(icon)
        self.cb_info.setChecked(False)
        self.cb_info.setObjectName("cb_info")
        self.verticalLayout_2.addWidget(self.cb_info)
        self.cb_warning = QtWidgets.QCheckBox(self.groupBox)
        icon = QtGui.QIcon.fromTheme("dialog-warning")
        self.cb_warning.setIcon(icon)
        self.cb_warning.setChecked(True)
        self.cb_warning.setObjectName("cb_warning")
        self.verticalLayout_2.addWidget(self.cb_warning)
        self.cb_errors = QtWidgets.QCheckBox(self.groupBox)
        icon = QtGui.QIcon.fromTheme("dialog-error")
        self.cb_errors.setIcon(icon)
        self.cb_errors.setChecked(True)
        self.cb_errors.setObjectName("cb_errors")
        self.verticalLayout_2.addWidget(self.cb_errors)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.blacklist = QtWidgets.QListWidget(self.groupBox_2)
        self.blacklist.setObjectName("blacklist")
        self.horizontalLayout.addWidget(self.blacklist)
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
        import gettext
        _ = gettext.gettext

        Form.setWindowTitle(_("Form"))
        Form.setToolTip(_("Show notifications in system tray (depends on the OS and whether the tray icon is visible or not)"))
        self.cb_allow_system_tray.setToolTip(_("If checked, the IDE notifications will be shown through the system tray icon (or libnotify on GNU/Linux)."))
        self.cb_allow_system_tray.setText(_("Show notification in system tray"))
        self.groupBox.setTitle(_("Open pane automatically for"))
        self.cb_info.setToolTip(_("General purpose information messages"))
        self.cb_info.setText(_("Information messages"))
        self.cb_warning.setToolTip(_("User warnings"))
        self.cb_warning.setText(_("Warning messages"))
        self.cb_errors.setToolTip(_("Internal errors,..."))
        self.cb_errors.setText(_("Error messages"))
        self.groupBox_2.setTitle(_("Blacklist"))
        self.blacklist.setToolTip(_("The list of ignored notifications"))
        self.bt_rm.setToolTip(_("Remove the select notification from the blacklist."))
        self.bt_rm.setText(_("..."))
        self.bt_clear.setToolTip(_("Clear tjhe blacklist"))
        self.bt_clear.setText(_("..."))

