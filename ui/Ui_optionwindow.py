# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'optionwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_optionWindow(object):
    def setupUi(self, optionWindow):
        optionWindow.setObjectName("optionWindow")
        optionWindow.resize(700, 340)
        optionWindow.setMinimumSize(QtCore.QSize(700, 340))
        optionWindow.setMaximumSize(QtCore.QSize(700, 340))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        optionWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/option_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        optionWindow.setWindowIcon(icon)
        optionWindow.setStyleSheet("QWidget {\n"
"    background-color: rgb(230,230,230);\n"
"}")
        self.gridLayout = QtWidgets.QGridLayout(optionWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ow_label_1 = QtWidgets.QLabel(optionWindow)
        self.ow_label_1.setMinimumSize(QtCore.QSize(0, 27))
        self.ow_label_1.setMaximumSize(QtCore.QSize(16777215, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.ow_label_1.setFont(font)
        self.ow_label_1.setObjectName("ow_label_1")
        self.horizontalLayout.addWidget(self.ow_label_1)
        self.ow_comboBox = QtWidgets.QComboBox(optionWindow)
        self.ow_comboBox.setMinimumSize(QtCore.QSize(100, 27))
        self.ow_comboBox.setMaximumSize(QtCore.QSize(100, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.ow_comboBox.setFont(font)
        self.ow_comboBox.setStyleSheet("QComboBox {\n"
"    border: 1px solid #acacac;\n"
"    border-radius: 1px;\n"
"    padding-left: 5px;\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, \n"
"                                stop: 0 #f0f0f0, stop: 1 #e5e5e5);\n"
"}\n"
"\n"
"QComboBox:disabled {\n"
"    background-color:  rgb(200,200,200);\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #7eb4ea;\n"
"    border-radius: 1px;\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, \n"
"                                stop: 0 #ecf4fc, stop: 1 #dcecfc);\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 27px;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::drop-down:hover {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 27px;\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(icons/down_arrow_icon.svg); \n"
"    width: 16px;\n"
"    height: 16px\n"
"}\n"
"\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px; \n"
"    left: 1px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    selection-background-color: rgb(200,200,200);\n"
"    selection-color: black;\n"
"    background: #f0f0f0;\n"
"    border: 0px solid #f0f0f0;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    margin: 5px 5px 5px 5px;\n"
"}")
        self.ow_comboBox.setObjectName("ow_comboBox")
        self.ow_comboBox.addItem("")
        self.ow_comboBox.addItem("")
        self.ow_comboBox.addItem("")
        self.ow_comboBox.addItem("")
        self.ow_comboBox.addItem("")
        self.horizontalLayout.addWidget(self.ow_comboBox)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.ow_infoButton_1 = QtWidgets.QToolButton(optionWindow)
        self.ow_infoButton_1.setMaximumSize(QtCore.QSize(27, 27))
        self.ow_infoButton_1.setStyleSheet("QToolButton {\n"
"    border: 1px solid transparent;\n"
"    background-color: transparent;\n"
"    width: 27px;\n"
"    height: 27px;\n"
"}\n"
"\n"
"QToolButton:flat {\n"
"    border: none;\n"
"}")
        self.ow_infoButton_1.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/info_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ow_infoButton_1.setIcon(icon1)
        self.ow_infoButton_1.setIconSize(QtCore.QSize(23, 23))
        self.ow_infoButton_1.setAutoRaise(False)
        self.ow_infoButton_1.setObjectName("ow_infoButton_1")
        self.horizontalLayout.addWidget(self.ow_infoButton_1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ow_label_2 = QtWidgets.QLabel(optionWindow)
        self.ow_label_2.setMinimumSize(QtCore.QSize(0, 27))
        self.ow_label_2.setMaximumSize(QtCore.QSize(16777215, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.ow_label_2.setFont(font)
        self.ow_label_2.setObjectName("ow_label_2")
        self.horizontalLayout_3.addWidget(self.ow_label_2)
        self.ow_lineEdit = QtWidgets.QLineEdit(optionWindow)
        self.ow_lineEdit.setMinimumSize(QtCore.QSize(400, 27))
        self.ow_lineEdit.setMaximumSize(QtCore.QSize(400, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(9)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.ow_lineEdit.setFont(font)
        self.ow_lineEdit.setStyleSheet("QLineEdit {\n"
"    border-radius: 3px;\n"
"    padding: 1px 4px 1px 4px;\n"
"    background-color:  rgb(240, 240, 240);\n"
"}")
        self.ow_lineEdit.setObjectName("ow_lineEdit")
        self.horizontalLayout_3.addWidget(self.ow_lineEdit)
        self.ow_openButton_1 = QtWidgets.QToolButton(optionWindow)
        self.ow_openButton_1.setMaximumSize(QtCore.QSize(27, 27))
        self.ow_openButton_1.setStyleSheet("QToolButton {\n"
"    border: 1px solid transparent;\n"
"    background-color: transparent;\n"
"    width: 27px;\n"
"    height: 27px;\n"
"}\n"
"\n"
"QToolButton:flat {\n"
"    border: none;\n"
"}")
        self.ow_openButton_1.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/open_popup_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ow_openButton_1.setIcon(icon2)
        self.ow_openButton_1.setIconSize(QtCore.QSize(23, 23))
        self.ow_openButton_1.setAutoRaise(False)
        self.ow_openButton_1.setObjectName("ow_openButton_1")
        self.horizontalLayout_3.addWidget(self.ow_openButton_1)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.ow_infoButton_2 = QtWidgets.QToolButton(optionWindow)
        self.ow_infoButton_2.setMaximumSize(QtCore.QSize(27, 27))
        self.ow_infoButton_2.setStyleSheet("QToolButton {\n"
"    border: 1px solid transparent;\n"
"    background-color: transparent;\n"
"    width: 27px;\n"
"    height: 27px;\n"
"}\n"
"\n"
"QToolButton:flat {\n"
"    border: none;\n"
"}")
        self.ow_infoButton_2.setText("")
        self.ow_infoButton_2.setIcon(icon1)
        self.ow_infoButton_2.setIconSize(QtCore.QSize(23, 23))
        self.ow_infoButton_2.setAutoRaise(False)
        self.ow_infoButton_2.setObjectName("ow_infoButton_2")
        self.horizontalLayout_3.addWidget(self.ow_infoButton_2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.line = QtWidgets.QFrame(optionWindow)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        spacerItem5 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.ow_checkBox_1 = QtWidgets.QCheckBox(optionWindow)
        self.ow_checkBox_1.setMinimumSize(QtCore.QSize(0, 27))
        self.ow_checkBox_1.setMaximumSize(QtCore.QSize(16777215, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.ow_checkBox_1.setFont(font)
        self.ow_checkBox_1.setObjectName("ow_checkBox_1")
        self.horizontalLayout_6.addWidget(self.ow_checkBox_1)
        spacerItem6 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.ow_infoButton_3 = QtWidgets.QToolButton(optionWindow)
        self.ow_infoButton_3.setMaximumSize(QtCore.QSize(27, 27))
        self.ow_infoButton_3.setStyleSheet("QToolButton {\n"
"    border: 1px solid transparent;\n"
"    background-color: transparent;\n"
"    width: 27px;\n"
"    height: 27px;\n"
"}\n"
"\n"
"QToolButton:flat {\n"
"    border: none;\n"
"}")
        self.ow_infoButton_3.setText("")
        self.ow_infoButton_3.setIcon(icon1)
        self.ow_infoButton_3.setIconSize(QtCore.QSize(23, 23))
        self.ow_infoButton_3.setAutoRaise(False)
        self.ow_infoButton_3.setObjectName("ow_infoButton_3")
        self.horizontalLayout_6.addWidget(self.ow_infoButton_3)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        spacerItem8 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem8)
        self.line_2 = QtWidgets.QFrame(optionWindow)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        spacerItem9 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem9)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.ow_checkBox_2 = QtWidgets.QCheckBox(optionWindow)
        self.ow_checkBox_2.setMinimumSize(QtCore.QSize(0, 27))
        self.ow_checkBox_2.setMaximumSize(QtCore.QSize(16777215, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.ow_checkBox_2.setFont(font)
        self.ow_checkBox_2.setObjectName("ow_checkBox_2")
        self.horizontalLayout_5.addWidget(self.ow_checkBox_2)
        spacerItem10 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem10)
        self.ow_infoButton_4 = QtWidgets.QToolButton(optionWindow)
        self.ow_infoButton_4.setMaximumSize(QtCore.QSize(27, 27))
        self.ow_infoButton_4.setStyleSheet("QToolButton {\n"
"    border: 1px solid transparent;\n"
"    background-color: transparent;\n"
"    width: 27px;\n"
"    height: 27px;\n"
"}\n"
"\n"
"QToolButton:flat {\n"
"    border: none;\n"
"}")
        self.ow_infoButton_4.setText("")
        self.ow_infoButton_4.setIcon(icon1)
        self.ow_infoButton_4.setIconSize(QtCore.QSize(23, 23))
        self.ow_infoButton_4.setAutoRaise(False)
        self.ow_infoButton_4.setObjectName("ow_infoButton_4")
        self.horizontalLayout_5.addWidget(self.ow_infoButton_4)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem11)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ow_checkBox_3 = QtWidgets.QCheckBox(optionWindow)
        self.ow_checkBox_3.setEnabled(False)
        self.ow_checkBox_3.setMinimumSize(QtCore.QSize(0, 27))
        self.ow_checkBox_3.setMaximumSize(QtCore.QSize(16777215, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.ow_checkBox_3.setFont(font)
        self.ow_checkBox_3.setObjectName("ow_checkBox_3")
        self.horizontalLayout_4.addWidget(self.ow_checkBox_3)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem12)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        spacerItem13 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem13)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem14 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem14)
        self.ow_okButton = QtWidgets.QToolButton(optionWindow)
        self.ow_okButton.setMinimumSize(QtCore.QSize(90, 27))
        self.ow_okButton.setMaximumSize(QtCore.QSize(90, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.ow_okButton.setFont(font)
        self.ow_okButton.setStyleSheet("QToolButton {\n"
"    border: 1px solid #acacac;\n"
"    border-radius: 1px;\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                    stop:0 #f0f0f0, stop:1 #e5e5e5);\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"    border: 1px solid #7eb4ea;\n"
"    border-radius: 1px;\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                    stop:0 #ecf4fc, stop:1 #dcecfc);\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    border: 1px solid #579de5;\n"
"    border-radius: 1px;\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                    stop:0 #daecfc, stop:1 #c4e0fc);\n"
"}")
        self.ow_okButton.setObjectName("ow_okButton")
        self.horizontalLayout_2.addWidget(self.ow_okButton)
        spacerItem15 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem15)
        self.ow_cancelButton = QtWidgets.QToolButton(optionWindow)
        self.ow_cancelButton.setMinimumSize(QtCore.QSize(90, 27))
        self.ow_cancelButton.setMaximumSize(QtCore.QSize(90, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.ow_cancelButton.setFont(font)
        self.ow_cancelButton.setStyleSheet("QToolButton {\n"
"    border: 1px solid #acacac;\n"
"    border-radius: 1px;\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                    stop:0 #f0f0f0, stop:1 #e5e5e5);\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"    border: 1px solid #7eb4ea;\n"
"    border-radius: 1px;\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                    stop:0 #ecf4fc, stop:1 #dcecfc);\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    border: 1px solid #579de5;\n"
"    border-radius: 1px;\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                    stop:0 #daecfc, stop:1 #c4e0fc);\n"
"}")
        self.ow_cancelButton.setObjectName("ow_cancelButton")
        self.horizontalLayout_2.addWidget(self.ow_cancelButton)
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem16)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(optionWindow)
        QtCore.QMetaObject.connectSlotsByName(optionWindow)

    def retranslateUi(self, optionWindow):
        _translate = QtCore.QCoreApplication.translate
        optionWindow.setWindowTitle(_translate("optionWindow", "Options"))
        self.ow_label_1.setText(_translate("optionWindow", "Logging level:"))
        self.ow_comboBox.setItemText(0, _translate("optionWindow", "DEBUG"))
        self.ow_comboBox.setItemText(1, _translate("optionWindow", "INFO"))
        self.ow_comboBox.setItemText(2, _translate("optionWindow", "WARNING"))
        self.ow_comboBox.setItemText(3, _translate("optionWindow", "CRITICAL"))
        self.ow_comboBox.setItemText(4, _translate("optionWindow", "ERROR"))
        self.ow_label_2.setText(_translate("optionWindow", "Path of the logging file:"))
        self.ow_checkBox_1.setText(_translate("optionWindow", "Check Prosim737 Updater updates on GitHub"))
        self.ow_checkBox_2.setText(_translate("optionWindow", "Terminate automatically Prosim737 processes to update Prosim737 modules"))
        self.ow_checkBox_3.setText(_translate("optionWindow", "Relaunch automatically Prosim737 processes after the update of Prosim737 modules"))
        self.ow_okButton.setText(_translate("optionWindow", "Ok"))
        self.ow_cancelButton.setText(_translate("optionWindow", "Cancel"))

