# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/dev/hackedit/data/forms/settings_page_environment.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(664, 608)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 652, 596))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_3 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_3)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.spin_toolbar_icon_size = QtWidgets.QSpinBox(self.groupBox_3)
        self.spin_toolbar_icon_size.setMinimum(16)
        self.spin_toolbar_icon_size.setMaximum(32)
        self.spin_toolbar_icon_size.setObjectName("spin_toolbar_icon_size")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spin_toolbar_icon_size)
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.combo_theme = QtWidgets.QComboBox(self.groupBox_3)
        self.combo_theme.setObjectName("combo_theme")
        self.combo_theme.addItem("")
        self.combo_theme.addItem("")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.combo_theme)
        self.cb_system_tray_icon = QtWidgets.QCheckBox(self.groupBox_3)
        self.cb_system_tray_icon.setObjectName("cb_system_tray_icon")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cb_system_tray_icon)
        self.cb_widescreen = QtWidgets.QCheckBox(self.groupBox_3)
        self.cb_widescreen.setObjectName("cb_widescreen")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.cb_widescreen)
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.combo_icon_themes = QtWidgets.QComboBox(self.groupBox_3)
        self.combo_icon_themes.setObjectName("combo_icon_themes")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.combo_icon_themes)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.group_system = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.group_system.setObjectName("group_system")
        self.formLayout = QtWidgets.QFormLayout(self.group_system)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtWidgets.QLabel(self.group_system)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.edit_run_command_in_terminal = QtWidgets.QLineEdit(self.group_system)
        self.edit_run_command_in_terminal.setObjectName("edit_run_command_in_terminal")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.edit_run_command_in_terminal)
        self.label = QtWidgets.QLabel(self.group_system)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.edit_open_folder_in_terminal = QtWidgets.QLineEdit(self.group_system)
        self.edit_open_folder_in_terminal.setText("")
        self.edit_open_folder_in_terminal.setObjectName("edit_open_folder_in_terminal")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.edit_open_folder_in_terminal)
        self.label_2 = QtWidgets.QLabel(self.group_system)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.edit_file_manager = QtWidgets.QLineEdit(self.group_system)
        self.edit_file_manager.setText("")
        self.edit_file_manager.setObjectName("edit_file_manager")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.edit_file_manager)
        self.label_3 = QtWidgets.QLabel(self.group_system)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cb_use_default_browser = QtWidgets.QCheckBox(self.group_system)
        self.cb_use_default_browser.setChecked(True)
        self.cb_use_default_browser.setObjectName("cb_use_default_browser")
        self.horizontalLayout.addWidget(self.cb_use_default_browser)
        self.edit_browser_command = QtWidgets.QLineEdit(self.group_system)
        self.edit_browser_command.setEnabled(False)
        self.edit_browser_command.setObjectName("edit_browser_command")
        self.horizontalLayout.addWidget(self.edit_browser_command)
        self.formLayout.setLayout(4, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.verticalLayout_3.addWidget(self.group_system)
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.table = QtWidgets.QTableWidget(self.groupBox)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setObjectName("table")
        self.table.setColumnCount(2)
        self.table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        self.table.horizontalHeader().setCascadingSectionResizes(True)
        self.table.horizontalHeader().setSortIndicatorShown(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.horizontalLayout_2.addWidget(self.table)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.bt_add = QtWidgets.QToolButton(self.groupBox)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.bt_add.setIcon(icon)
        self.bt_add.setObjectName("bt_add")
        self.verticalLayout_2.addWidget(self.bt_add)
        self.bt_remove = QtWidgets.QToolButton(self.groupBox)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.bt_remove.setIcon(icon)
        self.bt_remove.setObjectName("bt_remove")
        self.verticalLayout_2.addWidget(self.bt_remove)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        import gettext
        def _translate(_, string):
            return gettext.gettext(string)

        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_3.setTitle(_translate("Form", "User Interface"))
        self.label_6.setText(_translate("Form", "Toolbar icon size:"))
        self.spin_toolbar_icon_size.setToolTip(_translate("Form", "Size of the toolbar items"))
        self.label_5.setText(_translate("Form", "Theme:"))
        self.combo_theme.setToolTip(_translate("Form", "Switch between native and dark theme"))
        self.combo_theme.setItemText(0, _translate("Form", "Native"))
        self.combo_theme.setItemText(1, _translate("Form", "Dark"))
        self.cb_system_tray_icon.setToolTip(_translate("Form", "Show/Hide system tray icon (needed to display notifications on Windows and OSX)."))
        self.cb_system_tray_icon.setText(_translate("Form", "Show system tray icon"))
        self.cb_widescreen.setToolTip(_translate("Form", "Use a widescreen layout for the dock widgets (lateral panels will take the whole height of the window)"))
        self.cb_widescreen.setText(_translate("Form", "Use widescreen layout"))
        self.label_7.setText(_translate("Form", "Icon theme:"))
        self.combo_icon_themes.setToolTip(_translate("Form", "Select the icon theme."))
        self.group_system.setTitle(_translate("Form", "System commands"))
        self.label_4.setText(_translate("Form", "Run command in terminal:"))
        self.edit_run_command_in_terminal.setToolTip(_translate("Form", "<html><head/><body><p>The command for running a program in an external terminal</p><p>Use %s to indicate file path argument, e.g.: &quot;konsole -e %s&quot;</p></body></html>"))
        self.label.setText(_translate("Form", "Open folder in terminal:"))
        self.edit_open_folder_in_terminal.setToolTip(_translate("Form", "<html><head/><body><p>The command for opening folders in terminal.</p><p>Use %s to indicate file path argument, e.g.: &quot;konsole --workdir %s&quot;</p></body></html>"))
        self.label_2.setText(_translate("Form", "Open in file manager:"))
        self.edit_file_manager.setToolTip(_translate("Form", "<html><head/><body><p>The command for opening files in a file manager.</p><p>Use %s to indicate file path argument, e.g.: &quot;dolphin --select %s&quot;</p></body></html>"))
        self.label_3.setText(_translate("Form", "Open in web browser:"))
        self.cb_use_default_browser.setToolTip(_translate("Form", "<html><head/><body><p>If checked, the system default browser will be used. Otherwise you need to specify the command.</p></body></html>"))
        self.cb_use_default_browser.setText(_translate("Form", "Use system browser"))
        self.groupBox.setTitle(_translate("Form", "Environment variables"))
        self.table.setToolTip(_translate("Form", "<html><head/><body><p>The list of environment variables.</p><p><br/></p></body></html>"))
        self.table.setSortingEnabled(True)
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Key"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Value"))
        self.bt_add.setToolTip(_translate("Form", "Add an environment variable"))
        self.bt_add.setText(_translate("Form", "..."))
        self.bt_remove.setToolTip(_translate("Form", "Remove the selected environment variable."))
        self.bt_remove.setText(_translate("Form", "..."))

