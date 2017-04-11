import os
import requests
import logging
from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QLineEdit, QListWidget
from PyQt5.QtGui import QCursor
from ui.Ui_mainwindow import Ui_MainWindow
from ui.Ui_aboutwindow import Ui_aboutWindow
from ui.Ui_logwindow import Ui_Changelog
from ui.Ui_presavewindow import Ui_presaveWindow
from ui.Ui_infowindow import Ui_infoWindow
from ui._version import _updater_version, _eclipse_version, _py_version, _qt_version
from functions.updater_xml import create_updater_xml, read_updater_xml
from functions.button_functions import info_button, create_backup, restore_backup
from functions.button_functions import update_prosim, add_path, new_path, del_path
from functions.button_functions import new_credentials, del_credentials, store_update
from functions.objects_functions import objectsInit
from bs4 import BeautifulSoup


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        logging.info('mainwindow.py - UI initialization ...')
        self.setupUi(self)
        objectsInit(self)
        self.modified = False
        self.saved = False
        self.update_package_name = ''
        self.update_package_path = ''
        self.selected_list_widget = ''
        self.online_activated = False
        self.local_activated = False
        self.home_create_backup.setEnabled(False)
        self.home_restore_backup.setEnabled(False)
        self.home_update.setEnabled(False)
        self.home_store.setEnabled(False)
        all_line_edits = self.findChildren(QLineEdit)
        for widget in all_line_edits:
            widget.textChanged.connect(lambda: self.set_modified())
        all_tool_buttons = self.findChildren(QtWidgets.QToolButton)
        for widget in all_tool_buttons:
            widget.clicked.connect(lambda: self.tool_button_clicked())
        self.home_ck_1.stateChanged.connect(lambda: self.read_online_prosim_website())
        self.home_ck_1.stateChanged.connect(lambda: self.set_modified())
        self.listWidget_2.itemClicked.connect(lambda: self.select_list_item())
        self.listWidget_2.itemSelectionChanged.connect(lambda: self.update_store_button_state())
        self.listWidget_2.itemSelectionChanged.connect(lambda: self.update_update_button_state())
        self.listWidget.itemClicked.connect(lambda: self.select_list_item())
        self.listWidget.itemSelectionChanged.connect(lambda: self.update_update_button_state())
        self.home_ln_1.textChanged.connect(lambda: self.update_local_list())
        self.home_ln_2.textChanged.connect(lambda: self.update_backup_buttons_state())
        try:
            read_updater_xml(self, 'prosim_udpater_options.xml')
            self.saved = True
        except FileNotFoundError:
            logging.exception('mainwindow.py - xml file not found, no options loaded')
        self.make_window_title()
        logging.info('mainwindow.py - UI initialized ...')
        logging.info('*****************************************')

    @QtCore.pyqtSlot()
    def on_actionSave_triggered(self):
        self.save_document()

    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        self.open_document()

    @QtCore.pyqtSlot()
    def on_actionExit_triggered(self):
        self.close()

    @QtCore.pyqtSlot()
    def on_actionAbout_triggered(self):
        self.open_about()

    @QtCore.pyqtSlot()
    def on_actionChangelog_triggered(self):
        self.open_changelog()

    def save_document(self):
        logging.debug('mainwindow.py - saving of the options invoked')
        xml_file = 'prosim_udpater_options.xml'
        create_updater_xml(self, xml_file)
        self.make_window_title()
        
    def open_document(self):
        logging.debug('mainwindow.py - opening of the options invoked')
        if self.modified:
            result = self.make_onsave_msg_box("Open")
            if result == "iw_saveButton":
                self.save_document()
                self.open_file()
            elif result == "iw_nosaveButton":
                self.open_file()
        else:
            self.open_file()
            
    def open_about(self):
        logging.debug('mainwindow.py - about window invoked')
        about_text = ('The Prosim737 Updater v' + _updater_version + ' was developed by Olivier Henry,'
                      + ' using Eclipse ' + _eclipse_version + ', Python ' + _py_version + ' and PyQt '
                      + _qt_version + '. Its purpose is to help people to update easily and quickly an'
                      + ' installation of Prosim737 across few computers.')
        self.aboutWindow = MyAbout(about_text)
        x1, y1, w1, h1 = self.geometry().getRect()
        _, _, w2, h2 = self.aboutWindow.geometry().getRect()
        x2 = x1 + w1/2 - w2/2
        y2 = y1 + h1/2 - h2/2
        self.aboutWindow.setGeometry(x2, y2, w2, h2)
        self.aboutWindow.setMinimumSize(QtCore.QSize(480, self.aboutWindow.sizeHint().height()))
        self.aboutWindow.setMaximumSize(QtCore.QSize(480, self.aboutWindow.sizeHint().height()))
        self.aboutWindow.exec_()
        
    def open_changelog(self):
        logging.debug('mainwindow.py - changelog window invoked')
        self.logWindow = MyLog()
        x1, y1, w1, h1 = self.geometry().getRect()
        _, _, w2, h2 = self.logWindow.geometry().getRect()
        x2 = x1 + w1/2 - w2/2
        y2 = y1 + h1/2 - h2/2
        self.logWindow.setGeometry(x2, y2, w2, h2)
        self.logWindow.exec_()

    def closeEvent(self, event):
        logging.debug('mainwindow.py - close event invoked')
        if self.modified:
            result = self.make_onsave_msg_box("Close")
            if result == "iw_saveButton":
                self.save_document()
                event.accept()
            elif result == "iw_nosaveButton":
                event.accept()
            else:
                event.ignore()
        else:
            self.close()

    def make_window_title(self):
        logging.debug('mainwindow.py - make_window_title invoked: saved ' + 
                      str(self.saved) + ' ; modified ' + str(self.modified))
        if self.saved:
            title_string = "Prosim737 Updater v{0}".format(_updater_version)
        else:
            title_string = "Prosim737 Updater v{0} - unsaved".format(_updater_version)
        if self.modified:
            title_string += ' - modified'
        self.setWindowTitle(title_string)

    def set_modified(self):
        logging.debug('mainwindow.py - set_modified invoked')
        if not self.modified:
            self.modified = True
            self.make_window_title()

    '''def get_file_name(self):
        logging.debug('mainwindow.py - get_filename invoked')
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setDefaultSuffix('xml')
        out_file_name, _ = file_dialog.getSaveFileName(self, "Save XML File", filter='XML Files (*.xml)')
        logging.debug('mainwindow.py - get_filename: ' + str(out_file_name))
        return out_file_name'''

    def get_directory(self):
        logging.debug('mainwindow.py - get_directory invoked')
        file_dialog = QtWidgets.QFileDialog()
        out_dir = file_dialog.getExistingDirectory(self, "Select Directory")
        logging.debug('mainwindow.py - get_directory: ' + str(out_dir))
        return str(out_dir)

    def reset_all_fields(self):
        logging.debug('mainwindow.py - reset_all_fields invoked')
        all_check_boxes = self.findChildren(QtWidgets.QCheckBox)
        for check_box in all_check_boxes:
            check_box.setCheckState(False)
        all_line_edits = self.findChildren(QLineEdit)
        for widget in all_line_edits:
            widget.clear()
        all_list_widgets = self.findChildren(QListWidget)
        for widget in all_list_widgets:
            widget.clear()
        for i in reversed(range(self.server_vl.count())):
            if i == 0:
                break
            del_path(self, i, 'server')
        for i in reversed(range(self.mcp_vl.count())):
            if i == 0:
                break
            del_path(self, i, 'mcp')
        for i in reversed(range(self.cdu_vl.count())):
            if i == 0:
                break
            del_path(self, i, 'cdu')
        for i in reversed(range(self.display_vl.count())):
            if i == 0:
                break
            del_path(self, i, 'display')
        for i in reversed(range(self.panel_vl.count())):
            if i == 0:
                break
            del_path(self, i, 'panel')
        for i in reversed(range(self.audio_vl.count())):
            if i == 0:
                break
            del_path(self, i, 'audio')
        for i in reversed(range(self.credentials_vl.count())):
            del_credentials(self, i)
        objectsInit(self)
        self.make_window_title()
        logging.debug('mainwindow.py - reset_all_fields OK')

    def open_file(self):
        logging.debug('mainwindow.py - open_file invoked')
        out_file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self,'Open XML File','','XML Files (*.xml)')
        logging.debug('mainwindow.py - get_filename: ' + str(out_file_name))
        if out_file_name:
            self.reset_all_fields()
            read_updater_xml(self, out_file_name)
            self.saved = True
            self.make_window_title()
            self.set_modified()

    def make_onsave_msg_box(self, string):
        logging.debug('mainwindow.py - warning message invoked')
        self.presaveWindow = MyWarning(string)
        x1, y1, w1, h1 = self.geometry().getRect()
        _, _, w2, h2 = self.presaveWindow.geometry().getRect()
        x2 = x1 + w1/2 - w2/2
        y2 = y1 + h1/2 - h2/2
        self.presaveWindow.setGeometry(x2, y2, w2, h2)
        self.presaveWindow.setMinimumSize(QtCore.QSize(450, self.presaveWindow.sizeHint().height()))
        self.presaveWindow.setMaximumSize(QtCore.QSize(452, self.presaveWindow.sizeHint().height()))
        self.presaveWindow.exec_()
        return self.presaveWindow.buttonName
    
    def tool_button_clicked(self):
        if "info" in self.sender().objectName():
            info_button(self)
        elif "create" in self.sender().objectName():
            create_backup(self)
        elif "restore" in self.sender().objectName():
            restore_backup(self)
        elif "update" in self.sender().objectName():
            update_prosim(self)
        elif "store" in self.sender().objectName():
            store_update(self)
        elif "new" in self.sender().objectName():
            new_path(self)
        elif "cred_delete" in self.sender().objectName():
            del_credentials(self)
        elif "delete_bt" in self.sender().objectName():
            del_path(self)
        elif "credentials" in self.sender().objectName():
            new_credentials(self)
        else:
            if "_bt_" in self.sender().objectName():
                add_path(self)
            
    def read_online_prosim_website(self):
        logging.debug('mainwindow.py - read_online_prosim_website invoked')
        self.listWidget_2.clear()
        if self.home_ck_1.isChecked():
            self.home_lb_4.setEnabled(True)
            self.listWidget_2.setEnabled(True)
            file_names = []
            try:
                url = 'http://prosim-ar.com/downloads/'
                soup = BeautifulSoup(requests.get(url).text, "html.parser")
                file_list = (soup.find_all('a'))
                for i in file_list:
                    link = i.get('href', None)
                    if link is not None and 'zip' in link and 'ProSim737-v' in link:
                        file_names.append(link[link.rfind('/')+1:])
                if 'ProSim737-v1.46.zip' in file_names:
                    file_names.remove('ProSim737-v1.46.zip')
                url = 'http://download.prosim-ar.com/ProSim737beta/'
                soup = BeautifulSoup(requests.get(url).text, "html.parser")
                file_list = (soup.find_all('a'))
                for i in file_list:
                    file_name = i.extract().get_text()
                    if "ProSim737" in file_name:
                        file_names.append(file_name)    
                self.listWidget_2.addItems(file_names)
                if self.listWidget_2.count() > 0:
                    self.online_activated = True
            except Exception:
                logging.error('mainwindow.py - read_online_prosim_website: internet connection error - url ' +
                              url)
                self.online_activated = False
                infoText = "Prosim Updater can't check online updates. Please check your internet connection."
                x = QCursor.pos().x()
                y = QCursor.pos().y()    
                x = x - 175
                y = y + 50
                self.infoWindow = MyInfo(infoText)
                self.infoWindow.setMinimumSize(QtCore.QSize(450, self.infoWindow.sizeHint().height()))
                self.infoWindow.setMaximumSize(QtCore.QSize(450, self.infoWindow.sizeHint().height()))
                self.infoWindow.setGeometry(x, y, 450, self.infoWindow.sizeHint().height())
                self.infoWindow.exec_()
        else:
            self.home_lb_4.setEnabled(False)
            self.listWidget_2.setEnabled(False)
            self.online_activated = False

    def select_list_item(self):
        logging.debug('mainwindow.py - select_list_item invoked')
        if self.sender().objectName() == 'listWidget':
            self.listWidget_2.clearSelection()
            self.update_package_name = self.listWidget.currentItem().text()
            self.update_package_path = self.home_ln_1.text() + '/'
            self.selected_list_widget = 'local'
        else:
            self.listWidget.clearSelection() 
            self.update_package_name = self.listWidget_2.currentItem().text()
            if 'b' in self.update_package_name:
                self.update_package_path = 'http://download.prosim-ar.com/ProSim737beta/'
            else:
                self.update_package_path = 'http://prosim-ar.com/download/'
            self.selected_list_widget = 'online'
        logging.debug('mainwindow.py - select_list_item: ' + self.update_package_name + ' | ' + self.selected_list_widget)

    def update_local_list(self):
        logging.debug('mainwindow.py - update_local_list invoked')
        self.listWidget.clear()
        path = self.home_ln_1.text() + '/'
        file_list = []
        try:
            for name in os.listdir(path):
                if os.path.isfile(os.path.join(path, name)):
                    file_list.append(name)
        except Exception:
            logging.warning('mainwindow.py - update_local_list: no update | ' + str(path))
            self.local_activated = False
        if file_list:
            for file_name in file_list:
                if 'ProSim737' in file_name and '.zip' in file_name:
                    self.listWidget.addItem(str(file_name))
            self.local_activated = True
        else:
            self.local_activated = False
        logging.warning('mainwindow.py - update_local_list: file list ' + str(len(file_list)))
    
    def update_backup_buttons_state(self):
        logging.debug('mainwindow.py - update_backup_buttons_state invoked')
        if self.home_ln_2.text():
            self.home_create_backup.setEnabled(True)
            self.home_restore_backup.setEnabled(True)
        else:
            self.home_create_backup.setEnabled(False)
            self.home_restore_backup.setEnabled(False)
        logging.debug('mainwindow.py - update_backup_buttons_state: Create ' 
                      + str(self.home_create_backup.isEnabled()) + ' | Backup '
                      + str(self.home_restore_backup.isEnabled()))
            
    def update_store_button_state(self):
        logging.debug('mainwindow.py - update_store_button_state invoked')
        if self.listWidget_2.currentItem().isSelected():
            self.home_store.setEnabled(True)
        else:
            self.home_store.setEnabled(False)
        logging.debug('mainwindow.py - update_store_button_state: Store '
                      + str(self.home_store.isEnabled()))
    
    def update_update_button_state(self):
        logging.debug('mainwindow.py - update_update_button_state invoked')
        left, right = False, False
        try:
            right = self.listWidget_2.currentItem().isSelected()
        except AttributeError:
            pass
        try:
            left = self.listWidget.currentItem().isSelected()
        except AttributeError:
            pass
        if left or right:
            self.home_update.setEnabled(True)
        else:
            self.home_update.setEnabled(False)
        logging.debug('mainwindow.py - update_update_button_state: Update '
                      + str(self.home_update.isEnabled()) + ' | right '
                      + str(right) + ' | left ' + str(left)) 
        

class MyAbout(QtWidgets.QDialog, Ui_aboutWindow):
    def __init__(self, aboutText):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.aw_label_1.setText(aboutText)
        self.aw_okButton.clicked.connect(self.closeWindow)

    def closeWindow(self):
        self.close()
        
        
class MyLog(QtWidgets.QDialog, Ui_Changelog):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.lg_txBrower.setPlainText(open("documentation/changelog.txt").read())
        self.lg_okButton.clicked.connect(self.closeWindow)
        
    def closeWindow(self):
        self.close()
        
        
class MyWarning(QtWidgets.QDialog, Ui_presaveWindow):
    def __init__(self, string):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.iw_cancelButton.setFocus(True)
        all_buttons = self.findChildren(QtWidgets.QToolButton)
        for widget in all_buttons:
            widget.clicked.connect(self.closeWindow)
        self.iw_nosaveButton.setText(string + " without saving")

    def closeWindow(self):
        self.buttonName = self.sender().objectName()
        self.close()


class MyInfo(QtWidgets.QDialog, Ui_infoWindow):
    def __init__(self, infoText):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.iw_label_1.setText(infoText)
        self.iw_okButton.clicked.connect(self.closeWindow)
        
    def closeWindow(self):
        self.close()