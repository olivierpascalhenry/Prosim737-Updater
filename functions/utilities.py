import logging
import tempfile
import os
from shutil import rmtree
from PyQt5 import QtWidgets, QtGui, QtCore
from functions.window_functions import MyInfo


def load_prosim_path(self, tab_list):
    logging.debug('utilities.py - load_prosim_path')
    prosim_list = ['ProSim737', 'ProSimMCP', 'ProSimCDU', 'ProSimDisplay', 'ProSimPanel', 'ProSimAudio']
    prosim_path = {}
    for index, tab in enumerate(tab_list):
        line_list = tab.findChildren(QtWidgets.QLineEdit)
        path_list = []
        empty_tab = True
        for line in line_list:
            if line.text():
                path_list.append(line.text())
                empty_tab = False
        if not empty_tab:
            prosim_path[prosim_list[index]] = path_list      
    return prosim_path


def load_prosim_credentials(self):
    logging.debug('utilities.py - load_prosim_credentials')
    credential_list = {}
    for i in range(0, len(self.cred_ln_1_list)):
        if self.cred_ln_1_list[i].text() and self.cred_ln_2_list[i].text():
            credential_list[self.cred_ln_1_list[i].text()] = {'username' : self.cred_ln_2_list[i].text(),
                                                              'password' : self.cred_ln_3_list[i].text()}
    return credential_list


def remove_tmp_package(self):
    logging.debug('utilities.py - remove_tmp_package')
    try:
        os.remove(tempfile.gettempdir() + '\prosim_update_package.zip')
    except FileNotFoundError:
        pass
    try:
        rmtree(tempfile.gettempdir() + '\prosim_update_package')
    except FileNotFoundError:
        pass
    

def warning_window(self, text):
    logging.debug('utilities.py - warning_window')
    self.infoWindow = MyInfo(text)
    x1, y1, w1, h1 = self.geometry().getRect()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("icons/warning_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    self.infoWindow.setWindowIcon(icon)
    self.infoWindow.setWindowTitle('Warning')
    self.infoWindow.iw_label_2.setPixmap(QtGui.QPixmap("icons/warning_popup_icon.svg"))
    _, _, w2, h2 = self.infoWindow.geometry().getRect()
    x2 = x1 + w1/2 - w2/2
    y2 = y1 + h1/2 - h2/2
    self.infoWindow.setMinimumSize(QtCore.QSize(450, self.infoWindow.sizeHint().height()))
    self.infoWindow.setMaximumSize(QtCore.QSize(450, self.infoWindow.sizeHint().height()))
    self.infoWindow.setGeometry(x2, y2, w2, h2)
    self.infoWindow.exec_()
