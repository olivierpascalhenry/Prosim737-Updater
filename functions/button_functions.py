import tempfile
import logging
from shutil import copyfile
from PyQt5 import QtWidgets, QtCore, QtGui
from functions.window_functions import MyInfo, MyDownload, MyUnpack, MyStore, MyCompress, MyRestore, MyLog
from functions.utilities import load_prosim_path, load_prosim_credentials, remove_tmp_package, warning_window
import os


def info_button(self):
    logging.debug('button_functions.py - info_button - self.sender().objectName() ' + self.sender().objectName())
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
    logging.debug('button_functions.py - add_path - self.sender().objectName() ' + self.sender().objectName())
    index_object = self.sender().objectName().index('_bt_')
    category = self.sender().objectName()[:index_object]
    num = self.sender().objectName()[index_object+4:]
    path = self.get_directory()
    if path:
        line_object = self.findChildren(QtWidgets.QLineEdit, category + '_ln_' + num)
        line_object[0].setText(path.replace('/','\\'))
        self.set_modified()


def new_path(self, category=None, path=None):
    try:
        logging.debug('button_functions.py - new_path - self.sender().objectName() ' + self.sender().objectName()
                      + ' ; category ' + str(category) + ' ; path ' + str(path))
    except AttributeError as e:
        logging.exception('button_functions.py - new_path - AttributeError ' + str(e))
    if not category:
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
        ln_object[num_object].setText(path.replace('/','\\'))
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
    logging.debug('button_functions.py - new_credentials - credentials ' + str(credentials))
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
    logging.debug('button_functions.py - del_credentials - self.sender().objectName() ' + self.sender().objectName()
                  + ' ; index ' + str(index))
    if index == None:
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
    logging.debug('button_functions.py - del_path - self.sender().objectName() ' + self.sender().objectName()
                  + ' ; index ' + str(index) + ' ; category ' + str(category))
    if index == None:
        index = int(self.sender().objectName()[-1:])
    if category == None:
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
    logging.debug('button_functions.py - create_backup')
    if os.path.isdir(self.home_ln_2.text() + '\\'):
        prosim_path = load_prosim_path(self, [self.tabWidgetPage2,self.tabWidgetPage3,self.tabWidgetPage4,
                                              self.tabWidgetPage5, self.tabWidgetPage6, self.tabWidgetPage7])
        prosim_credentials = load_prosim_credentials(self)
        if prosim_path:
            self.compressWindow = MyCompress(self.home_ln_2.text(), prosim_path, prosim_credentials)
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.compressWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.compressWindow.setGeometry(x2, y2, w2, h2)
            self.compressWindow.setMinimumSize(QtCore.QSize(500, self.compressWindow.sizeHint().height()))
            self.compressWindow.setMaximumSize(QtCore.QSize(500, self.compressWindow.sizeHint().height()))
            self.compressWindow.exec_()
        else :
            logging.debug('button_functions.py - update_prosim - no path in prosim modules')
            infoText = 'There is no path entered for the different Prosim737 modules, consequently it is not possible '\
                        + ' to create a backup. Please enter at least one path.'
            warning_window(self, infoText)
    else:
        logging.debug('button_functions.py - create_backup - path is not valid')
        infoText = 'The path to store a backup is not valid. Please check the path.'
        warning_window(self, infoText)


def restore_backup(self, kill, relaunch):
    logging.debug('button_functions.py - restore_backup')
    remove_tmp_package(self)
    self.restoreWindow = MyRestore(self.home_ln_2.text(), kill, relaunch)
    x1, y1, w1, h1 = self.geometry().getRect()
    _, _, w2, h2 = self.restoreWindow.geometry().getRect()
    x2 = x1 + w1/2 - w2/2
    y2 = y1 + h1/2 - h2/2
    self.restoreWindow.setGeometry(x2, y2, w2, h2)
    self.restoreWindow.setMinimumSize(QtCore.QSize(600, self.restoreWindow.sizeHint().height()))
    self.restoreWindow.setMaximumSize(QtCore.QSize(600, self.restoreWindow.sizeHint().height()))
    self.restoreWindow.exec_()


def update_prosim(self, kill, relaunch):
    logging.debug('button_functions.py - update_prosim - self.selected_list_widget ' + str(self.selected_list_widget))
    prosim_path = load_prosim_path(self, [self.tabWidgetPage2,self.tabWidgetPage3,self.tabWidgetPage4,
                                          self.tabWidgetPage5, self.tabWidgetPage6, self.tabWidgetPage7])
    if prosim_path:
        logging.debug('button_functions.py - update_prosim - update, prosim_path ' + str(prosim_path))
        prosim_credentials = load_prosim_credentials(self)
        remove_tmp_package(self)
        if self.selected_list_widget == 'online':
            url_name = self.update_package_path + self.update_package_name
            self.downloadWindow = MyDownload(url_name, prosim_path, prosim_credentials, kill, relaunch)
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.downloadWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.downloadWindow.setGeometry(x2, y2, w2, h2)
            self.downloadWindow.setMinimumSize(QtCore.QSize(650, self.downloadWindow.sizeHint().height()))
            self.downloadWindow.setMaximumSize(QtCore.QSize(650, self.downloadWindow.sizeHint().height()))
            self.downloadWindow.exec_()
        elif self.selected_list_widget == 'local':
            copyfile(self.update_package_path + self.update_package_name, tempfile.gettempdir() + '\prosim_update_package.zip')
            self.unpackWindow = MyUnpack(prosim_path, prosim_credentials, kill, relaunch)
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.unpackWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.unpackWindow.setGeometry(x2, y2, w2, h2)
            self.unpackWindow.setMinimumSize(QtCore.QSize(650, self.unpackWindow.sizeHint().height()))
            self.unpackWindow.setMaximumSize(QtCore.QSize(650, self.unpackWindow.sizeHint().height()))
            self.unpackWindow.exec_()
    else:
        logging.debug('button_functions.py - update_prosim - no path in prosim modules')
        infoText = 'There is no path entered for the different Prosim737 modules. Please enter at least one path.'
        warning_window(self, infoText)


def store_update(self):
    logging.debug('button_functions.py - store_update - self.selected_list_widget ' + str(self.selected_list_widget))
    if self.selected_list_widget == 'online':
        url_name = self.update_package_path + self.update_package_name
        update_file = self.home_ln_1.text() + '\\' + self.update_package_name
        self.storeWindow = MyStore(url_name, update_file)
        self.storeWindow.label.setText('Downloading ' + self.update_package_name + '...')
        x1, y1, w1, h1 = self.geometry().getRect()
        _, _, w2, h2 = self.storeWindow.geometry().getRect()
        x2 = x1 + w1/2 - w2/2
        y2 = y1 + h1/2 - h2/2
        self.storeWindow.setGeometry(x2, y2, w2, h2)
        self.storeWindow.setMinimumSize(QtCore.QSize(500, self.storeWindow.sizeHint().height()))
        self.storeWindow.setMaximumSize(QtCore.QSize(500, self.storeWindow.sizeHint().height()))
        self.storeWindow.exec_()
        self.check_prosim737_local_updates()


def display_changelog(self):
    logging.debug('button_functions.py - display_changelog')
    self.logWindow = MyLog()
    x1, y1, w1, h1 = self.geometry().getRect()
    _, _, w2, h2 = self.logWindow.geometry().getRect()
    x2 = x1 + w1/2 - w2/2
    y2 = y1 + h1/2 - h2/2
    self.logWindow.setGeometry(x2, y2, w2, h2)
    self.logWindow.lg_txBrower.setPlainText(open('documentation\prosim_changelog.txt').read().replace('»', '').replace('ï', '').replace('¿', ''))
    self.logWindow.exec_()
