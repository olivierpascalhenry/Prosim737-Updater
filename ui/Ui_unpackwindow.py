# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unpackwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_unpackWindow(object):
    def setupUi(self, unpackWindow):
        unpackWindow.setObjectName("unpackWindow")
        unpackWindow.resize(650, 290)
        unpackWindow.setMinimumSize(QtCore.QSize(650, 270))
        unpackWindow.setMaximumSize(QtCore.QSize(650, 16777215))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        unpackWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/info_popup_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        unpackWindow.setWindowIcon(icon)
        unpackWindow.setStyleSheet("QWidget {\n"
"    background-color: rgb(230,230,230);\n"
"}")
        self.gridLayout = QtWidgets.QGridLayout(unpackWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.uw_label_3 = QtWidgets.QLabel(unpackWindow)
        self.uw_label_3.setMinimumSize(QtCore.QSize(50, 50))
        self.uw_label_3.setMaximumSize(QtCore.QSize(50, 50))
        self.uw_label_3.setText("")
        self.uw_label_3.setPixmap(QtGui.QPixmap("icons/info_popup_icon.svg"))
        self.uw_label_3.setScaledContents(True)
        self.uw_label_3.setObjectName("uw_label_3")
        self.verticalLayout.addWidget(self.uw_label_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.uw_label_1 = QtWidgets.QLabel(unpackWindow)
        self.uw_label_1.setMinimumSize(QtCore.QSize(0, 120))
        self.uw_label_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.uw_label_1.setFont(font)
        self.uw_label_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.uw_label_1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.uw_label_1.setLineWidth(0)
        self.uw_label_1.setMidLineWidth(0)
        self.uw_label_1.setTextFormat(QtCore.Qt.AutoText)
        self.uw_label_1.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.uw_label_1.setWordWrap(True)
        self.uw_label_1.setObjectName("uw_label_1")
        self.verticalLayout_2.addWidget(self.uw_label_1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem2)
        self.uw_progressBar = QtWidgets.QProgressBar(unpackWindow)
        self.uw_progressBar.setMinimumSize(QtCore.QSize(0, 27))
        self.uw_progressBar.setMaximumSize(QtCore.QSize(16777215, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.uw_progressBar.setFont(font)
        self.uw_progressBar.setProperty("value", 0)
        self.uw_progressBar.setTextVisible(False)
        self.uw_progressBar.setObjectName("uw_progressBar")
        self.verticalLayout_2.addWidget(self.uw_progressBar)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.uw_label_2 = QtWidgets.QLabel(unpackWindow)
        self.uw_label_2.setMinimumSize(QtCore.QSize(0, 27))
        self.uw_label_2.setMaximumSize(QtCore.QSize(16777215, 27))
        font = QtGui.QFont()
        font.setItalic(True)
        self.uw_label_2.setFont(font)
        self.uw_label_2.setObjectName("uw_label_2")
        self.horizontalLayout_2.addWidget(self.uw_label_2)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        spacerItem5 = QtWidgets.QSpacerItem(28, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.uw_downloadButton = QtWidgets.QToolButton(unpackWindow)
        self.uw_downloadButton.setMinimumSize(QtCore.QSize(190, 27))
        self.uw_downloadButton.setMaximumSize(QtCore.QSize(230, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.uw_downloadButton.setFont(font)
        self.uw_downloadButton.setStyleSheet("QToolButton {\n"
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
        self.uw_downloadButton.setObjectName("uw_downloadButton")
        self.horizontalLayout.addWidget(self.uw_downloadButton)
        spacerItem7 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.uw_cancelButton = QtWidgets.QToolButton(unpackWindow)
        self.uw_cancelButton.setMinimumSize(QtCore.QSize(90, 27))
        self.uw_cancelButton.setMaximumSize(QtCore.QSize(110, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.uw_cancelButton.setFont(font)
        self.uw_cancelButton.setStyleSheet("QToolButton {\n"
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
        self.uw_cancelButton.setObjectName("uw_cancelButton")
        self.horizontalLayout.addWidget(self.uw_cancelButton)
        spacerItem8 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.uw_quitButton = QtWidgets.QToolButton(unpackWindow)
        self.uw_quitButton.setMinimumSize(QtCore.QSize(90, 27))
        self.uw_quitButton.setMaximumSize(QtCore.QSize(110, 27))
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.uw_quitButton.setFont(font)
        self.uw_quitButton.setStyleSheet("QToolButton {\n"
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
        self.uw_quitButton.setObjectName("uw_quitButton")
        self.horizontalLayout.addWidget(self.uw_quitButton)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem9)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.retranslateUi(unpackWindow)
        QtCore.QMetaObject.connectSlotsByName(unpackWindow)

    def retranslateUi(self, unpackWindow):
        _translate = QtCore.QCoreApplication.translate
        unpackWindow.setWindowTitle(_translate("unpackWindow", "Update Install"))
        self.uw_label_1.setText(_translate("unpackWindow", "<html><head/><body><p>Click on the <span style=\" font-weight:600; font-style:italic; color:#000000;\">Unpack and Install</span> button to start unpacking the package. Installation process will start automatically once the package is extracted.</p><p align=\"center\"><span style=\" font-style:italic; color:#c80000;\">Unpacking can be canceled, but once the installation is started, the process can\'t be stopped until installation is complete.</span></p></body></html>"))
        self.uw_label_2.setText(_translate("unpackWindow", "TEMP"))
        self.uw_downloadButton.setText(_translate("unpackWindow", "Unpack and Install"))
        self.uw_cancelButton.setText(_translate("unpackWindow", "Cancel"))
        self.uw_quitButton.setText(_translate("unpackWindow", "Quit"))

