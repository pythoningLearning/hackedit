# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/Documents/hackedit/data/forms/settings_page_build_and_run.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1205, 847)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tab_categories = QtWidgets.QTabWidget(Form)
        self.tab_categories.setObjectName("tab_categories")
        self.tab_compilers = QtWidgets.QWidget()
        self.tab_compilers.setObjectName("tab_compilers")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_compilers)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_4.setSpacing(9)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tree_compilers = QtWidgets.QTreeWidget(self.tab_compilers)
        self.tree_compilers.setObjectName("tree_compilers")
        item_0 = QtWidgets.QTreeWidgetItem(self.tree_compilers)
        item_0 = QtWidgets.QTreeWidgetItem(self.tree_compilers)
        self.tree_compilers.header().setCascadingSectionResizes(False)
        self.tree_compilers.header().setDefaultSectionSize(250)
        self.verticalLayout_4.addWidget(self.tree_compilers)
        self.tab_compiler_settings = QtWidgets.QTabWidget(self.tab_compilers)
        self.tab_compiler_settings.setObjectName("tab_compiler_settings")
        self.tab_compiler_setup = QtWidgets.QWidget()
        self.tab_compiler_setup.setObjectName("tab_compiler_setup")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_compiler_setup)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(6, 6, 6, 6)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.tab_compiler_setup)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edit_compiler = PathLineEdit(self.tab_compiler_setup)
        self.edit_compiler.setObjectName("edit_compiler")
        self.horizontalLayout.addWidget(self.edit_compiler)
        self.bt_select_compiler = QtWidgets.QToolButton(self.tab_compiler_setup)
        self.bt_select_compiler.setObjectName("bt_select_compiler")
        self.horizontalLayout.addWidget(self.bt_select_compiler)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.verticalLayout_5.addLayout(self.formLayout)
        self.group_msvc = QtWidgets.QGroupBox(self.tab_compiler_setup)
        self.group_msvc.setCheckable(True)
        self.group_msvc.setChecked(False)
        self.group_msvc.setObjectName("group_msvc")
        self.formLayout_2 = QtWidgets.QFormLayout(self.group_msvc)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_vcvarsall = QtWidgets.QLabel(self.group_msvc)
        self.label_vcvarsall.setObjectName("label_vcvarsall")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_vcvarsall)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.edit_vcvarsall = QtWidgets.QLineEdit(self.group_msvc)
        self.edit_vcvarsall.setObjectName("edit_vcvarsall")
        self.horizontalLayout_2.addWidget(self.edit_vcvarsall)
        self.bt_select_vcvarsall = QtWidgets.QToolButton(self.group_msvc)
        self.bt_select_vcvarsall.setObjectName("bt_select_vcvarsall")
        self.horizontalLayout_2.addWidget(self.bt_select_vcvarsall)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label = QtWidgets.QLabel(self.group_msvc)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.combo_vcvarsall_arch = QtWidgets.QComboBox(self.group_msvc)
        self.combo_vcvarsall_arch.setObjectName("combo_vcvarsall_arch")
        self.combo_vcvarsall_arch.addItem("")
        self.combo_vcvarsall_arch.addItem("")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.combo_vcvarsall_arch)
        self.verticalLayout_5.addWidget(self.group_msvc)
        self.groupBox = QtWidgets.QGroupBox(self.tab_compiler_setup)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.table_env_vars = QtWidgets.QTableWidget(self.groupBox)
        self.table_env_vars.setMinimumSize(QtCore.QSize(0, 0))
        self.table_env_vars.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_env_vars.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_env_vars.setObjectName("table_env_vars")
        self.table_env_vars.setColumnCount(2)
        self.table_env_vars.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_env_vars.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_env_vars.setHorizontalHeaderItem(1, item)
        self.table_env_vars.horizontalHeader().setDefaultSectionSize(150)
        self.table_env_vars.horizontalHeader().setStretchLastSection(True)
        self.table_env_vars.verticalHeader().setVisible(False)
        self.table_env_vars.verticalHeader().setCascadingSectionResizes(False)
        self.horizontalLayout_4.addWidget(self.table_env_vars)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.bt_add_env_var = QtWidgets.QPushButton(self.groupBox)
        self.bt_add_env_var.setText("")
        icon = QtGui.QIcon.fromTheme("list-add")
        self.bt_add_env_var.setIcon(icon)
        self.bt_add_env_var.setObjectName("bt_add_env_var")
        self.verticalLayout_3.addWidget(self.bt_add_env_var)
        self.bt_rm_env_var = QtWidgets.QPushButton(self.groupBox)
        self.bt_rm_env_var.setText("")
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.bt_rm_env_var.setIcon(icon)
        self.bt_rm_env_var.setObjectName("bt_rm_env_var")
        self.verticalLayout_3.addWidget(self.bt_rm_env_var)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_5.addWidget(self.groupBox)
        self.tab_compiler_settings.addTab(self.tab_compiler_setup, "")
        self.tab_default_options = QtWidgets.QWidget()
        self.tab_default_options.setObjectName("tab_default_options")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_default_options)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.stacked_compiler_options = QtWidgets.QStackedWidget(self.tab_default_options)
        self.stacked_compiler_options.setObjectName("stacked_compiler_options")
        self.gridLayout.addWidget(self.stacked_compiler_options, 0, 0, 1, 1)
        self.tab_compiler_settings.addTab(self.tab_default_options, "")
        self.verticalLayout_4.addWidget(self.tab_compiler_settings)
        self.verticalLayout_4.setStretch(0, 1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.line_2 = QtWidgets.QFrame(self.tab_compilers)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_3.addWidget(self.line_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.bt_add_compiler = QtWidgets.QToolButton(self.tab_compilers)
        self.bt_add_compiler.setMinimumSize(QtCore.QSize(100, 0))
        icon = QtGui.QIcon.fromTheme("list-add")
        self.bt_add_compiler.setIcon(icon)
        self.bt_add_compiler.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.bt_add_compiler.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.bt_add_compiler.setObjectName("bt_add_compiler")
        self.verticalLayout_2.addWidget(self.bt_add_compiler)
        self.bt_clone_compiler = QtWidgets.QPushButton(self.tab_compilers)
        self.bt_clone_compiler.setMinimumSize(QtCore.QSize(100, 0))
        icon = QtGui.QIcon.fromTheme("edit-copy")
        self.bt_clone_compiler.setIcon(icon)
        self.bt_clone_compiler.setObjectName("bt_clone_compiler")
        self.verticalLayout_2.addWidget(self.bt_clone_compiler)
        self.bt_delete_compiler = QtWidgets.QPushButton(self.tab_compilers)
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.bt_delete_compiler.setIcon(icon)
        self.bt_delete_compiler.setObjectName("bt_delete_compiler")
        self.verticalLayout_2.addWidget(self.bt_delete_compiler)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.bt_check_compiler = QtWidgets.QPushButton(self.tab_compilers)
        icon = QtGui.QIcon.fromTheme("checkbox")
        self.bt_check_compiler.setIcon(icon)
        self.bt_check_compiler.setObjectName("bt_check_compiler")
        self.verticalLayout_2.addWidget(self.bt_check_compiler)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.tab_categories.addTab(self.tab_compilers, "")
        self.tab_pre_compilers = QtWidgets.QWidget()
        self.tab_pre_compilers.setObjectName("tab_pre_compilers")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab_pre_compilers)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_6.setSpacing(9)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.tree_pre_compilers = QtWidgets.QTreeWidget(self.tab_pre_compilers)
        self.tree_pre_compilers.setObjectName("tree_pre_compilers")
        item_0 = QtWidgets.QTreeWidgetItem(self.tree_pre_compilers)
        item_0 = QtWidgets.QTreeWidgetItem(self.tree_pre_compilers)
        self.tree_pre_compilers.header().setCascadingSectionResizes(False)
        self.tree_pre_compilers.header().setDefaultSectionSize(250)
        self.verticalLayout_6.addWidget(self.tree_pre_compilers)
        self.group_pre_compiler_settings = QtWidgets.QGroupBox(self.tab_pre_compilers)
        self.group_pre_compiler_settings.setObjectName("group_pre_compiler_settings")
        self.formLayout_3 = QtWidgets.QFormLayout(self.group_pre_compiler_settings)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_3 = QtWidgets.QLabel(self.group_pre_compiler_settings)
        self.label_3.setObjectName("label_3")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(self.group_pre_compiler_settings)
        self.label_4.setObjectName("label_4")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(self.group_pre_compiler_settings)
        self.label_5.setObjectName("label_5")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.label_7 = QtWidgets.QLabel(self.group_pre_compiler_settings)
        self.label_7.setObjectName("label_7")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.edit_pre_compiler_path = QtWidgets.QLineEdit(self.group_pre_compiler_settings)
        self.edit_pre_compiler_path.setObjectName("edit_pre_compiler_path")
        self.horizontalLayout_6.addWidget(self.edit_pre_compiler_path)
        self.bt_select_pre_compiler_path = QtWidgets.QToolButton(self.group_pre_compiler_settings)
        self.bt_select_pre_compiler_path.setObjectName("bt_select_pre_compiler_path")
        self.horizontalLayout_6.addWidget(self.bt_select_pre_compiler_path)
        self.formLayout_3.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_6)
        self.edit_pre_compiler_extensions = QtWidgets.QLineEdit(self.group_pre_compiler_settings)
        self.edit_pre_compiler_extensions.setObjectName("edit_pre_compiler_extensions")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.edit_pre_compiler_extensions)
        self.edit_pre_compiler_flags = QtWidgets.QLineEdit(self.group_pre_compiler_settings)
        self.edit_pre_compiler_flags.setObjectName("edit_pre_compiler_flags")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.edit_pre_compiler_flags)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.group_pre_compiler_settings)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.verticalLayout_6.addWidget(self.group_pre_compiler_settings)
        self.verticalLayout_6.setStretch(0, 1)
        self.horizontalLayout_5.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.bt_add_pre_compiler = QtWidgets.QToolButton(self.tab_pre_compilers)
        self.bt_add_pre_compiler.setMinimumSize(QtCore.QSize(100, 0))
        icon = QtGui.QIcon.fromTheme("list-add")
        self.bt_add_pre_compiler.setIcon(icon)
        self.bt_add_pre_compiler.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.bt_add_pre_compiler.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.bt_add_pre_compiler.setObjectName("bt_add_pre_compiler")
        self.verticalLayout_7.addWidget(self.bt_add_pre_compiler)
        self.bt_clone_pre_compiler = QtWidgets.QPushButton(self.tab_pre_compilers)
        self.bt_clone_pre_compiler.setMinimumSize(QtCore.QSize(100, 0))
        icon = QtGui.QIcon.fromTheme("edit-copy")
        self.bt_clone_pre_compiler.setIcon(icon)
        self.bt_clone_pre_compiler.setObjectName("bt_clone_pre_compiler")
        self.verticalLayout_7.addWidget(self.bt_clone_pre_compiler)
        self.bt_delete_pre_compiler = QtWidgets.QPushButton(self.tab_pre_compilers)
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.bt_delete_pre_compiler.setIcon(icon)
        self.bt_delete_pre_compiler.setObjectName("bt_delete_pre_compiler")
        self.verticalLayout_7.addWidget(self.bt_delete_pre_compiler)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem2)
        self.bt_check_pre_compiler = QtWidgets.QPushButton(self.tab_pre_compilers)
        icon = QtGui.QIcon.fromTheme("checkbox")
        self.bt_check_pre_compiler.setIcon(icon)
        self.bt_check_pre_compiler.setObjectName("bt_check_pre_compiler")
        self.verticalLayout_7.addWidget(self.bt_check_pre_compiler)
        self.horizontalLayout_5.addLayout(self.verticalLayout_7)
        self.tab_categories.addTab(self.tab_pre_compilers, "")
        self.tab_interpreters = QtWidgets.QWidget()
        self.tab_interpreters.setObjectName("tab_interpreters")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_interpreters)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_6 = QtWidgets.QLabel(self.tab_interpreters)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 0, 0, 1, 1)
        self.tab_categories.addTab(self.tab_interpreters, "")
        self.verticalLayout.addWidget(self.tab_categories)

        self.retranslateUi(Form)
        self.tab_categories.setCurrentIndex(0)
        self.tab_compiler_settings.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        from hackedit.api.gettext import get_translation
        _ = get_translation(package="hackedit")
        Form.setWindowTitle(_("Form"))
        self.tree_compilers.headerItem().setText(0, _("Name"))
        self.tree_compilers.headerItem().setText(1, _("Type"))
        self.tree_compilers.headerItem().setText(2, _("Version"))
        __sortingEnabled = self.tree_compilers.isSortingEnabled()
        self.tree_compilers.setSortingEnabled(False)
        self.tree_compilers.topLevelItem(0).setText(0, _("Auto-detected"))
        self.tree_compilers.topLevelItem(1).setText(0, _("Manual"))
        self.tree_compilers.setSortingEnabled(__sortingEnabled)
        self.label_2.setText(_("Compiler:"))
        self.bt_select_compiler.setToolTip(_("Select compiler"))
        self.bt_select_compiler.setText(_("..."))
        self.group_msvc.setToolTip(_("Check this if you\'re using a MSVC based compiler."))
        self.group_msvc.setTitle(_("MSVC S&upport"))
        self.label_vcvarsall.setText(_("VCVARSALL:"))
        self.bt_select_vcvarsall.setToolTip(_("Select vcvarsall.bat if the compiler is a MSVC based compiler."))
        self.bt_select_vcvarsall.setText(_("..."))
        self.label.setText(_("Architecture:"))
        self.combo_vcvarsall_arch.setItemText(0, _("x86"))
        self.combo_vcvarsall_arch.setItemText(1, _("x64"))
        self.groupBox.setTitle(_("Environment"))
        self.table_env_vars.setToolTip(_("<html><head/><body><p>The list of environment variables to set before compiling a file.</p><p>Note that the values defined in this list erase any previous value you might have defined in your system (empty values are not set).</p><p><br/></p></body></html>"))
        item = self.table_env_vars.horizontalHeaderItem(0)
        item.setText(_("Key"))
        item = self.table_env_vars.horizontalHeaderItem(1)
        item.setText(_("Value"))
        self.bt_add_env_var.setToolTip(_("Add an environment variable to set on the compiler process."))
        self.bt_rm_env_var.setToolTip(_("Remove the selected environment variable."))
        self.tab_compiler_settings.setTabText(self.tab_compiler_settings.indexOf(self.tab_compiler_setup), _("Setup"))
        self.tab_compiler_settings.setTabText(self.tab_compiler_settings.indexOf(self.tab_default_options), _("Default options"))
        self.bt_add_compiler.setToolTip(_("<html><head/><body><p>Add a new compiler</p></body></html>"))
        self.bt_add_compiler.setText(_("Add"))
        self.bt_clone_compiler.setToolTip(_("Clone the selected compiler"))
        self.bt_clone_compiler.setText(_("Clone"))
        self.bt_delete_compiler.setToolTip(_("Delete the selected compiler"))
        self.bt_delete_compiler.setText(_("Delete"))
        self.bt_check_compiler.setToolTip(_("Check if the selected compiler works"))
        self.bt_check_compiler.setText(_("Check"))
        self.tab_categories.setTabText(self.tab_categories.indexOf(self.tab_compilers), _("Compilers"))
        self.tab_categories.setTabToolTip(self.tab_categories.indexOf(self.tab_compilers), _("This tab lets you configure compilers used by the hackedit build system."))
        self.tree_pre_compilers.headerItem().setText(0, _("Name"))
        self.tree_pre_compilers.headerItem().setText(1, _("Type"))
        self.tree_pre_compilers.headerItem().setText(2, _("Version"))
        __sortingEnabled = self.tree_pre_compilers.isSortingEnabled()
        self.tree_pre_compilers.setSortingEnabled(False)
        self.tree_pre_compilers.topLevelItem(0).setText(0, _("Auto-detected"))
        self.tree_pre_compilers.topLevelItem(1).setText(0, _("Manual"))
        self.tree_pre_compilers.setSortingEnabled(__sortingEnabled)
        self.group_pre_compiler_settings.setTitle(_("Settings"))
        self.label_3.setText(_("Path:"))
        self.label_4.setText(_("Associated extensions:"))
        self.label_5.setText(_("Flags:"))
        self.label_7.setText(_("Output pattern:"))
        self.bt_select_pre_compiler_path.setText(_("..."))
        self.bt_add_pre_compiler.setToolTip(_("<html><head/><body><p>Add a new compiler</p></body></html>"))
        self.bt_add_pre_compiler.setText(_("Add"))
        self.bt_clone_pre_compiler.setToolTip(_("Clone the selected compiler"))
        self.bt_clone_pre_compiler.setText(_("Clone"))
        self.bt_delete_pre_compiler.setToolTip(_("Delete the selected compiler"))
        self.bt_delete_pre_compiler.setText(_("Delete"))
        self.bt_check_pre_compiler.setToolTip(_("Check if the selected compiler works"))
        self.bt_check_pre_compiler.setText(_("Check"))
        self.tab_categories.setTabText(self.tab_categories.indexOf(self.tab_pre_compilers), _("Pre-compilers"))
        self.tab_categories.setTabToolTip(self.tab_categories.indexOf(self.tab_pre_compilers), _("<html><head/><body><p>This tab let your configure pre-compilers or transpilers used by the hackedit\'s build system</p><p><br/></p><p>Pre-compilers are tools that process a source file into another source file (e.g. sass, flex, bison or any tools that let you extend a language with custom syntax).</p><p><br/></p><p>The pre-compiler pass will alaways occur before the compiler pass.</p></body></html>"))
        self.label_6.setText(_("Not Implemented"))
        self.tab_categories.setTabText(self.tab_categories.indexOf(self.tab_interpreters), _("Interpeters"))

from hackedit.api.widgets import PathLineEdit
