# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/Colin/Documents/hackedit/data/forms/dlg_script_run_config.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(783, 494)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(-1, 0, -1, -1)
        self.formLayout.setObjectName("formLayout")
        self.label_prj_interpreter = QtWidgets.QLabel(Dialog)
        self.label_prj_interpreter.setObjectName("label_prj_interpreter")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_prj_interpreter)
        self.combo_prj_interpreter = QtWidgets.QComboBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_prj_interpreter.sizePolicy().hasHeightForWidth())
        self.combo_prj_interpreter.setSizePolicy(sizePolicy)
        self.combo_prj_interpreter.setObjectName("combo_prj_interpreter")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.combo_prj_interpreter)
        self.label_project = QtWidgets.QLabel(Dialog)
        self.label_project.setObjectName("label_project")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_project)
        self.cb_project = QtWidgets.QComboBox(Dialog)
        self.cb_project.setObjectName("cb_project")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cb_project)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.group_configs = QtWidgets.QGroupBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.group_configs.sizePolicy().hasHeightForWidth())
        self.group_configs.setSizePolicy(sizePolicy)
        self.group_configs.setFlat(False)
        self.group_configs.setCheckable(False)
        self.group_configs.setObjectName("group_configs")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.group_configs)
        self.horizontalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.list_configs = QtWidgets.QListWidget(self.group_configs)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_configs.sizePolicy().hasHeightForWidth())
        self.list_configs.setSizePolicy(sizePolicy)
        self.list_configs.setObjectName("list_configs")
        self.horizontalLayout_7.addWidget(self.list_configs)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.bt_add_cfg = QtWidgets.QToolButton(self.group_configs)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_add_cfg.sizePolicy().hasHeightForWidth())
        self.bt_add_cfg.setSizePolicy(sizePolicy)
        self.bt_add_cfg.setText("")
        icon = QtGui.QIcon.fromTheme("list-add")
        self.bt_add_cfg.setIcon(icon)
        self.bt_add_cfg.setObjectName("bt_add_cfg")
        self.verticalLayout_3.addWidget(self.bt_add_cfg)
        self.bt_rm_cfg = QtWidgets.QToolButton(self.group_configs)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_rm_cfg.sizePolicy().hasHeightForWidth())
        self.bt_rm_cfg.setSizePolicy(sizePolicy)
        self.bt_rm_cfg.setText("")
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.bt_rm_cfg.setIcon(icon)
        self.bt_rm_cfg.setObjectName("bt_rm_cfg")
        self.verticalLayout_3.addWidget(self.bt_rm_cfg)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout_7.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2.addWidget(self.group_configs)
        self.group_settings = QtWidgets.QGroupBox(Dialog)
        self.group_settings.setObjectName("group_settings")
        self.formLayout_2 = QtWidgets.QFormLayout(self.group_settings)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_7 = QtWidgets.QLabel(self.group_settings)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.edit_name = QtWidgets.QLineEdit(self.group_settings)
        self.edit_name.setObjectName("edit_name")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.edit_name)
        self.label = QtWidgets.QLabel(self.group_settings)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.edit_script = PathLineEdit(self.group_settings)
        self.edit_script.setObjectName("edit_script")
        self.horizontalLayout_5.addWidget(self.edit_script)
        self.bt_pick_script = QtWidgets.QToolButton(self.group_settings)
        self.bt_pick_script.setObjectName("bt_pick_script")
        self.horizontalLayout_5.addWidget(self.bt_pick_script)
        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label_2 = QtWidgets.QLabel(self.group_settings)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.edit_script_args = QtWidgets.QLineEdit(self.group_settings)
        self.edit_script_args.setObjectName("edit_script_args")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.edit_script_args)
        self.label_5 = QtWidgets.QLabel(self.group_settings)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.edit_working_dir = PathLineEdit(self.group_settings)
        self.edit_working_dir.setObjectName("edit_working_dir")
        self.horizontalLayout_6.addWidget(self.edit_working_dir)
        self.bt_pick_working_dir = QtWidgets.QToolButton(self.group_settings)
        self.bt_pick_working_dir.setObjectName("bt_pick_working_dir")
        self.horizontalLayout_6.addWidget(self.bt_pick_working_dir)
        self.formLayout_2.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_6)
        self.label_4 = QtWidgets.QLabel(self.group_settings)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.edit_intepreter_options = QtWidgets.QLineEdit(self.group_settings)
        self.edit_intepreter_options.setObjectName("edit_intepreter_options")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.edit_intepreter_options)
        self.label_6 = QtWidgets.QLabel(self.group_settings)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.table_env_vars = QtWidgets.QTableWidget(self.group_settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.table_env_vars.sizePolicy().hasHeightForWidth())
        self.table_env_vars.setSizePolicy(sizePolicy)
        self.table_env_vars.setAlternatingRowColors(False)
        self.table_env_vars.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_env_vars.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_env_vars.setGridStyle(QtCore.Qt.SolidLine)
        self.table_env_vars.setRowCount(0)
        self.table_env_vars.setObjectName("table_env_vars")
        self.table_env_vars.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.table_env_vars.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_env_vars.setHorizontalHeaderItem(1, item)
        self.table_env_vars.horizontalHeader().setCascadingSectionResizes(False)
        self.table_env_vars.horizontalHeader().setStretchLastSection(True)
        self.table_env_vars.verticalHeader().setVisible(False)
        self.horizontalLayout_4.addWidget(self.table_env_vars)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.bt_add_env_var = QtWidgets.QToolButton(self.group_settings)
        self.bt_add_env_var.setText("")
        icon = QtGui.QIcon.fromTheme("list-add")
        self.bt_add_env_var.setIcon(icon)
        self.bt_add_env_var.setObjectName("bt_add_env_var")
        self.verticalLayout_4.addWidget(self.bt_add_env_var)
        self.bt_rm_env_var = QtWidgets.QToolButton(self.group_settings)
        self.bt_rm_env_var.setText("")
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.bt_rm_env_var.setIcon(icon)
        self.bt_rm_env_var.setObjectName("bt_rm_env_var")
        self.verticalLayout_4.addWidget(self.bt_rm_env_var)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.formLayout_2.setLayout(5, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.cb_run_in_external_terminal = QtWidgets.QCheckBox(self.group_settings)
        self.cb_run_in_external_terminal.setObjectName("cb_run_in_external_terminal")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.cb_run_in_external_terminal)
        self.horizontalLayout_2.addWidget(self.group_settings)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.cb_project, self.combo_prj_interpreter)
        Dialog.setTabOrder(self.combo_prj_interpreter, self.bt_add_cfg)
        Dialog.setTabOrder(self.bt_add_cfg, self.bt_rm_cfg)
        Dialog.setTabOrder(self.bt_rm_cfg, self.edit_name)
        Dialog.setTabOrder(self.edit_name, self.edit_script)
        Dialog.setTabOrder(self.edit_script, self.bt_pick_script)
        Dialog.setTabOrder(self.bt_pick_script, self.edit_script_args)
        Dialog.setTabOrder(self.edit_script_args, self.edit_working_dir)
        Dialog.setTabOrder(self.edit_working_dir, self.bt_pick_working_dir)
        Dialog.setTabOrder(self.bt_pick_working_dir, self.edit_intepreter_options)
        Dialog.setTabOrder(self.edit_intepreter_options, self.table_env_vars)
        Dialog.setTabOrder(self.table_env_vars, self.bt_add_env_var)
        Dialog.setTabOrder(self.bt_add_env_var, self.bt_rm_env_var)
        Dialog.setTabOrder(self.bt_rm_env_var, self.list_configs)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Python run configuration"))
        self.label_prj_interpreter.setText(_translate("Dialog", "Project interpreter:"))
        self.combo_prj_interpreter.setToolTip(_translate("Dialog", "Select project interpreter"))
        self.label_project.setText(_translate("Dialog", "Project:"))
        self.cb_project.setToolTip(_translate("Dialog", "Select project to edit"))
        self.group_configs.setTitle(_translate("Dialog", "Configurations"))
        self.list_configs.setToolTip(_translate("Dialog", "List of available run configurations"))
        self.bt_add_cfg.setToolTip(_translate("Dialog", "Add new configuration"))
        self.bt_rm_cfg.setToolTip(_translate("Dialog", "Remove selected config"))
        self.group_settings.setTitle(_translate("Dialog", "Settings"))
        self.label_7.setText(_translate("Dialog", "Name:"))
        self.edit_name.setToolTip(_translate("Dialog", "Name of the configuration"))
        self.label.setText(_translate("Dialog", "Script:"))
        self.edit_script.setToolTip(_translate("Dialog", "Path to the script to run"))
        self.bt_pick_script.setToolTip(_translate("Dialog", "Choose script"))
        self.bt_pick_script.setText(_translate("Dialog", "..."))
        self.label_2.setText(_translate("Dialog", "Script parameters:"))
        self.edit_script_args.setToolTip(_translate("Dialog", "Script paramters"))
        self.label_5.setText(_translate("Dialog", "Working directory:"))
        self.edit_working_dir.setToolTip(_translate("Dialog", "Working directory"))
        self.bt_pick_working_dir.setToolTip(_translate("Dialog", "Choose working dir"))
        self.bt_pick_working_dir.setText(_translate("Dialog", "..."))
        self.label_4.setText(_translate("Dialog", "Interpreter options:"))
        self.edit_intepreter_options.setToolTip(_translate("Dialog", "Interpreter options"))
        self.label_6.setText(_translate("Dialog", "Environment variables"))
        self.table_env_vars.setToolTip(_translate("Dialog", "Environment variables to set on the run process"))
        self.table_env_vars.setSortingEnabled(True)
        item = self.table_env_vars.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Name"))
        item = self.table_env_vars.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Value"))
        self.bt_add_env_var.setToolTip(_translate("Dialog", "Add a new environment variable"))
        self.bt_rm_env_var.setToolTip(_translate("Dialog", "Remove the selected environment variable"))
        self.cb_run_in_external_terminal.setToolTip(_translate("Dialog", "Check this to run the script in an external terminal."))
        self.cb_run_in_external_terminal.setText(_translate("Dialog", "Run in external terminal"))

from hackedit.api.widgets import PathLineEdit
