import urllib.request
import tempfile
import zipfile
import os
import time
import psutil
import xml.dom.minidom
import subprocess
import logging
from shutil import copyfile, copy, rmtree
from ui.Ui_infowindow import Ui_infoWindow
from ui.Ui_downloadwindow import Ui_downloadWindow
from ui.Ui_unpackwindow import Ui_unpackWindow
from ui.Ui_storewindow import Ui_storeWindow
from ui.Ui_compresswindow import Ui_compressWindow
from ui.Ui_restorewindow import Ui_restoreWindow
from ui.Ui_pathwindow import Ui_pathWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5.Qt import QThread


def info_button(self):
    logging.debug('button_functions.py - info_button invoked')
    logging.debug('button_functions.py - info_button: ' + str(self.sender().objectName()))
    infoText = self.button_information[int(self.sender().objectName()[8:]) - 1]
    x = QtGui.QCursor.pos().x()
    y = QtGui.QCursor.pos().y()
    x = x - 175
    y = y + 50
    self.infoWindow = MyInfo(infoText)
    self.infoWindow.setMinimumSize(QtCore.QSize(450, self.infoWindow.sizeHint().height()))
    self.infoWindow.setMaximumSize(QtCore.QSize(450, self.infoWindow.sizeHint().height()))
    self.infoWindow.setGeometry(x, y, 450, self.infoWindow.sizeHint().height())
    self.infoWindow.exec_()


def add_path(self):
    logging.debug('button_functions.py - add_path invoked')
    logging.debug('button_functions.py - add_path: ' + str(self.sender().objectName()))
    index_object = self.sender().objectName().index('_bt_')
    category = self.sender().objectName()[:index_object]
    num = self.sender().objectName()[index_object+4:]
    path = self.get_directory()
    if path:
        line_object = self.findChildren(QLineEdit, category + '_ln_' + num)
        line_object[0].setText(str(path))
        self.set_modified()


def new_path(self, category=None, path=None):
    logging.debug('button_functions.py - new_path invoked')
    if not category:
        logging.debug('button_functions.py - new_path: ' + str(self.sender().objectName()))
        category = self.sender().objectName()[:-13]
    vl_object = getattr(self, category + '_vl')
    hl_object = getattr(self, category + '_hl_list')
    lb_object = getattr(self, category + '_lb_list')
    ln_object = getattr(self, category + '_ln_list')
    bt_object = getattr(self, category + '_bt_list')
    no_object = getattr(self, category + '_no_list')
    dl_object = getattr(self, category + '_dl_list')
    num_object = getattr(self, category + '_num')
    font1 = QtGui.QFont()
    font1.setFamily("fonts/SourceSansPro-Regular.ttf")
    font1.setPointSize(10)
    font1.setBold(False)
    font1.setWeight(50)
    font1.setKerning(True)
    font1.setStyleStrategy(QtGui.QFont.PreferAntialias)
    font2 = QtGui.QFont()
    font2.setFamily("fonts/SourceSansPro-Regular.ttf")
    font2.setPointSize(9)
    font2.setBold(False)
    font2.setWeight(50)
    font2.setKerning(True)
    font2.setStyleStrategy(QtGui.QFont.PreferAntialias)
    icon1 = QtGui.QIcon()
    icon1.addPixmap(QtGui.QPixmap("icons/open_popup_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    icon2 = QtGui.QIcon()
    icon2.addPixmap(QtGui.QPixmap("icons/del_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    icon3 = QtGui.QIcon()
    icon3.addPixmap(QtGui.QPixmap("icons/none_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    hl_object.append(QtWidgets.QHBoxLayout()) 
    hl_object[num_object].setObjectName(category + "_user_hl_" + str(num_object + 1))
    lb_object.append(QtWidgets.QLabel())
    lb_object[num_object].setMinimumSize(QtCore.QSize(0, 27))
    lb_object[num_object].setMaximumSize(QtCore.QSize(16777215, 27))
    lb_object[num_object].setFont(font1)
    lb_object[num_object].setText("Prosim737 " + self.category_name[category] + " location:")
    lb_object[num_object].setObjectName(category + "_user_lb_" + str(num_object + 1))
    hl_object[num_object].addWidget(lb_object[num_object])
    ln_object.append(QtWidgets.QLineEdit())
    ln_object[num_object].setMinimumSize(QtCore.QSize(600, 27))
    ln_object[num_object].setMaximumSize(QtCore.QSize(600, 27))
    ln_object[num_object].setFont(font2)
    ln_object[num_object].setStyleSheet("QLineEdit {\n"
        "    border-radius: 3px;\n"
        "   padding: 1px 4px 1px 4px;\n"
        "    background-color:  rgb(240, 240, 240);\n"
        "}")
    ln_object[num_object].setFrame(False)
    ln_object[num_object].setObjectName(category + "_user_ln_" + str(num_object + 1))
    hl_object[num_object].addWidget(ln_object[num_object])
    bt_object.append(QtWidgets.QToolButton())
    bt_object[num_object].setMaximumSize(QtCore.QSize(27, 27))
    bt_object[num_object].setStyleSheet("QToolButton {\n"
        "    border: 1px solid transparent;\n"
        "    background-color: transparent;\n"
        "    width: 27px;\n"
        "    height: 27px;\n"
        "}\n"
        "\n"
        "QToolButton:flat {\n"
        "    border: none;\n"
        "}")
    bt_object[num_object].setIcon(icon1)
    bt_object[num_object].setIconSize(QtCore.QSize(23, 23))
    bt_object[num_object].setAutoRaise(False)
    bt_object[num_object].setObjectName(category + "_user_bt_" + str(num_object + 1))
    hl_object[num_object].addWidget(bt_object[num_object])
    dl_object.append(QtWidgets.QToolButton())
    dl_object[num_object].setMaximumSize(QtCore.QSize(27, 27))
    dl_object[num_object].setStyleSheet("QToolButton {\n"
        "    border: 1px solid transparent;\n"
        "    background-color: transparent;\n"
        "    width: 27px;\n"
        "    height: 27px;\n"
        "}\n"
        "\n"
        "QToolButton:flat {\n"
        "    border: none;\n"
        "}")
    dl_object[num_object].setIcon(icon2)
    dl_object[num_object].setIconSize(QtCore.QSize(23, 23))
    dl_object[num_object].setAutoRaise(False)
    dl_object[num_object].setObjectName(category + "_user_delete_bt_" + str(num_object + 1))
    hl_object[num_object].addWidget(dl_object[num_object])
    no_object.append(QtWidgets.QToolButton())
    no_object[num_object].setMaximumSize(QtCore.QSize(27, 27))
    no_object[num_object].setStyleSheet("QToolButton {\n"
        "    border: 1px solid transparent;\n"
        "    background-color: transparent;\n"
        "    width: 27px;\n"
        "    height: 27px;\n"
        "}\n"
        "\n"
        "QToolButton:flat {\n"
        "    border: none;\n"
        "}")
    no_object[num_object].setIcon(icon3)
    no_object[num_object].setIconSize(QtCore.QSize(23, 23))
    no_object[num_object].setAutoRaise(False)
    no_object[num_object].setObjectName(category + "_none_bt_" + str(num_object + 1))
    hl_object[num_object].addWidget(no_object[num_object])
    hl_object[num_object].addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
    vl_object.addLayout(hl_object[num_object])
    bt_object[num_object].clicked.connect(lambda: self.tool_button_clicked())
    dl_object[num_object].clicked.connect(lambda: self.tool_button_clicked())
    ln_object[num_object].textChanged.connect(lambda: self.set_modified())
    if path:
        ln_object[num_object].setText(path)
    num_object += 1
    setattr(self, category + '_vl', vl_object)
    setattr(self, category + '_hl_list', hl_object)
    setattr(self, category + '_lb_list', lb_object)
    setattr(self, category + '_ln_list', ln_object)
    setattr(self, category + '_bt_list', bt_object)
    setattr(self, category + '_no_list', no_object)
    setattr(self, category + '_dl_list', dl_object)
    setattr(self, category + '_num', num_object)
    
    
def new_credentials(self, credentials=None):
    logging.debug('button_functions.py - new_credentials invoked')
    if credentials is None:
        logging.debug('button_functions.py - new_credentials: ' + str(self.sender().objectName()))
    font1 = QtGui.QFont()
    font1.setFamily("fonts/SourceSansPro-Regular.ttf")
    font1.setPointSize(10)
    font1.setBold(False)
    font1.setWeight(50)
    font1.setKerning(True)
    font1.setStyleStrategy(QtGui.QFont.PreferAntialias)
    font2 = QtGui.QFont()
    font2.setFamily("fonts/SourceSansPro-Regular.ttf")
    font2.setPointSize(9)
    font2.setBold(False)
    font2.setWeight(50)
    font2.setKerning(True)
    font2.setStyleStrategy(QtGui.QFont.PreferAntialias)
    icon1 = QtGui.QIcon()
    icon1.addPixmap(QtGui.QPixmap("icons/open_popup_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    icon2 = QtGui.QIcon()
    icon2.addPixmap(QtGui.QPixmap("icons/del_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.cred_hl_1_list.append(QtWidgets.QHBoxLayout()) 
    self.cred_hl_1_list[self.cred_num].setObjectName("cred_hl_1_list_" + str(self.cred_num))
    self.cred_hl_1_list[self.cred_num].addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum))
    self.cred_vl_1_list.append(QtWidgets.QVBoxLayout()) 
    self.cred_vl_1_list[self.cred_num].setObjectName("cred_vl_1_list_" + str(self.cred_num))
    self.cred_hl_1_list[self.cred_num].addLayout(self.cred_vl_1_list[self.cred_num])
    if self.cred_num > 0:
        self.cred_vl_1_list[self.cred_num].addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed))
    self.cred_hl_2_list.append(QtWidgets.QHBoxLayout()) 
    self.cred_hl_2_list[self.cred_num].setObjectName("cred_hl_2_list_" + str(self.cred_num))
    self.cred_vl_1_list[self.cred_num].addLayout(self.cred_hl_2_list[self.cred_num])
    self.cred_lb_1_list.append(QtWidgets.QLabel())
    self.cred_lb_1_list[self.cred_num].setMinimumSize(QtCore.QSize(0, 27))
    self.cred_lb_1_list[self.cred_num].setMaximumSize(QtCore.QSize(16777215, 27))
    self.cred_lb_1_list[self.cred_num].setFont(font1)
    self.cred_lb_1_list[self.cred_num].setText("Computer name / IP address:")
    self.cred_lb_1_list[self.cred_num].setObjectName("cred_lb_1_list_" + str(self.cred_num))
    self.cred_hl_2_list[self.cred_num].addWidget(self.cred_lb_1_list[self.cred_num])
    self.cred_ln_1_list.append(QtWidgets.QLineEdit())
    self.cred_ln_1_list[self.cred_num].setMinimumSize(QtCore.QSize(300, 27))
    self.cred_ln_1_list[self.cred_num].setMaximumSize(QtCore.QSize(16777215, 27))
    self.cred_ln_1_list[self.cred_num].setFont(font2)
    self.cred_ln_1_list[self.cred_num].setStyleSheet("QLineEdit {\n"
        "    border-radius: 3px;\n"
        "    padding: 1px 4px 1px 4px;\n"
        "    background-color:  rgb(240, 240, 240);\n"
        "}")
    self.cred_ln_1_list[self.cred_num].setFrame(False)
    self.cred_ln_1_list[self.cred_num].setObjectName("cred_ln_1_list_" + str(self.cred_num))
    self.cred_hl_2_list[self.cred_num].addWidget(self.cred_ln_1_list[self.cred_num])
    self.cred_hl_2_list[self.cred_num].addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
    self.cred_hl_3_list.append(QtWidgets.QHBoxLayout()) 
    self.cred_hl_3_list[self.cred_num].setObjectName("cred_hl_3_list_" + str(self.cred_num))
    self.cred_vl_1_list[self.cred_num].addLayout(self.cred_hl_3_list[self.cred_num])
    self.cred_lb_2_list.append(QtWidgets.QLabel())
    self.cred_lb_2_list[self.cred_num].setMinimumSize(QtCore.QSize(0, 27))
    self.cred_lb_2_list[self.cred_num].setMaximumSize(QtCore.QSize(16777215, 27))
    self.cred_lb_2_list[self.cred_num].setFont(font1)
    self.cred_lb_2_list[self.cred_num].setText("Username:")
    self.cred_lb_2_list[self.cred_num].setObjectName("cred_lb_2_list_" + str(self.cred_num))
    self.cred_hl_3_list[self.cred_num].addWidget(self.cred_lb_2_list[self.cred_num])
    self.cred_ln_2_list.append(QtWidgets.QLineEdit())
    self.cred_ln_2_list[self.cred_num].setMinimumSize(QtCore.QSize(300, 27))
    self.cred_ln_2_list[self.cred_num].setMaximumSize(QtCore.QSize(16777215, 27))
    self.cred_ln_2_list[self.cred_num].setFont(font2)
    self.cred_ln_2_list[self.cred_num].setStyleSheet("QLineEdit {\n"
        "    border-radius: 3px;\n"
        "    padding: 1px 4px 1px 4px;\n"
        "    background-color:  rgb(240, 240, 240);\n"
        "}")
    self.cred_ln_2_list[self.cred_num].setFrame(False)
    self.cred_ln_2_list[self.cred_num].setObjectName("cred_ln_2_list_" + str(self.cred_num))
    self.cred_hl_3_list[self.cred_num].addWidget(self.cred_ln_2_list[self.cred_num])
    self.cred_hl_3_list[self.cred_num].addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum))
    self.cred_lb_3_list.append(QtWidgets.QLabel())
    self.cred_lb_3_list[self.cred_num].setMinimumSize(QtCore.QSize(0, 27))
    self.cred_lb_3_list[self.cred_num].setMaximumSize(QtCore.QSize(16777215, 27))
    self.cred_lb_3_list[self.cred_num].setFont(font1)
    self.cred_lb_3_list[self.cred_num].setText("Password:")
    self.cred_lb_3_list[self.cred_num].setObjectName("cred_lb_3_list_" + str(self.cred_num))
    self.cred_hl_3_list[self.cred_num].addWidget(self.cred_lb_3_list[self.cred_num])
    self.cred_ln_3_list.append(QtWidgets.QLineEdit())
    self.cred_ln_3_list[self.cred_num].setMinimumSize(QtCore.QSize(300, 27))
    self.cred_ln_3_list[self.cred_num].setMaximumSize(QtCore.QSize(16777215, 27))
    self.cred_ln_3_list[self.cred_num].setFont(font2)
    self.cred_ln_3_list[self.cred_num].setStyleSheet("QLineEdit {\n"
        "    border-radius: 3px;\n"
        "    padding: 1px 4px 1px 4px;\n"
        "    background-color:  rgb(240, 240, 240);\n"
        "}")
    self.cred_ln_3_list[self.cred_num].setFrame(False)
    self.cred_ln_3_list[self.cred_num].setObjectName("cred_ln_3_list_" + str(self.cred_num))
    self.cred_hl_3_list[self.cred_num].addWidget(self.cred_ln_3_list[self.cred_num])
    self.cred_hl_3_list[self.cred_num].addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum))
    self.cred_dl_list.append(QtWidgets.QToolButton())
    self.cred_dl_list[self.cred_num].setMaximumSize(QtCore.QSize(27, 27))
    self.cred_dl_list[self.cred_num].setStyleSheet("QToolButton {\n"
        "    border: 1px solid transparent;\n"
        "    background-color: transparent;\n"
        "    width: 27px;\n"
        "    height: 27px;\n"
        "}\n"
        "\n"
        "QToolButton:flat {\n"
        "    border: none;\n"
        "}")
    self.cred_dl_list[self.cred_num].setIcon(icon2)
    self.cred_dl_list[self.cred_num].setIconSize(QtCore.QSize(23, 23))
    self.cred_dl_list[self.cred_num].setAutoRaise(False)
    self.cred_dl_list[self.cred_num].setObjectName("cred_delete_list_" + str(self.cred_num))
    self.cred_hl_1_list[self.cred_num].addWidget(self.cred_dl_list[self.cred_num])
    self.cred_hl_1_list[self.cred_num].addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
    self.credentials_vl.addLayout(self.cred_hl_1_list[self.cred_num])
    self.cred_dl_list[self.cred_num].clicked.connect(lambda: self.tool_button_clicked())
    if credentials:
        self.cred_ln_1_list[self.cred_num].setText(credentials[0])
        self.cred_ln_2_list[self.cred_num].setText(credentials[1])
        self.cred_ln_3_list[self.cred_num].setText(credentials[2])
    self.cred_ln_1_list[self.cred_num].textChanged.connect(lambda: self.set_modified())
    self.cred_ln_2_list[self.cred_num].textChanged.connect(lambda: self.set_modified())
    self.cred_ln_3_list[self.cred_num].textChanged.connect(lambda: self.set_modified())
    self.cred_num += 1


def del_credentials(self, index=None):
    logging.debug('button_functions.py - del_credentials invoked')
    if index == None:
        logging.debug('button_functions.py - del_credentials: ' + str(self.sender().objectName()))
        index = int(self.sender().objectName()[-1:])
    string1 = self.cred_ln_1_list[index].text()
    string2 = self.cred_ln_2_list[index].text()
    string3 = self.cred_ln_3_list[index].text()
    self.cred_hl_1_list[index].deleteLater()
    self.cred_hl_1_list.pop(index)
    self.cred_vl_1_list[index].deleteLater()
    self.cred_vl_1_list.pop(index)
    self.cred_hl_2_list[index].deleteLater()
    self.cred_hl_2_list.pop(index)
    self.cred_hl_3_list[index].deleteLater()
    self.cred_hl_3_list.pop(index)
    self.cred_lb_1_list[index].deleteLater()
    self.cred_lb_1_list.pop(index)
    self.cred_ln_1_list[index].deleteLater()
    self.cred_ln_1_list.pop(index)
    self.cred_lb_2_list[index].deleteLater()
    self.cred_lb_2_list.pop(index)
    self.cred_ln_2_list[index].deleteLater()
    self.cred_ln_2_list.pop(index)
    self.cred_lb_3_list[index].deleteLater()
    self.cred_lb_3_list.pop(index)
    self.cred_ln_3_list[index].deleteLater()
    self.cred_ln_3_list.pop(index)
    self.cred_dl_list[index].deleteLater()
    self.cred_dl_list.pop(index)
    self.cred_num -= 1
    if string1 and string2 and string3:
        self.set_modified()
    if len(self.cred_hl_1_list) > 0:
        for i in range(0, len(self.cred_hl_1_list)):
            self.cred_hl_1_list[i].setObjectName("cred_hl_1_list_" + str(i))
            self.cred_vl_1_list[i].setObjectName("cred_vl_1_list_" + str(i))
            self.cred_hl_2_list[i].setObjectName("cred_hl_2_list_" + str(i))
            self.cred_hl_3_list[i].setObjectName("cred_hl_3_list_" + str(i))
            self.cred_lb_1_list[i].setObjectName("cred_lb_1_list_" + str(i))
            self.cred_ln_1_list[i].setObjectName("cred_ln_1_list_" + str(i))
            self.cred_lb_2_list[i].setObjectName("cred_lb_2_list_" + str(i))
            self.cred_ln_2_list[i].setObjectName("cred_ln_2_list_" + str(i))
            self.cred_lb_3_list[i].setObjectName("cred_lb_3_list_" + str(i))
            self.cred_ln_3_list[i].setObjectName("cred_ln_3_list_" + str(i))
            self.cred_dl_list[i].setObjectName("cred_delete_list_" + str(i))
   
      
def del_path(self, index=None, category=None):
    logging.debug('button_functions.py - del_path invoked')
    if index == None:
        logging.debug('button_functions.py - del_path: ' + str(self.sender().objectName()))
        index = int(self.sender().objectName()[-1:])
    if category == None:
        logging.debug('button_functions.py - del_path: ' + str(self.sender().objectName()))
        category = self.sender().objectName()[:-17]
    hl_object = getattr(self, category + '_hl_list')
    lb_object = getattr(self, category + '_lb_list')
    ln_object = getattr(self, category + '_ln_list')
    bt_object = getattr(self, category + '_bt_list')
    no_object = getattr(self, category + '_no_list')
    dl_object = getattr(self, category + '_dl_list')
    num_object = getattr(self, category + '_num')
    string = ln_object[index - 1].text()
    hl_object[index - 1].deleteLater()
    hl_object.pop(index - 1)
    lb_object[index - 1].deleteLater()
    lb_object.pop(index - 1)
    ln_object[index - 1].deleteLater()
    ln_object.pop(index - 1)
    bt_object[index - 1].deleteLater()
    bt_object.pop(index - 1)
    no_object[index - 1].deleteLater()
    no_object.pop(index - 1)
    dl_object[index - 1].deleteLater()
    dl_object.pop(index - 1)
    num_object -= 1
    if len(hl_object) > 0:
        for i in range(0, len(hl_object)):
            hl_object[i].setObjectName(category + "_user_hl_" + str(i+1))
            lb_object[i].setObjectName(category + "_user_lb_" + str(i+1))
            ln_object[i].setObjectName(category + "_user_ln_" + str(i+1))
            bt_object[i].setObjectName(category + "_user_bt_" + str(i+1))
            no_object[i].setObjectName(category + "_none_bt_" + str(i+1))
            dl_object[i].setObjectName(category + "_user_delete_bt_" + str(i+1))
    setattr(self, category + '_hl_list', hl_object)
    setattr(self, category + '_lb_list', lb_object)
    setattr(self, category + '_ln_list', ln_object)
    setattr(self, category + '_bt_list', bt_object)
    setattr(self, category + '_no_list', no_object)
    setattr(self, category + '_dl_list', dl_object)
    setattr(self, category + '_num', num_object)
    if string:
        self.set_modified()


def create_backup(self):
    logging.debug('button_functions.py - create_backup invoked')
    prosim_server = load_prosim_path(self, self.tabWidgetPage2.findChildren(QLineEdit))
    prosim_mcp = load_prosim_path(self, self.tabWidgetPage3.findChildren(QLineEdit))
    prosim_cdu = load_prosim_path(self, self.tabWidgetPage4.findChildren(QLineEdit))
    prosim_display = load_prosim_path(self, self.tabWidgetPage5.findChildren(QLineEdit))
    prosim_panel = load_prosim_path(self, self.tabWidgetPage6.findChildren(QLineEdit))
    prosim_audio = load_prosim_path(self, self.tabWidgetPage7.findChildren(QLineEdit))
    prosim_path = prosim_server + prosim_mcp + prosim_cdu + prosim_display + prosim_panel + prosim_audio
    self.compressWindow = MyCompress(self.home_ln_2.text(), prosim_path)
    x1, y1, w1, h1 = self.geometry().getRect()
    _, _, w2, h2 = self.compressWindow.geometry().getRect()
    x2 = x1 + w1/2 - w2/2
    y2 = y1 + h1/2 - h2/2
    self.compressWindow.setGeometry(x2, y2, w2, h2)
    self.compressWindow.setMinimumSize(QtCore.QSize(500, self.compressWindow.sizeHint().height()))
    self.compressWindow.setMaximumSize(QtCore.QSize(500, self.compressWindow.sizeHint().height()))
    self.compressWindow.exec_()


def restore_backup(self):
    logging.debug('button_functions.py - restore_backup invoked')
    remove_tmp_package(self)
    prosim_credentials = load_prosim_credentials(self)
    self.restoreWindow = MyRestore(self.home_ln_2.text(), prosim_credentials)
    x1, y1, w1, h1 = self.geometry().getRect()
    _, _, w2, h2 = self.restoreWindow.geometry().getRect()
    x2 = x1 + w1/2 - w2/2
    y2 = y1 + h1/2 - h2/2
    self.restoreWindow.setGeometry(x2, y2, w2, h2)
    self.restoreWindow.setMinimumSize(QtCore.QSize(600, self.restoreWindow.sizeHint().height()))
    self.restoreWindow.setMaximumSize(QtCore.QSize(600, self.restoreWindow.sizeHint().height()))
    self.restoreWindow.exec_()


def update_prosim(self):
    logging.debug('button_functions.py - update_prosim invoked')
    logging.debug('button_functions.py - update_prosim: ' + self.selected_list_widget)
    prosim_server = load_prosim_path(self, self.tabWidgetPage2.findChildren(QLineEdit))
    prosim_mcp = load_prosim_path(self, self.tabWidgetPage3.findChildren(QLineEdit))
    prosim_cdu = load_prosim_path(self, self.tabWidgetPage4.findChildren(QLineEdit))
    prosim_display = load_prosim_path(self, self.tabWidgetPage5.findChildren(QLineEdit))
    prosim_panel = load_prosim_path(self, self.tabWidgetPage6.findChildren(QLineEdit))
    prosim_audio = load_prosim_path(self, self.tabWidgetPage7.findChildren(QLineEdit))
    prosim_path = [prosim_server, prosim_mcp, prosim_cdu, prosim_display, prosim_panel, prosim_audio]
    logging.debug('button_functions.py - update, prosim_path ' + str(prosim_path))
    prosim_credentials = load_prosim_credentials(self)
    remove_tmp_package(self)
    if self.selected_list_widget == 'online':
        url_name = self.update_package_path + self.update_package_name
        self.downloadWindow = MyDownload(url_name, prosim_path, prosim_credentials)
        x1, y1, w1, h1 = self.geometry().getRect()
        _, _, w2, h2 = self.downloadWindow.geometry().getRect()
        x2 = x1 + w1/2 - w2/2
        y2 = y1 + h1/2 - h2/2
        self.downloadWindow.setGeometry(x2, y2, w2, h2)
        self.downloadWindow.setMinimumSize(QtCore.QSize(650, self.downloadWindow.sizeHint().height()))
        self.downloadWindow.setMaximumSize(QtCore.QSize(650, self.downloadWindow.sizeHint().height()))
        self.downloadWindow.exec_()
    elif self.selected_list_widget == 'local':
        temp_path = tempfile.gettempdir()
        copyfile(self.update_package_path + self.update_package_name, temp_path + '\prosim_update_package.zip')
        self.unpackWindow = MyUnpack(prosim_path, prosim_credentials)
        x1, y1, w1, h1 = self.geometry().getRect()
        _, _, w2, h2 = self.unpackWindow.geometry().getRect()
        x2 = x1 + w1/2 - w2/2
        y2 = y1 + h1/2 - h2/2
        self.unpackWindow.setGeometry(x2, y2, w2, h2)
        self.unpackWindow.setMinimumSize(QtCore.QSize(650, self.unpackWindow.sizeHint().height()))
        self.unpackWindow.setMaximumSize(QtCore.QSize(650, self.unpackWindow.sizeHint().height()))
        self.unpackWindow.exec_()


def store_update(self):
    logging.debug('button_functions.py - store_update invoked')
    logging.debug('button_functions.py - store_update: ' + self.selected_list_widget)
    if self.selected_list_widget == 'online':
        url_name = self.update_package_path + self.update_package_name
        update_file = self.home_ln_1.text() + '/' + self.update_package_name
        self.storeWindow = MyStore(url_name, update_file)
        x1, y1, w1, h1 = self.geometry().getRect()
        _, _, w2, h2 = self.storeWindow.geometry().getRect()
        x2 = x1 + w1/2 - w2/2
        y2 = y1 + h1/2 - h2/2
        self.storeWindow.setGeometry(x2, y2, w2, h2)
        self.storeWindow.setMinimumSize(QtCore.QSize(500, self.storeWindow.sizeHint().height()))
        self.storeWindow.setMaximumSize(QtCore.QSize(500, self.storeWindow.sizeHint().height()))
        self.storeWindow.exec_()
        self.update_local_list()


def load_prosim_path(self, line_list):
    logging.debug('button_functions.py - load_prosim_path invoked')
    path_list = []
    for line in line_list:
        if line.text():
            path_list.append(line.text())
    return path_list


def load_prosim_credentials(self):
    logging.debug('button_functions.py - load_prosim_credentials invoked')
    credential_list = {}
    for i in range(0, len(self.cred_ln_1_list)):
        if self.cred_ln_1_list[i].text() and self.cred_ln_2_list[i].text():
            credential_list[self.cred_ln_1_list[i].text()] = {'username' : self.cred_ln_2_list[i].text(),
                                                              'password' : self.cred_ln_3_list[i].text()}
    return credential_list

def remove_tmp_package(self):
    logging.debug('button_functions.py - remove_tmp_package invoked')
    zip_name = tempfile.gettempdir() + '\prosim_update_package.zip'
    folder_name = tempfile.gettempdir() + '\prosim_update_package'
    if os.path.exists(zip_name):
        os.remove(zip_name)
        logging.debug('button_functions.py - remove_tmp_package: ' + zip_name + ' removed')
    if os.path.exists(folder_name):
        rmtree(folder_name)
        logging.debug('button_functions.py - remove_tmp_package: ' + folder_name + ' removed')
        

class MyInfo(QtWidgets.QDialog, Ui_infoWindow):
    def __init__(self, infoText):
        QWidget.__init__(self)
        logging.debug('button_functions.py - MyInfo invoked')
        self.setupUi(self)
        self.iw_label_1.setText(infoText)
        self.iw_okButton.clicked.connect(self.closeWindow)
        
    def closeWindow(self):
        self.close()
        
        
class MyDownload(QtWidgets.QDialog, Ui_downloadWindow):
    def __init__(self, url_name, prosim_path, prosim_credentials):
        QWidget.__init__(self)
        logging.debug('button_functions.py - MyDownload invoked')
        self.setupUi(self)
        self.label.setText('')
        self.url_name = url_name
        self.prosim_path = prosim_path
        self.prosim_credentials = prosim_credentials
        self.dw_cancelButton.clicked.connect(self.closeWindow)
        self.dw_downloadButton.clicked.connect(self.download_update)
        
    def download_update(self):
        logging.debug('button_functions.py - MyDownload: download update')
        success = self.check_prosim_processes()
        if success is False:
            return
        success = self.check_prosim_paths()
        if success is False:
            return
        self.dw_cancelButton.setEnabled(False)
        self.dw_downloadButton.setEnabled(False)
        self.label.setText('Downloading update...')
        self.thread = DownloadFile(self.url_name)
        self.thread.download_update.connect(self.update_progress_bar)
        self.thread.download_done.connect(self.unzip_update)
        self.thread.start()
    
    def update_progress_bar(self, val):
        self.progressBar.setValue(val)
    
    def unzip_update(self):
        logging.debug('button_functions.py - MyDownload: unzip update')
        self.label.setText('Unpacking update...')
        self.thread.download_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        self.update_progress_bar(0)
        zip_name = tempfile.gettempdir() + '\prosim_update_package.zip'
        unpack_folder = tempfile.gettempdir() + '\prosim_update_package'
        self.thread = UnpackFile(zip_name, unpack_folder)
        self.thread.unpack_update.connect(self.update_progress_bar)
        self.thread.unpack_done.connect(self.install_update)
        self.thread.start()
    
    def install_update(self):
        logging.debug('button_functions.py - MyDownload: install update')
        self.thread.unpack_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        self.update_progress_bar(0)
        self.label.setText('Installing update...')
        unpack_folder = tempfile.gettempdir() + '\prosim_update_package\\'
        self.thread = InstallFile(unpack_folder, self.prosim_path)
        self.thread.install_update.connect(self.update_progress_bar)
        self.thread.install_done.connect(self.end_process)
        self.thread.start()

    def end_process(self):
        logging.debug('button_functions.py - MyDownload: end process')
        self.thread.install_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        self.update_progress_bar(100)
        self.dw_cancelButton.setEnabled(True)
        self.dw_downloadButton.setEnabled(True)
        self.label.setText('Job finished !')
    
    def closeWindow(self):
        try:
            self.thread.terminated = True
            self.thread.exit()
        except AttributeError:
            pass
        self.close()
        
    def check_prosim_paths(self):
        logging.debug('button_functions.py - MyDownload: check_prosim_paths invoked')
        wrong_path = []
        success = True
        for all_path in self.prosim_path:
            for path in all_path:
                if not os.path.isdir(path):
                    wrong_path.append(path)  
        if wrong_path:
            self.pathWindow = MyPath(wrong_path)
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.pathWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
            self.pathWindow.exec_()
            success = False
        logging.debug('button_functions.py - MyDownload: success ' + str(success))
        return success
        
    def check_prosim_processes(self):
        logging.debug('button_functions.py - MyDownload: check_prosim_processes invoked')
        success = True
        prosim_processes = ['Prosim737.exe', 'ProsimAudio.exe', 'ProsimCDU.exe',
                            'ProsimMCP.exe', 'ProsimPanel.exe', 'ProsimDisplay.exe']
        running_processes = []
        computer_list = []
        for all_folders in self.prosim_path:
            for folder in all_folders:
                if folder[:2] == '//':
                    index = folder[2:].find('/')
                    computer_list.append(folder[2:index+2])
                elif ':/' in folder[:3]:
                    drive, _ = os.path.splitdrive(folder)
                    computer_list.append(drive[1:])
        computer_list = list(set(computer_list))
        logging.debug('button_functions.py - MyDownload: check_prosim_processes, computer_list ' + str(computer_list))
        for computer in computer_list:
            if computer == ':':
                for pid in psutil.pids():
                    try:
                        if psutil.Process(pid).name() in prosim_processes:
                            running_processes.append('Local - ' + psutil.Process(pid).name())
                    except psutil.NoSuchProcess:
                        pass
            else:
                if self.prosim_credentials:
                    try:
                        username = self.prosim_credentials[computer]['username']
                        password = self.prosim_credentials[computer]['password']
                        if password:
                            command = 'tasklist.exe /s ' + computer + ' /u ' + username + ' /p ' + password
                        else:
                            command = 'tasklist.exe /s ' + computer + ' /u ' + username
                        remote_list = [line.split() for line in subprocess.check_output(command).splitlines()]
                        for process in remote_list[2:]:
                            try:
                                if process[0].decode('ascii') in prosim_processes:
                                    running_processes.append(computer + ' - ' + process[0].decode('ascii'))
                            except IndexError:
                                pass
                    except KeyError:
                        logging.exception('button_functions.py - MyUnpack: check_prosim_processes')
                else:
                    logging.debug('button_functions.py - MyDonwload: check_prosim_processes, no credentials')
        if running_processes:
            text = ['The following processes are still running:',
                    'Please, make sure to stop them before installing Prosim737.']
            self.pathWindow = MyPath(running_processes, text)
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.pathWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
            self.pathWindow.exec_()
            success = False
        logging.debug('button_functions.py - MyDownload: success ' + str(success))
        return success


class MyUnpack(QtWidgets.QDialog, Ui_unpackWindow):
    def __init__(self, prosim_path, prosim_credentials):
        QWidget.__init__(self)
        logging.debug('button_functions.py - MyUnpack invoked')
        self.setupUi(self)
        self.label.setText('')
        self.prosim_path = prosim_path
        self.prosim_credentials = prosim_credentials
        self.dw_cancelButton.clicked.connect(self.closeWindow)
        self.dw_downloadButton.clicked.connect(self.unzip_update)
    
    def update_progress_bar(self, val):
        self.progressBar.setValue(val)
    
    def unzip_update(self):
        logging.debug('button_functions.py - MyUnpack: unzip update')
        success = self.check_prosim_processes()
        if success is False:
            return
        success = self.check_prosim_paths()
        if success is False:
            return
        self.dw_downloadButton.setEnabled(False)
        self.dw_cancelButton.setEnabled(False)
        self.label.setText('Unpacking update...')
        self.update_progress_bar(0)
        zip_name = tempfile.gettempdir() + '\prosim_update_package.zip'
        unpack_folder = tempfile.gettempdir() + '\prosim_update_package'
        self.thread = UnpackFile(zip_name, unpack_folder)
        self.thread.unpack_update.connect(self.update_progress_bar)
        self.thread.unpack_done.connect(self.install_update)
        self.thread.start()
    
    def install_update(self):
        logging.debug('button_functions.py - MyUnpack: install update')
        self.thread.unpack_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        self.update_progress_bar(0)
        self.label.setText('Installing update...')
        unpack_folder = tempfile.gettempdir() + '\prosim_update_package\\'
        self.thread = InstallFile(unpack_folder, self.prosim_path)
        self.thread.install_update.connect(self.update_progress_bar)
        self.thread.install_done.connect(self.end_process)
        self.thread.start()
    
    def end_process(self):
        logging.debug('button_functions.py - MyUnpack: end process')
        self.thread.install_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        self.update_progress_bar(100)
        self.dw_cancelButton.setEnabled(True)
        self.dw_downloadButton.setEnabled(True)
        self.label.setText('Job finished !')
    
    def closeWindow(self):
        try:
            self.thread.terminated = True
            self.thread.exit()
        except AttributeError:
            pass
        self.close()
        
    def check_prosim_paths(self):
        logging.debug('button_functions.py - MyUnpack: check_prosim_paths')
        wrong_path = []
        success = True
        for all_folders in self.prosim_path:
            for path in all_folders:
                if not os.path.isdir(path):
                    wrong_path.append(path)
        if wrong_path:
            self.pathWindow = MyPath(wrong_path)
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.pathWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
            self.pathWindow.exec_()
            success = False
        logging.debug('button_functions.py - MyUnpack: success ' + str(success))
        return success
    
    def check_prosim_processes(self):
        logging.debug('button_functions.py - MyUnpack: check_prosim_processes')
        success = True
        prosim_processes = ['Prosim737.exe', 'ProsimAudio.exe', 'ProsimCDU.exe',
                            'ProsimMCP.exe', 'ProsimPanel.exe', 'ProsimDisplay.exe']
        running_processes = []
        computer_list = []
        for all_folders in self.prosim_path:
            for folder in all_folders:
                if folder[:2] == '//':
                    index = folder[2:].find('/')
                    computer_list.append(folder[2:index+2])
                elif ':/' in folder[:3]:
                    drive, _ = os.path.splitdrive(folder)
                    computer_list.append(drive[1:])
        computer_list = list(set(computer_list))
        logging.debug('button_functions.py - MyUnpack: check_prosim_processes, computer_list ' + str(computer_list))
        for computer in computer_list:
            if computer == ':':
                for pid in psutil.pids():
                    try:
                        if psutil.Process(pid).name() in prosim_processes:
                            running_processes.append('Local - ' + psutil.Process(pid).name())
                    except psutil.NoSuchProcess:
                        pass
            else:
                if self.prosim_credentials:
                    try:
                        username = self.prosim_credentials[computer]['username']
                        password = self.prosim_credentials[computer]['password']
                        if password:
                            command = 'tasklist.exe /s ' + computer + ' /u ' + username + ' /p ' + password
                        else:
                            command = 'tasklist.exe /s ' + computer + ' /u ' + username
                        remote_list = [line.split() for line in subprocess.check_output(command).splitlines()]
                        for process in remote_list[2:]:
                            try:
                                if process[0].decode('ascii') in prosim_processes:
                                    running_processes.append(computer + ' - ' + process[0].decode('ascii'))
                            except IndexError:
                                pass
                    except KeyError:
                        logging.exception('button_functions.py - MyUnpack: check_prosim_processes')
                else:
                    logging.debug('button_functions.py - MyUnpack: check_prosim_processes, no credentials')
        if running_processes:
            text = ['The following processes are still running:',
                    'Please, make sure to stop them before installing Prosim737.']
            self.pathWindow = MyPath(running_processes, text)
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.pathWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
            self.pathWindow.exec_()
            success = False
        logging.debug('button_functions.py - MyUnpack: success ' + str(success))
        return success


class MyStore(QtWidgets.QDialog, Ui_storeWindow):
    def __init__(self, url_name, update_file):
        QWidget.__init__(self)
        logging.debug('button_functions.py - MyStore invoked')
        self.setupUi(self)
        self.update_file = update_file
        self.url_name = url_name
        self.download_update()
    
    def update_progress_bar(self, val):
        self.progressBar.setValue(val)
    
    def download_update(self):
        logging.debug('button_functions.py - MyStore: download_update')
        self.thread = DownloadFile(self.url_name, self.update_file)
        self.thread.download_update.connect(self.update_progress_bar)
        self.thread.download_done.connect(self.closeWindow)
        self.thread.start()
    
    def closeWindow(self):
        self.thread.download_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        self.close()
        
        
class MyCompress(QtWidgets.QDialog, Ui_compressWindow):
    def __init__(self, backup_directory, prosim_path):
        QWidget.__init__(self)
        logging.debug('button_functions.py - MyCompress invoked')
        self.setupUi(self)
        self.backup_directory = backup_directory
        self.prosim_path = prosim_path
        success = self.check_prosim_paths()
        if success is False:
            self.closeWindow()
        else:
            self.compress_directories()
    
    def update_progress_bar(self, val):
        self.progressBar.setValue(val)
    
    def compress_directories(self):
        logging.debug('button_functions.py - MyCompress: compress directories')
        self.thread = ZipProsim(self.backup_directory, self.prosim_path)
        self.thread.zip_update.connect(self.update_progress_bar)
        self.thread.zip_done.connect(self.closeWindow)
        self.thread.start()
        
    def check_prosim_paths(self):
        logging.debug('button_functions.py - MyCompress: check_prosim_paths')
        wrong_path = []
        success = True
        for path in self.prosim_path:
            if not os.path.isdir(path):
                wrong_path.append(path)
        if wrong_path:
            self.pathWindow = MyPath(wrong_path)
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.pathWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
            self.pathWindow.exec_()
            success = False
        logging.debug('button_functions.py - MyCompress: success ' + str(success))
        return success
    
    def closeWindow(self):
        self.thread.zip_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        self.close()


class MyRestore(QtWidgets.QDialog, Ui_restoreWindow):
    def __init__(self, backup_folder, prosim_credentials):
        QWidget.__init__(self)
        logging.debug('button_functions.py - MyRestore invoked')
        self.setupUi(self)
        self.label.setText('')
        self.backup_folder = backup_folder
        self.prosim_credentials = prosim_credentials
        self.rw_cancelButton.clicked.connect(self.closeWindow)
        self.rw_restoreButton.clicked.connect(self.restore_backup)
        self.rw_deleteButton.clicked.connect(self.delete_backup)
        self.rw_restoreButton.setEnabled(False)
        self.rw_deleteButton.setEnabled(False)
        self.progressBar.setEnabled(False)
        self.progressBar.setVisible(False)
        self.listWidget.itemClicked.connect(self.select_list_item)
        self.list_backups()
        
    def update_progress_bar(self, val):
        self.progressBar.setValue(val)
    
    def list_backups(self):
        logging.debug('button_functions.py - MyRestore: list backups')
        file_list = []
        try:
            for name in os.listdir(self.backup_folder):
                if os.path.isfile(os.path.join(self.backup_folder, name)):
                    file_list.append(name)
        except Exception:
            logging.warning('button_functions.py - MyRestore: ' + str(Exception))
        if file_list:
            for file_name in file_list:
                if 'Prosim737_backup_' in file_name and '.zip' in file_name:
                    self.listWidget.addItem(str(file_name))
    
    def select_list_item(self):
        self.rw_restoreButton.setEnabled(True)
        self.rw_deleteButton.setEnabled(True)
    
    def delete_backup(self):
        file_name = self.listWidget.currentItem().text()
        logging.debug('button_functions.py - MyRestore: delete backup ' + str(file_name))
        os.remove(self.backup_folder + '\\' + file_name)
        self.listWidget.clear()
        self.list_backups()
        self.rw_restoreButton.setEnabled(False)
        self.rw_deleteButton.setEnabled(False)
        
    def restore_backup(self):
        file_name = self.listWidget.currentItem().text()
        logging.debug('button_functions.py - MyRestore: restore backup ' + str(file_name))
        zip_file = zipfile.ZipFile(self.backup_folder + '\\' + file_name)
        xml_file = zip_file.read('backup_options.xml')
        backup_folders = self.read_backup_xml(xml_file)
        success = self.check_prosim_processes(backup_folders)
        if success is False:
            return
        success = self.check_prosim_paths(backup_folders)
        if success is False:
            return
        self.rw_restoreButton.setEnabled(False)
        self.rw_deleteButton.setEnabled(False)
        self.rw_cancelButton.setEnabled(False)
        self.label.setText('Unpacking backup...')
        self.progressBar.setEnabled(True)
        self.progressBar.setVisible(True)
        temp_path = tempfile.gettempdir()
        copyfile(self.backup_folder + '\\' + file_name, temp_path + '\prosim_update_package.zip')
        unpack_folder = temp_path + '\prosim_update_package'
        self.thread = UnpackFile(temp_path + '\prosim_update_package.zip', unpack_folder, True)
        self.thread.unpack_update.connect(self.update_progress_bar)
        self.thread.unpack_done.connect(self.install_backup)
        self.thread.start()
    
    def install_backup(self):
        logging.debug('button_functions.py - MyRestore: install backup')
        self.thread.unpack_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        self.update_progress_bar(0)
        self.label.setText('Installing backup...')
        unpack_folder = tempfile.gettempdir() + '\prosim_update_package\\'
        self.thread = InstallFile(unpack_folder, backup=True,)
        self.thread.install_update.connect(self.update_progress_bar)
        self.thread.install_done.connect(self.end_process)
        self.thread.start()

    def end_process(self):
        logging.debug('button_functions.py - MyRestore: end process')
        self.thread.install_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        self.update_progress_bar(100)
        self.rw_restoreButton.setEnabled(True)
        self.rw_deleteButton.setEnabled(True)
        self.rw_cancelButton.setEnabled(True)
        self.label.setText('Job finished !')

    def closeWindow(self):
        try:
            self.thread.terminated = True
            self.thread.exit()
        except AttributeError:
            pass
        self.close()
        
    def read_backup_xml(self, xml_file):
        path_dict = {}
        doc = xml.dom.minidom.parseString(str(xml_file,'utf-8'))
        backup_element = self.get_element(doc, 'BackupInstance')
        for element in backup_element:
            prosim_folder = self.get_element_value(element, 'BackupFile')[:-4]
            target_folder = self.get_element_value(element, 'BackupPath')
            path_dict[prosim_folder] = target_folder
        return path_dict
    
    def get_element(self, parent, element_name):
        return parent.getElementsByTagNameNS('ProsimUpdater', element_name)
    
    def get_element_value(self, parent, element_name):
        elements = parent.getElementsByTagNameNS('ProsimUpdater', element_name)
        if elements:
            element = elements[0]
            nodes = element.childNodes
            for node in nodes:
                if node.nodeType == node.TEXT_NODE:
                    return node.data.strip()
                
    def check_prosim_paths(self, backup_folders):
        logging.debug('button_functions.py - MyRestore: check_prosim_paths')
        success = True
        wrong_path = []
        for _, value in backup_folders.items():
            if not os.path.isdir(value):
                wrong_path.append(value)  
        if wrong_path:
            self.pathWindow = MyPath(wrong_path)
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.pathWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
            self.pathWindow.exec_()
            success = False
        logging.debug('button_functions.py - MyRestore: success ' + str(success))
        return success
    
    def check_prosim_processes(self, backup_folders):
        logging.debug('button_functions.py - MyRestore: check_prosim_processes')
        success = True
        prosim_processes = ['Prosim737.exe', 'ProsimAudio.exe', 'ProsimCDU.exe',
                            'ProsimMCP.exe', 'ProsimPanel.exe', 'ProsimDisplay.exe']
        running_processes = []
        computer_list = []
        for _, value in backup_folders.items():
                if value[:2] == '//':
                    index = value[2:].find('/')
                    computer_list.append(value[2:index+2])
                elif ':/' in value[:3]:
                    drive, _ = os.path.splitdrive(value)
                    computer_list.append(drive[1:])
        computer_list = list(set(computer_list))
        logging.debug('button_functions.py - MyRestore: check_prosim_processes, computer_list ' + str(computer_list))
        for computer in computer_list:
            if computer == ':':
                for pid in psutil.pids():
                    try:
                        if psutil.Process(pid).name() in prosim_processes:
                            running_processes.append('Local - ' + psutil.Process(pid).name())
                    except psutil.NoSuchProcess:
                        pass
            else:
                if self.prosim_credentials:
                    try:
                        username = self.prosim_credentials[computer]['username']
                        password = self.prosim_credentials[computer]['password']
                        if password:
                            command = 'tasklist.exe /s ' + computer + ' /u ' + username + ' /p ' + password
                        else:
                            command = 'tasklist.exe /s ' + computer + ' /u ' + username
                        remote_list = [line.split() for line in subprocess.check_output(command).splitlines()]
                        for process in remote_list[2:]:
                            try:
                                if process[0].decode('ascii') in prosim_processes:
                                    running_processes.append(computer + ' - ' + process[0].decode('ascii'))
                            except IndexError:
                                pass
                    except KeyError:
                        logging.exception('button_functions.py - MyUnpack: check_prosim_processes')
                else:
                    logging.debug('button_functions.py - MyRestore: check_prosim_processes, no credentials')
        if running_processes:
            text = ['The following processes are still running:',
                    'Please, make sure to stop them before installing Prosim737.']
            self.pathWindow = MyPath(running_processes, text)
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.pathWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
            self.pathWindow.exec_()
            success = False
        logging.debug('button_functions.py - MyRestore: success ' + str(success))
        return success


class MyPath(QtWidgets.QDialog, Ui_pathWindow):
    def __init__(self, wrong_path, text=None):
        QWidget.__init__(self)
        logging.debug('button_functions.py - MyPath invoked')
        self.setupUi(self)
        self.wrong_path = wrong_path
        self.iw_okButton.clicked.connect(self.closeWindow)
        if text:
            self.iw_label_1.setText(text[0])
            self.iw_label_3.setText(text[1])
        self.add_path_ui()
    
    def add_path_ui(self):
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        for path in self.wrong_path:
            if len(path) > 50:
                path = path[:15] + ' ... ' + path[path.rfind('/') + 1:]
            label = QtWidgets.QLabel()
            label.setMinimumSize(QtCore.QSize(0, 27))
            label.setMaximumSize(QtCore.QSize(16777215, 27))
            label.setFont(font)
            label.setFrameShape(QtWidgets.QFrame.NoFrame)
            label.setFrameShadow(QtWidgets.QFrame.Plain)
            label.setLineWidth(0)
            label.setMidLineWidth(0)
            label.setTextFormat(QtCore.Qt.AutoText)
            label.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
            label.setWordWrap(True)
            label.setObjectName("iw_label")
            label.setText(path)
            self.verticalLayout_2.addWidget(label)
    
    def closeWindow(self):
        self.close()

        
class DownloadFile(QThread):
    download_update = QtCore.pyqtSignal(int)
    download_done = QtCore.pyqtSignal()
    def __init__(self, url_name, update_file=None):
        QThread.__init__(self)
        logging.debug('button_functions.py - DownloadFile invoked')
        logging.debug('button_functions.py - DownloadFile: url_name ' + str(url_name)
                      + ' | update_file ' + str(update_file))
        self.url_name = url_name
        self.update_file = update_file
        self.terminated = False
    
    def run(self):
        def report(block_count, block_size, total_size):
            if block_count == 0:
                logging.debug('button_functions.py - DownloadFile: download started')
                self.download_update.emit(0)
            if (block_count * block_size) >= total_size:
                logging.debug('button_functions.py - DownloadFile: download finished')
                self.download_done.emit()
            incAmount = round(100*(block_count * block_size) / total_size)
            self.download_update.emit(incAmount)
        temp_path = tempfile.gettempdir()
        if not self.update_file:
            urllib.request.urlretrieve(self.url_name, temp_path + '\prosim_update_package.zip', reporthook=report)
        else:
            urllib.request.urlretrieve(self.url_name, self.update_file, reporthook=report)

    def stop(self):
        self.terminate()


class UnpackFile(QThread):
    unpack_update = QtCore.pyqtSignal(int)
    unpack_done = QtCore.pyqtSignal()
    def __init__(self, in_file, target_name, backup=False):
        QThread.__init__(self)
        logging.debug('button_functions.py - UnpackFile invoked')
        logging.debug('button_functions.py - UnpackFile: in_file ' + str(in_file) + ' | target_name '
                      + str(target_name) + ' | backup' + str(backup))
        self.backup = backup
        self.in_file = in_file
        self.target_name = target_name
        self.prosim_list = ['ProSim737', 'ProSimAudio', 'ProSimCDU',
                            'ProSimDisplay', 'ProSimMCP', 'ProSimPanel']
        
    def run(self):
        logging.debug('button_functions.py - UnpackFile: ' + self.in_file + ' | ' + self.target_name)
        self.unpack(self.in_file, self.target_name)
        if self.backup:
            file_list = []
            try:
                for name in os.listdir(self.target_name + '\\'):
                    if os.path.isfile(os.path.join(self.target_name, name)):
                        file_list.append(name)
            except Exception:
                logging.warning('button_functions.py - UnpackFile ' + str(Exception))
            if file_list:
                for file_name in file_list:
                    if '.zip' in file_name:
                        logging.debug('button_functions.py - UnpackFile: ' + self.target_name
                                      + '\\' + file_name + ' | ' + self.target_name + '\\'
                                      + file_name[:-4])
                        self.unpack(self.target_name + '\\' + file_name, self.target_name + '\\' + file_name[:-4])
        else:
            for folder in self.prosim_list:
                file_in = self.target_name + '\\' + folder + '.zip'
                logging.debug('button_functions.py - UnpackFile: ' + file_in + ' | ' + self.target_name)
                self.unpack(file_in, self.target_name)
        self.unpack_done.emit()
        
    def unpack(self, in_file, target_name):
        logging.debug('button_functions.py - UnpackFile: unpack started')
        self.unpack_update.emit(0)
        zf = zipfile.ZipFile(in_file, 'r')
        uncompress_size = sum((file.file_size for file in zf.infolist()))
        extracted_size = 0
        for file in zf.infolist():
            extracted_size += file.file_size
            percentage = round(extracted_size * 100/uncompress_size)
            self.unpack_update.emit(percentage)
            zf.extract(file, target_name)
        logging.debug('button_functions.py - UnpackFile: unpack finished')
        
    def stop(self):
        self.terminate()


class InstallFile(QThread):
    install_update = QtCore.pyqtSignal(int)
    install_done = QtCore.pyqtSignal()
    def __init__(self, directory, prosim_path=None, backup=False):
        QThread.__init__(self)
        logging.debug('button_functions.py - InstallFile invoked')
        logging.debug('button_functions.py - InstallFile: directory ' + str(directory) + ' | prosim_path '
                      + str(prosim_path) + ' | backup ' + str(backup))
        self.backup = backup
        self.directory = directory
        self.prosim_list = ['ProSim737', 'ProSimMCP', 'ProSimCDU', 
                            'ProSimDisplay', 'ProSimPanel', 'ProSimAudio']
        if prosim_path is not None:
            self.prosim_path = prosim_path

    def run(self):
        if self.backup:
            prosim_directories = self.read_backup_xml(self.directory + '\\backup_options.xml')
            for key in prosim_directories:
                prosim_folder = self.directory + '\\' + key
                num_files = self.count_files(prosim_folder)
                num_copied = 0
                for path, _, filenames in os.walk(prosim_folder):
                    for file in filenames:
                        source_file = os.path.join(path, file)
                        destFile = os.path.join(path.replace(prosim_folder, prosim_directories[key]), file)
                        if not os.path.isdir(os.path.dirname(destFile)):
                            os.makedirs(os.path.dirname(destFile))
                        copy(source_file, destFile)
                    num_copied += 1
                    percentage = int(round((num_copied/float(num_files))*100))
                    self.install_update.emit(percentage)
        else:
            for index, folder in enumerate(self.prosim_list):
                prosim_target = self.prosim_path[index]
                num_files = self.count_files(self.directory + folder)
                num_copied = 0
                for path, _, filenames in os.walk(self.directory + folder):
                    for file in filenames:
                        source_file = os.path.join(path, file)
                        for dest in prosim_target:
                            destFile = os.path.join(path.replace(self.directory + folder, dest), file)
                            if not os.path.isdir(os.path.dirname(destFile)):
                                os.makedirs(os.path.dirname(destFile))
                            copy(source_file, destFile)
                        num_copied += 1
                        percentage = int(round((num_copied/float(num_files))*100))
                        self.install_update.emit(percentage)
        self.install_done.emit()
    
    def count_files(self, directory):
        files = []
        if os.path.isdir(directory):
            for _, _, filenames in os.walk(directory):
                files.extend(filenames)
        return len(files)
    
    def read_backup_xml(self, xml_file):
        logging.debug('button_functions.py - InstallFile: read xml file')
        path_dict = {}
        f = open(xml_file, 'r')
        doc = xml.dom.minidom.parse(f)
        backup_element = self.get_element(doc, 'BackupInstance')
        for element in backup_element:
            prosim_folder = self.get_element_value(element, 'BackupFile')[:-4]
            target_folder = self.get_element_value(element, 'BackupPath')
            logging.debug('button_functions.py - InstallFile: prosim_folder ' + prosim_folder
                          + ' | target_folder ' + target_folder)
            path_dict[prosim_folder] = target_folder
        return path_dict
    
    def get_element(self, parent, element_name):
        return parent.getElementsByTagNameNS('ProsimUpdater', element_name)
    
    def get_element_value(self, parent, element_name):
        elements = parent.getElementsByTagNameNS('ProsimUpdater', element_name)
        if elements:
            element = elements[0]
            nodes = element.childNodes
            for node in nodes:
                if node.nodeType == node.TEXT_NODE:
                    return node.data.strip()
    
    def stop(self):
        self.terminate()
    
    
class ZipProsim(QThread):
    zip_update = QtCore.pyqtSignal(int)
    zip_done = QtCore.pyqtSignal()
    def __init__(self, directory, prosim_path):
        QThread.__init__(self)
        logging.debug('button_functions.py - ZipProsim invoked')
        logging.debug('button_functions.py - ZipProsim: directory ' + str(directory)
                      + ' | prosim_path' + str(prosim_path))
        self.directory = directory
        self.prosim_path = prosim_path
        self.temp_directory = tempfile.mkdtemp()

    def run(self):
        multiple_folder_list = []
        for path in self.prosim_path:
            multiple_folder_list.append(os.path.basename(os.path.normpath(path)))
        for x in set(multiple_folder_list):
            multiple_folder_list.remove(x)
        multiple_folder_list = list(set(multiple_folder_list))
        timestr = time.strftime("%Y-%m-%dT%H-%M-%S")
        timexml = time.strftime("%Y-%m-%d %H:%M:%S")
        backup_list = []
        i = 0
        for path in self.prosim_path:
            zip_name = os.path.basename(os.path.normpath(path))
            if multiple_folder_list:
                if zip_name in multiple_folder_list:
                    zip_name += '_' + str(i)
                    i += 1
            logging.debug('button_functions.py - ZipProsim: ' + self.temp_directory + '\\' + zip_name + '.zip'
                      + ' | ' + str(path))
            zipf = zipfile.ZipFile(self.temp_directory + '\\' + zip_name + '.zip', 'w', zipfile.ZIP_DEFLATED)
            self.zipdir(path + '\\', zipf)
            zipf.close()
            backup_list.append([zip_name + '.zip', path])
        self.create_backup_xml(self.temp_directory + '\\backup_options.xml', timexml, backup_list) 
        zipb = zipfile.ZipFile(self.directory + '\\Prosim737_backup_' + timestr + '.zip', 'w', zipfile.ZIP_DEFLATED)
        self.zipdir(self.temp_directory, zipb)
        zipb.close()
        rmtree(self.temp_directory)
        self.zip_done.emit() 
        
    def zipdir(self, path, ziph):
        num_files = 0
        for _, _, files in os.walk(path):
            for file in files:
                num_files += 1
        processed_files = 0
        len_path = len(path)
        for root, _, files in os.walk(path):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext != '.DEM':
                    file_path = os.path.join(root, file)
                    ziph.write(file_path, file_path[len_path:])
                    processed_files += 1
                    percentage = round(100 * (float(processed_files)/num_files))
                    self.zip_update.emit(percentage)

    def create_backup_xml(self, out_file_name, timestr, backup_list):
        doc = xml.dom.minidom.Document()
        doc_root = self.add_element(doc, "BackupOptions", doc)
        doc_root.setAttribute("xmlns:updater", 'ProsimUpdater')
        self.add_element(doc, "CreationTime", doc_root, timestr)
        for sublist in backup_list:
                backup_element = self.add_element(doc, "BackupInstance", doc_root)
                self.add_element(doc, "BackupFile", backup_element, sublist[0])
                self.add_element(doc, "BackupPath", backup_element, sublist[1])
        f = open(out_file_name, 'w')
        f.write(doc.toprettyxml())
        f.close()
        
    def add_element(self, doc, element_name, parent, value=None):
        new_element = doc.createElementNS('ProsimUpdater', 'updater:' + element_name)
        if value:
            new_text = doc.createTextNode(value)
            new_element.appendChild(new_text)
        parent.appendChild(new_element)
        return new_element

    def stop(self):
        self.terminate()
    