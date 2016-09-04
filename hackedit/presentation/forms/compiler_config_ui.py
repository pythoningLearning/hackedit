# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/Documents/hackedit/data/forms/compiler_config.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(715, 381)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.edit_flags = QtWidgets.QLineEdit(Form)
        self.edit_flags.setObjectName("edit_flags")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.edit_flags)
        self.label_18 = QtWidgets.QLabel(Form)
        self.label_18.setObjectName("label_18")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.edit_libs = QtWidgets.QLineEdit(Form)
        self.edit_libs.setObjectName("edit_libs")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.edit_libs)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.list_include_paths = QtWidgets.QListWidget(self.groupBox_2)
        self.list_include_paths.setObjectName("list_include_paths")
        self.horizontalLayout_2.addWidget(self.list_include_paths)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.bt_abs_include_path = QtWidgets.QToolButton(self.groupBox_2)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.bt_abs_include_path.setIcon(icon)
        self.bt_abs_include_path.setObjectName("bt_abs_include_path")
        self.verticalLayout_4.addWidget(self.bt_abs_include_path)
        self.bt_rel_include_path = QtWidgets.QToolButton(self.groupBox_2)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.bt_rel_include_path.setIcon(icon)
        self.bt_rel_include_path.setObjectName("bt_rel_include_path")
        self.verticalLayout_4.addWidget(self.bt_rel_include_path)
        self.bt_delete_include_path = QtWidgets.QToolButton(self.groupBox_2)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.bt_delete_include_path.setIcon(icon)
        self.bt_delete_include_path.setObjectName("bt_delete_include_path")
        self.verticalLayout_4.addWidget(self.bt_delete_include_path)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.list_lib_paths = QtWidgets.QListWidget(self.groupBox_3)
        self.list_lib_paths.setObjectName("list_lib_paths")
        self.horizontalLayout.addWidget(self.list_lib_paths)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.bt_abs_lib_path = QtWidgets.QToolButton(self.groupBox_3)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.bt_abs_lib_path.setIcon(icon)
        self.bt_abs_lib_path.setObjectName("bt_abs_lib_path")
        self.verticalLayout_5.addWidget(self.bt_abs_lib_path)
        self.bt_rel_lib_path = QtWidgets.QToolButton(self.groupBox_3)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.bt_rel_lib_path.setIcon(icon)
        self.bt_rel_lib_path.setObjectName("bt_rel_lib_path")
        self.verticalLayout_5.addWidget(self.bt_rel_lib_path)
        self.bt_delete_lib_path = QtWidgets.QToolButton(self.groupBox_3)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.bt_delete_lib_path.setIcon(icon)
        self.bt_delete_lib_path.setObjectName("bt_delete_lib_path")
        self.verticalLayout_5.addWidget(self.bt_delete_lib_path)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.horizontalLayout_3.addWidget(self.groupBox_3)
        self.groupBox_2.raise_()
        self.groupBox_3.raise_()
        self.list_lib_paths.raise_()
        self.verticalLayout.addWidget(self.groupBox)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        from hackedit.application.i18n import get_translation
        _ = get_translation(package="hackedit")
        Form.setWindowTitle(_("Form"))
        self.label.setText(_("Compiler flags:"))
        self.edit_flags.setToolTip(_("<html><head/><body><p>List of extra compiler flags. Each entry in the list must be separated by a white space.</p></body></html>"))
        self.label_18.setText(_("Libraries:"))
        self.edit_libs.setToolTip(_("<html><head/><body><p>The list of libraries you would like your programs to link with (-l option).</p><p>Each entry in the list must be separated by a white space</p></body></html>"))
        self.groupBox.setTitle(_("Paths"))
        self.groupBox_2.setTitle(_("Includes"))
        self.list_include_paths.setToolTip(_("<html><head/><body><p>The list of include paths</p></body></html>"))
        self.bt_abs_include_path.setToolTip(_("Add an absolute library path"))
        self.bt_abs_include_path.setText(_("..."))
        self.bt_rel_include_path.setToolTip(_("Add a relative library path"))
        self.bt_rel_include_path.setText(_("..."))
        self.bt_delete_include_path.setToolTip(_("Delete selected path"))
        self.bt_delete_include_path.setText(_("..."))
        self.groupBox_3.setTitle(_("Libraries"))
        self.list_lib_paths.setToolTip(_("<html><head/><body><p>The list of library paths.</p></body></html>"))
        self.bt_abs_lib_path.setToolTip(_("Add an absolute library path"))
        self.bt_abs_lib_path.setText(_("..."))
        self.bt_rel_lib_path.setToolTip(_("Add a relative library path"))
        self.bt_rel_lib_path.setText(_("..."))
        self.bt_delete_lib_path.setToolTip(_("Delete selected path"))
        self.bt_delete_lib_path.setText(_("..."))

