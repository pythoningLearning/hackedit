# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/Documents/hackedit/data/forms/widget_package_manager.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(973, 571)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.table_packages = QtWidgets.QTableWidget(Form)
        self.table_packages.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_packages.setAlternatingRowColors(True)
        self.table_packages.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_packages.setObjectName("table_packages")
        self.table_packages.setColumnCount(3)
        self.table_packages.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_packages.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_packages.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_packages.setHorizontalHeaderItem(2, item)
        self.table_packages.horizontalHeader().setStretchLastSection(False)
        self.table_packages.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.table_packages)
        self.label_status = QtWidgets.QLabel(Form)
        self.label_status.setObjectName("label_status")
        self.verticalLayout_2.addWidget(self.label_status)
        self.progress_bar = QtWidgets.QProgressBar(Form)
        self.progress_bar.setMaximum(0)
        self.progress_bar.setProperty("value", -1)
        self.progress_bar.setObjectName("progress_bar")
        self.verticalLayout_2.addWidget(self.progress_bar)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.bt_add_packages = QtWidgets.QToolButton(Form)
        self.bt_add_packages.setText("")
        icon = QtGui.QIcon.fromTheme("list-add")
        self.bt_add_packages.setIcon(icon)
        self.bt_add_packages.setObjectName("bt_add_packages")
        self.verticalLayout.addWidget(self.bt_add_packages)
        self.bt_rm_package = QtWidgets.QToolButton(Form)
        self.bt_rm_package.setText("")
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.bt_rm_package.setIcon(icon)
        self.bt_rm_package.setObjectName("bt_rm_package")
        self.verticalLayout.addWidget(self.bt_rm_package)
        self.bt_update_package = QtWidgets.QToolButton(Form)
        self.bt_update_package.setText("")
        icon = QtGui.QIcon.fromTheme("go-up")
        self.bt_update_package.setIcon(icon)
        self.bt_update_package.setObjectName("bt_update_package")
        self.verticalLayout.addWidget(self.bt_update_package)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        from hackedit.application.i18n import get_translation
        _ = get_translation(package="hackedit")
        Form.setWindowTitle(_("Form"))
        self.table_packages.setToolTip(_("The list of installed package for the selected interpreter."))
        self.table_packages.setSortingEnabled(True)
        item = self.table_packages.horizontalHeaderItem(0)
        item.setText(_("Name"))
        item = self.table_packages.horizontalHeaderItem(1)
        item.setText(_("Version"))
        item = self.table_packages.horizontalHeaderItem(2)
        item.setText(_("Latest"))
        self.label_status.setText(_("Updating package list"))
        self.bt_add_packages.setToolTip(_("Install one or more packages"))
        self.bt_rm_package.setToolTip(_("Uninstall selected package"))
        self.bt_update_package.setToolTip(_("Update selected package"))

