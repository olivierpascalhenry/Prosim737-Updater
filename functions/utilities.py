import logging
import tempfile
import os
from shutil import rmtree
from PyQt5 import QtWidgets, QtGui, QtCore
from ui.Ui_infowindow import Ui_infoWindow


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
    
    
def translate_elements(self, widget, language, text_translations):
    logging.debug('utilities.py - translate_elements - language ' + language)
    if isinstance(widget, QtWidgets.QTabWidget):
        all_widgets = widget.findChildren(QtWidgets.QWidget)
        for tab in all_widgets:
            try:
                widget.setTabText(widget.indexOf(tab),text_translations[tab.objectName()][language])
            except KeyError:
                pass
    all_labels = widget.findChildren(QtWidgets.QLabel)
    for label in all_labels:     
        try:
            label.setText(text_translations[label.objectName()][language])
        except KeyError:
            pass
    all_check = widget.findChildren(QtWidgets.QCheckBox)
    for check in all_check:
        try:
            check.setText(text_translations[check.objectName()][language])
        except KeyError:
            pass
    all_buttons = widget.findChildren(QtWidgets.QToolButton)
    for button in all_buttons:
        try:
            button.setText(text_translations[button.objectName()][language])
        except KeyError:
            pass
    
    all_actions = self.findChildren(QtWidgets.QAction)
    for action in all_actions:
        try:
            action.setText(text_translations[action.objectName()][language][0])
            action.setToolTip(text_translations[action.objectName()][language][1])
        except KeyError:
            pass
    
    
def translate_new_path_element(self, widget, language, category):
    logging.debug('utilities.py - translate_new_path_element - language ' + language + ' ; category ' + category)
    widget.setText(self.text_translations['user_lb'][language] % self.category_name[category])


def translate_all_path_credential_elements(self):
    complete_list = [self.server_lb_list, self.mcp_lb_list, self.cdu_lb_list, self.display_lb_list, self.panel_lb_list,self.audio_lb_list]
    module_list = ['Server', 'MCP', 'CDU', 'Display', 'Panel', 'Audio']
    for i, sublist in enumerate(complete_list):
        for label in sublist:
            label.setText(self.text_translations['user_lb'][self.config_dict['OPTIONS'].get('language')] % module_list[i])
    for label in self.cred_lb_3_list:
        label.setText(self.text_translations['cred_lb_3_list'][self.config_dict['OPTIONS'].get('language')])
    for label in self.cred_lb_2_list:
        label.setText(self.text_translations['cred_lb_2_list'][self.config_dict['OPTIONS'].get('language')])
    for label in self.cred_lb_1_list:
        label.setText(self.text_translations['cred_lb_1_list'][self.config_dict['OPTIONS'].get('language')])


class MyInfo(QtWidgets.QDialog, Ui_infoWindow):
    def __init__(self, infoText):
        logging.debug('window_functions.py - MyInfo - __init__')
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.iw_label_1.setText(infoText)
        self.iw_okButton.clicked.connect(self.closeWindow)
        
    def closeWindow(self):
        logging.debug('window_functions.py - MyInfo - closeWindow')
        self.close()
