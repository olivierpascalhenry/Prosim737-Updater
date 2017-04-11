# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pathwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_pathWindow(object):
    def setupUi(self, pathWindow):
        pathWindow.setObjectName("pathWindow")
        pathWindow.resize(600, 180)
        pathWindow.setMinimumSize(QtCore.QSize(600, 180))
        pathWindow.setMaximumSize(QtCore.QSize(600, 16777215))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        pathWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/warning_popup_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        pathWindow.setWindowIcon(icon)
        pathWindow.setStyleSheet("QWidget {\n"
"    background-color: rgb(230,230,230);\n"
"}")
        self.gridLayout = QtWidgets.QGridLayout(pathWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.iw_label_2 = QtWidgets.QLabel(pathWindow)
        self.iw_label_2.setMinimumSize(QtCore.QSize(50, 50))
        self.iw_label_2.setMaximumSize(QtCore.QSize(50, 50))
        self.iw_label_2.setText("")
        self.iw_label_2.setPixmap(QtGui.QPixmap("icons/warning_popup_icon.svg"))
        self.iw_label_2.setScaledContents(True)
        self.iw_label_2.setObjectName("iw_label_2")
        self.verticalLayout.addWidget(self.iw_label_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.iw_label_1 = QtWidgets.QLabel(pathWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iw_label_1.sizePolicy().hasHeightForWidth())
        self.iw_label_1.setSizePolicy(sizePolicy)
        self.iw_label_1.setMinimumSize(QtCore.QSize(0, 27))
        self.iw_label_1.setMaximumSize(QtCore.QSize(16777215, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.iw_label_1.setFont(font)
        self.iw_label_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.iw_label_1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.iw_label_1.setLineWidth(0)
        self.iw_label_1.setMidLineWidth(0)
        self.iw_label_1.setTextFormat(QtCore.Qt.AutoText)
        self.iw_label_1.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.iw_label_1.setWordWrap(True)
        self.iw_label_1.setObjectName("iw_label_1")
        self.verticalLayout_3.addWidget(self.iw_label_1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem4)
        self.iw_label_3 = QtWidgets.QLabel(pathWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iw_label_3.sizePolicy().hasHeightForWidth())
        self.iw_label_3.setSizePolicy(sizePolicy)
        self.iw_label_3.setMinimumSize(QtCore.QSize(0, 27))
        self.iw_label_3.setMaximumSize(QtCore.QSize(16777215, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.iw_label_3.setFont(font)
        self.iw_label_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.iw_label_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.iw_label_3.setLineWidth(0)
        self.iw_label_3.setMidLineWidth(0)
        self.iw_label_3.setTextFormat(QtCore.Qt.AutoText)
        self.iw_label_3.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.iw_label_3.setWordWrap(True)
        self.iw_label_3.setObjectName("iw_label_3")
        self.verticalLayout_3.addWidget(self.iw_label_3)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        spacerItem5 = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.iw_okButton = QtWidgets.QToolButton(pathWindow)
        self.iw_okButton.setMinimumSize(QtCore.QSize(90, 27))
        self.iw_okButton.setMaximumSize(QtCore.QSize(90, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.iw_okButton.setFont(font)
        self.iw_okButton.setStyleSheet("QToolButton {\n"
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
        self.iw_okButton.setObjectName("iw_okButton")
        self.horizontalLayout_2.addWidget(self.iw_okButton)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.retranslateUi(pathWindow)
        QtCore.QMetaObject.connectSlotsByName(pathWindow)

    def retranslateUi(self, pathWindow):
        _translate = QtCore.QCoreApplication.translate
        pathWindow.setWindowTitle(_translate("pathWindow", "Warning"))
        self.iw_label_1.setText(_translate("pathWindow", "Prosim Updater can\'t find the following folders:"))
        self.iw_label_3.setText(_translate("pathWindow", "Please, make sure that they exist before installing Prosim737."))
        self.iw_okButton.setText(_translate("pathWindow", "Ok"))

