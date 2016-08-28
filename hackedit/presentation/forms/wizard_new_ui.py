# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/Documents/hackedit/data/forms/wizard_new.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        Wizard.setObjectName("Wizard")
        Wizard.resize(717, 414)
        Wizard.setWizardStyle(QtWidgets.QWizard.ClassicStyle)
        Wizard.setOptions(QtWidgets.QWizard.NoBackButtonOnStartPage)
        self.wizardPageHome = QtWidgets.QWizardPage()
        self.wizardPageHome.setObjectName("wizardPageHome")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.wizardPageHome)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.wizardPageHome)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.list_sources = QtWidgets.QListWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_sources.sizePolicy().hasHeightForWidth())
        self.list_sources.setSizePolicy(sizePolicy)
        self.list_sources.setObjectName("list_sources")
        self.gridLayout.addWidget(self.list_sources, 0, 0, 1, 1)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.line = QtWidgets.QFrame(self.wizardPageHome)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_3.addWidget(self.line)
        self.groupBox_2 = QtWidgets.QGroupBox(self.wizardPageHome)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tree_templates = QtWidgets.QTreeWidget(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_templates.sizePolicy().hasHeightForWidth())
        self.tree_templates.setSizePolicy(sizePolicy)
        self.tree_templates.setObjectName("tree_templates")
        item_0 = QtWidgets.QTreeWidgetItem(self.tree_templates)
        icon = QtGui.QIcon.fromTheme("folder")
        item_0.setIcon(0, icon)
        item_0 = QtWidgets.QTreeWidgetItem(self.tree_templates)
        icon = QtGui.QIcon.fromTheme("document")
        item_0.setIcon(0, icon)
        item_0 = QtWidgets.QTreeWidgetItem(self.tree_templates)
        icon = QtGui.QIcon.fromTheme("trash")
        item_0.setIcon(0, icon)
        self.tree_templates.header().setVisible(False)
        self.gridLayout_2.addWidget(self.tree_templates, 0, 0, 1, 1)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.lbl_boss_version = QtWidgets.QLabel(self.wizardPageHome)
        self.lbl_boss_version.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_boss_version.setOpenExternalLinks(True)
        self.lbl_boss_version.setObjectName("lbl_boss_version")
        self.verticalLayout.addWidget(self.lbl_boss_version)
        Wizard.addPage(self.wizardPageHome)
        self.wizardPageLocation = QtWidgets.QWizardPage()
        self.wizardPageLocation.setObjectName("wizardPageLocation")
        self.formLayout = QtWidgets.QFormLayout(self.wizardPageLocation)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.wizardPageLocation)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.edit_prj_path = PathLineEdit(self.wizardPageLocation)
        self.edit_prj_path.setObjectName("edit_prj_path")
        self.horizontalLayout_2.addWidget(self.edit_prj_path)
        self.bt_select_prj_path = QtWidgets.QToolButton(self.wizardPageLocation)
        self.bt_select_prj_path.setObjectName("bt_select_prj_path")
        self.horizontalLayout_2.addWidget(self.bt_select_prj_path)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.lbl_prj_location_error = QtWidgets.QLabel(self.wizardPageLocation)
        self.lbl_prj_location_error.setStyleSheet("background-color: red;\n"
"color: white;")
        self.lbl_prj_location_error.setObjectName("lbl_prj_location_error")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lbl_prj_location_error)
        Wizard.addPage(self.wizardPageLocation)

        self.retranslateUi(Wizard)
        QtCore.QMetaObject.connectSlotsByName(Wizard)
        Wizard.setTabOrder(self.list_sources, self.tree_templates)
        Wizard.setTabOrder(self.tree_templates, self.edit_prj_path)
        Wizard.setTabOrder(self.edit_prj_path, self.bt_select_prj_path)

    def retranslateUi(self, Wizard):
        from hackedit.api.i18n import get_translation
        _ = get_translation(package="hackedit")
        Wizard.setWindowTitle(_("New"))
        self.wizardPageHome.setTitle(_("Select template"))
        self.wizardPageHome.setSubTitle(_("Select a project or a single file template"))
        self.groupBox.setTitle(_("Sources"))
        self.list_sources.setToolTip(_("The list of template sources"))
        self.groupBox_2.setTitle(_("Templates"))
        self.tree_templates.setToolTip(_("The list of templates for the selected source"))
        self.tree_templates.headerItem().setText(0, _("Template"))
        __sortingEnabled = self.tree_templates.isSortingEnabled()
        self.tree_templates.setSortingEnabled(False)
        self.tree_templates.topLevelItem(0).setText(0, _("Project templates"))
        self.tree_templates.topLevelItem(1).setText(0, _("File templates"))
        self.tree_templates.topLevelItem(2).setText(0, _("Un-categorized templates"))
        self.tree_templates.setSortingEnabled(__sortingEnabled)
        self.lbl_boss_version.setText(_("Powered by BOSS v0.9.20"))
        self.wizardPageLocation.setTitle(_("Set location"))
        self.wizardPageLocation.setSubTitle(_("Set the location of the project/file"))
        self.label.setText(_("Create in:"))
        self.edit_prj_path.setToolTip(_("Select the project/file destination."))
        self.bt_select_prj_path.setText(_("Browse"))
        self.lbl_prj_location_error.setText(_("TextLabel"))

from hackedit.api.widgets import PathLineEdit
