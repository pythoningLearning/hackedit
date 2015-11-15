# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/dev/hackedit/data/forms/settings_page_mimetypes.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(678, 390)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.table_mimes = QtWidgets.QTableWidget(self.groupBox)
        self.table_mimes.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_mimes.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_mimes.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_mimes.setShowGrid(True)
        self.table_mimes.setCornerButtonEnabled(False)
        self.table_mimes.setObjectName("table_mimes")
        self.table_mimes.setColumnCount(2)
        self.table_mimes.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.table_mimes.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_mimes.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_mimes.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_mimes.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_mimes.setItem(0, 1, item)
        self.table_mimes.horizontalHeader().setVisible(True)
        self.table_mimes.horizontalHeader().setCascadingSectionResizes(True)
        self.table_mimes.horizontalHeader().setDefaultSectionSize(200)
        self.table_mimes.horizontalHeader().setHighlightSections(False)
        self.table_mimes.horizontalHeader().setStretchLastSection(True)
        self.table_mimes.verticalHeader().setVisible(False)
        self.table_mimes.verticalHeader().setHighlightSections(False)
        self.gridLayout.addWidget(self.table_mimes, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.edit_mime_extensions = QtWidgets.QLineEdit(self.groupBox)
        self.edit_mime_extensions.setObjectName("edit_mime_extensions")
        self.horizontalLayout_2.addWidget(self.edit_mime_extensions)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.edit_filter = PromptLineEdit(self.groupBox)
        self.edit_filter.setObjectName("edit_filter")
        self.gridLayout.addWidget(self.edit_filter, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.edit_ignored = QtWidgets.QLineEdit(self.groupBox_2)
        self.edit_ignored.setObjectName("edit_ignored")
        self.gridLayout_2.addWidget(self.edit_ignored, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        import gettext
        def _translate(_, string):
            return gettext.gettext(string)

        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Recognized mimetypes"))
        self.table_mimes.setToolTip(_translate("Form", "The list of mimetypes and their handler"))
        item = self.table_mimes.verticalHeaderItem(0)
        item.setText(_translate("Form", "0"))
        item = self.table_mimes.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Mimetype"))
        item = self.table_mimes.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Handler"))
        __sortingEnabled = self.table_mimes.isSortingEnabled()
        self.table_mimes.setSortingEnabled(False)
        item = self.table_mimes.item(0, 0)
        item.setText(_translate("Form", "text/x-python"))
        item = self.table_mimes.item(0, 1)
        item.setText(_translate("Form", "PyCodeEdit"))
        self.table_mimes.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("Form", "Patterns:"))
        self.edit_mime_extensions.setToolTip(_translate("Form", "Mimetype patterns (separated by ;)"))
        self.groupBox_2.setTitle(_translate("Form", "Ignored files and directories"))
        self.edit_ignored.setToolTip(_translate("Form", "<html><head/><body><p>The list of ignore patterns (each pattern must be separated by a semi-colon ;)</p></body></html>"))

from pyqode.core.widgets import PromptLineEdit
