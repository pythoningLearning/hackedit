# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/Documents/hackedit/data/forms/welcome_window.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(856, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/hackedit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.list_recents = RecentFilesListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_recents.sizePolicy().hasHeightForWidth())
        self.list_recents.setSizePolicy(sizePolicy)
        self.list_recents.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.list_recents.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.list_recents.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.list_recents.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list_recents.setProperty("showDropIndicator", False)
        self.list_recents.setAlternatingRowColors(True)
        self.list_recents.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.list_recents.setProperty("isWrapping", False)
        self.list_recents.setObjectName("list_recents")
        self.horizontalLayout.addWidget(self.list_recents)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_version = QtWidgets.QLabel(self.centralwidget)
        self.label_version.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_version.setAlignment(QtCore.Qt.AlignCenter)
        self.label_version.setObjectName("label_version")
        self.verticalLayout.addWidget(self.label_version)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setObjectName("label_title")
        self.verticalLayout_2.addWidget(self.label_title)
        self.bt_new = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_new.sizePolicy().hasHeightForWidth())
        self.bt_new.setSizePolicy(sizePolicy)
        self.bt_new.setMinimumSize(QtCore.QSize(240, 0))
        icon = QtGui.QIcon.fromTheme("document-new")
        self.bt_new.setIcon(icon)
        self.bt_new.setObjectName("bt_new")
        self.verticalLayout_2.addWidget(self.bt_new)
        self.bt_open = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_open.sizePolicy().hasHeightForWidth())
        self.bt_open.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.bt_open.setIcon(icon)
        self.bt_open.setObjectName("bt_open")
        self.verticalLayout_2.addWidget(self.bt_open)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.bt_quit = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon.fromTheme("application-exit")
        self.bt_quit.setIcon(icon)
        self.bt_quit.setObjectName("bt_quit")
        self.horizontalLayout_3.addWidget(self.bt_quit)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.bt_configure = QtWidgets.QToolButton(self.centralwidget)
        icon = QtGui.QIcon.fromTheme("preferences-system")
        self.bt_configure.setIcon(icon)
        self.bt_configure.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.bt_configure.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.bt_configure.setObjectName("bt_configure")
        self.horizontalLayout_3.addWidget(self.bt_configure)
        self.bt_help = QtWidgets.QToolButton(self.centralwidget)
        icon = QtGui.QIcon.fromTheme("system-help")
        self.bt_help.setIcon(icon)
        self.bt_help.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.bt_help.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.bt_help.setObjectName("bt_help")
        self.horizontalLayout_3.addWidget(self.bt_help)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        from hackedit.api.i18n import get_translation
        _ = get_translation(package="hackedit")
        MainWindow.setWindowTitle(_("Welcome to HackEdit"))
        self.list_recents.setToolTip(_("The list of recent documents/projects"))
        self.label_version.setText(_("Version %s"))
        self.label_title.setText(_("<html><head/><body><p align=\"center\"><img src=\":/icons/hackedit_128.png\"/></p><p align=\"center\"><span style=\" font-size:48pt;\">HackEdit</span></p></body></html>"))
        self.bt_new.setToolTip(_("Create a new file/project"))
        self.bt_new.setText(_("New"))
        self.bt_new.setShortcut(_("Ctrl+N"))
        self.bt_open.setToolTip(_("Open a project (directory)."))
        self.bt_open.setText(_("Open"))
        self.bt_open.setShortcut(_("Ctrl+O"))
        self.bt_quit.setToolTip(_("Quit application"))
        self.bt_quit.setText(_("Quit"))
        self.bt_quit.setShortcut(_("Ctrl+Q"))
        self.bt_configure.setToolTip(_("Edit preferences"))
        self.bt_configure.setText(_("Preferences"))
        self.bt_configure.setShortcut(_("Ctrl+,"))
        self.bt_help.setToolTip(_("Get some help"))
        self.bt_help.setText(_("Get Help"))
        self.bt_help.setShortcut(_("F1"))

from hackedit.presentation.widgets.recents import RecentFilesListWidget
from . import hackedit_rc
