# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/Documents/hackedit/data/forms/settings_page_behaviour.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(635, 478)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 623, 466))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.cb_splashscreen = QtWidgets.QCheckBox(self.groupBox)
        self.cb_splashscreen.setChecked(True)
        self.cb_splashscreen.setObjectName("cb_splashscreen")
        self.verticalLayout_3.addWidget(self.cb_splashscreen)
        self.cb_reopen = QtWidgets.QCheckBox(self.groupBox)
        self.cb_reopen.setChecked(True)
        self.cb_reopen.setObjectName("cb_reopen")
        self.verticalLayout_3.addWidget(self.cb_reopen)
        self.cb_restore_session = QtWidgets.QCheckBox(self.groupBox)
        self.cb_restore_session.setObjectName("cb_restore_session")
        self.verticalLayout_3.addWidget(self.cb_restore_session)
        self.cb_confirm_exit = QtWidgets.QCheckBox(self.groupBox)
        self.cb_confirm_exit.setChecked(True)
        self.cb_confirm_exit.setObjectName("cb_confirm_exit")
        self.verticalLayout_3.addWidget(self.cb_confirm_exit)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setEnabled(True)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.rb_open_proj_in_same = QtWidgets.QRadioButton(self.groupBox_3)
        self.rb_open_proj_in_same.setObjectName("rb_open_proj_in_same")
        self.verticalLayout_5.addWidget(self.rb_open_proj_in_same)
        self.rb_open_proj_in_new = QtWidgets.QRadioButton(self.groupBox_3)
        self.rb_open_proj_in_new.setChecked(False)
        self.rb_open_proj_in_new.setObjectName("rb_open_proj_in_new")
        self.verticalLayout_5.addWidget(self.rb_open_proj_in_new)
        self.rb_open_proj_ask = QtWidgets.QRadioButton(self.groupBox_3)
        self.rb_open_proj_ask.setChecked(True)
        self.rb_open_proj_ask.setObjectName("rb_open_proj_ask")
        self.verticalLayout_5.addWidget(self.rb_open_proj_ask)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.cb_check_for_updates = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_check_for_updates.setObjectName("cb_check_for_updates")
        self.verticalLayout_4.addWidget(self.cb_check_for_updates)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        from hackedit.application.i18n import get_translation
        _ = get_translation(package="hackedit")
        Form.setWindowTitle(_("Form"))
        self.groupBox.setTitle(_("Startup/Shutdown"))
        self.cb_splashscreen.setToolTip(_("Show/Hide splashscreen on application startup."))
        self.cb_splashscreen.setText(_("Show splash screen"))
        self.cb_reopen.setToolTip(_("Reopen most recent project automatically"))
        self.cb_reopen.setText(_("Reopen last window on startup"))
        self.cb_restore_session.setToolTip(_("Restore session (remember open files and current editor)"))
        self.cb_restore_session.setText(_("Restore session (remember open files and current index)"))
        self.cb_confirm_exit.setToolTip(_("Ask for confirmation before quitting the application."))
        self.cb_confirm_exit.setText(_("Confirm application exit "))
        self.groupBox_3.setTitle(_("Project opening"))
        self.rb_open_proj_in_same.setToolTip(_("<html><head/><body><p>Add project to the current window (add to currently open projects)</p></body></html>"))
        self.rb_open_proj_in_same.setText(_("Add &to currently open projects"))
        self.rb_open_proj_in_new.setToolTip(_("<html><head/><body><p>Open project in a new window.</p></body></html>"))
        self.rb_open_proj_in_new.setText(_("Open pro&ject in a new window"))
        self.rb_open_proj_ask.setToolTip(_("Always ask"))
        self.rb_open_proj_ask.setText(_("As&k each time"))
        self.groupBox_2.setTitle(_("Updates"))
        self.cb_check_for_updates.setToolTip(_("Check for updates on application startup"))
        self.cb_check_for_updates.setText(_("Automatically check for update on startup"))

