# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/colin/dev/hackedit/data/forms/settings_page_editor_colors.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(753, 580)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 741, 568))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.fontComboBox = QtWidgets.QFontComboBox(self.groupBox)
        self.fontComboBox.setFontFilters(QtWidgets.QFontComboBox.MonospacedFonts)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans Mono")
        self.fontComboBox.setCurrentFont(font)
        self.fontComboBox.setObjectName("fontComboBox")
        self.horizontalLayout_2.addWidget(self.fontComboBox)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.spinbox_font_size = QtWidgets.QSpinBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinbox_font_size.sizePolicy().hasHeightForWidth())
        self.spinbox_font_size.setSizePolicy(sizePolicy)
        self.spinbox_font_size.setMinimum(8)
        self.spinbox_font_size.setObjectName("spinbox_font_size")
        self.horizontalLayout_2.addWidget(self.spinbox_font_size)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.combo_color_schemes = QtWidgets.QComboBox(self.groupBox_2)
        self.combo_color_schemes.setObjectName("combo_color_schemes")
        self.horizontalLayout.addWidget(self.combo_color_schemes)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.edit_preview = CodeEdit(self.groupBox_3)
        self.edit_preview.setObjectName("edit_preview")
        self.gridLayout_2.addWidget(self.edit_preview, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        import gettext
        def _translate(_, string):
            return gettext.gettext(string)

        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Font"))
        self.label.setText(_translate("Form", "Family:"))
        self.fontComboBox.setToolTip(_translate("Form", "The editor font"))
        self.label_3.setText(_translate("Form", "Font size:"))
        self.spinbox_font_size.setToolTip(_translate("Form", "Default editor font size"))
        self.groupBox_2.setTitle(_translate("Form", "Colors"))
        self.label_4.setText(_translate("Form", "Color scheme:"))
        self.combo_color_schemes.setToolTip(_translate("Form", "Available editor color schemes"))
        self.groupBox_3.setTitle(_translate("Form", "Preview"))
        self.edit_preview.setToolTip(_translate("Form", "Color scheme/Font preview"))

from pyqode.core.api import CodeEdit
