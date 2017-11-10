import os
import logging
import tempfile
import time
from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from ui.Ui_mainwindow import Ui_MainWindow
from ui._version import _updater_version
from functions.updater_xml import create_updater_xml, read_updater_xml
from functions.button_functions import info_button, create_backup, restore_backup
from functions.button_functions import update_prosim, add_path, new_path, del_path
from functions.button_functions import new_credentials, del_credentials, store_update
from functions.button_functions import display_changelog
from functions.objects_functions import objectsInit
from functions.window_functions import MyUpdate, MyOptions, MyWarning, MyAbout, MyLog, MyInfo
from functions.thread_functions import CheckProsim737Online, CheckProsim737UpdaterOnline, DownloadFile
from functions.utilities import translate_elements, translate_all_path_credential_elements


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, path, config_dict, translations, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.config_dict = config_dict
        self.config_path = path
        self.text_translations = translations
        logging.info('mainwindow.py - UI initialization ...')
        self.setupUi(self)
        objectsInit(self)
        self.link_latest_version = None
        self.modified = False
        self.saved = False
        self.update_package_name = ''
        self.update_package_path = ''
        self.selected_list_widget = ''
        all_tool_buttons = []
        all_line_edits = []
        for i in range(self.tabWidget.count()):
            all_tool_buttons += getattr(self,'tabWidgetPage' + str(i + 1)).findChildren(QtWidgets.QToolButton)
            all_line_edits += getattr(self,'tabWidgetPage' + str(i + 1)).findChildren(Qt.QLineEdit)
        for widget in all_line_edits:
            widget.textChanged.connect(self.set_modified)
        for widget in all_tool_buttons:
            widget.clicked.connect(self.tool_button_clicked)
        self.home_ck_1.stateChanged.connect(self.check_prosim737_online_updates)
        self.home_ck_1.stateChanged.connect(self.set_modified)
        self.listWidget_2.itemClicked.connect(self.select_list_item)
        self.listWidget_2.itemSelectionChanged.connect(self.update_store_button_state)
        self.listWidget_2.itemSelectionChanged.connect(self.update_update_button_state)
        self.listWidget.itemClicked.connect(self.select_list_item)
        self.listWidget.itemSelectionChanged.connect(self.update_update_button_state)
        self.home_ln_1.textChanged.connect(self.check_prosim737_local_updates)
        self.home_ln_2.textChanged.connect(self.update_backup_buttons_state)
        self.home_ln_1.textChanged.connect(self.update_store_button_state)
        self.create_language_list()
        self.check_language_config()
        translate_elements(self, self.tabWidget, self.config_dict['OPTIONS'].get('language'), self.text_translations)
        self.download_prosim737_changelog()
        self.check_prosim737updater_update()
        self.make_window_title()
        try:
            read_updater_xml(self, 'prosim_udpater_options.xml')
            self.saved = True
        except FileNotFoundError:
            logging.exception('mainwindow.py - xml file not found, no user options loaded')
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
    
    @QtCore.pyqtSlot()
    def on_actionOptions_triggered(self):
        self.open_options()
    
    @QtCore.pyqtSlot()
    def on_actionUpdate_triggered(self):
        self.download_and_install_prosim737updater_update()

    def save_document(self):
        logging.debug('mainwindow.py - save_document')
        xml_file = 'prosim_udpater_options.xml'
        create_updater_xml(self, xml_file)
        self.make_window_title()
        
    def open_document(self):
        logging.debug('mainwindow.py - open_document')
        if self.modified:
            result = self.make_onsave_msg_box(self.text_translations['iw_nosaveButton-text-open'][self.config_dict['OPTIONS'].get('language')])
            if result == "iw_saveButton":
                self.save_document()
                self.open_file()
            elif result == "iw_nosaveButton":
                self.open_file()
        else:
            self.open_file()
            
    def open_about(self):
        logging.debug('mainwindow.py - open_about')
        self.aboutWindow = MyAbout(self.config_dict, self.text_translations)
        x1, y1, w1, h1 = self.geometry().getRect()
        _, _, w2, h2 = self.aboutWindow.geometry().getRect()
        x2 = x1 + w1/2 - w2/2
        y2 = y1 + h1/2 - h2/2
        self.aboutWindow.setGeometry(x2, y2, w2, h2)
        self.aboutWindow.setMinimumSize(QtCore.QSize(480, self.aboutWindow.sizeHint().height()))
        self.aboutWindow.setMaximumSize(QtCore.QSize(480, self.aboutWindow.sizeHint().height()))
        self.aboutWindow.exec_()
        
    def open_changelog(self):
        logging.debug('mainwindow.py - open_changelog')
        self.logWindow = MyLog()
        x1, y1, w1, h1 = self.geometry().getRect()
        _, _, w2, h2 = self.logWindow.geometry().getRect()
        x2 = x1 + w1/2 - w2/2
        y2 = y1 + h1/2 - h2/2
        self.logWindow.setGeometry(x2, y2, w2, h2)
        self.logWindow.exec_()
           
    def open_options(self):
        logging.debug('mainwindow.py - open_options')
        language_before = self.config_dict.get('OPTIONS', 'language')
        self.optionWindow = MyOptions(self.config_dict, self.text_translations, self.language_list)
        x1, y1, w1, h1 = self.geometry().getRect()
        _, _, w2, h2 = self.optionWindow.geometry().getRect()
        x2 = x1 + w1/2 - w2/2
        y2 = y1 + h1/2 - h2/2
        self.optionWindow.setGeometry(x2, y2, w2, h2)
        self.optionWindow.exec_()
        if not self.optionWindow.cancel:
            self.config_dict = self.optionWindow.config_dict
            language_after = self.config_dict.get('OPTIONS', 'language')
            with open(os.path.join(self.config_path, 'prosim_updater.ini'), 'w') as config_file:
                self.config_dict.write(config_file)
            logging.getLogger().setLevel(self.config_dict.get('LOG', 'level'))
            self.check_prosim737updater_update()
            if language_before != language_after:
                translate_elements(self, self.tabWidget, language_after, self.text_translations)
                translate_all_path_credential_elements(self)
            
    def closeEvent(self, event):
        logging.debug('mainwindow.py - closeEvent')
        if self.modified:
            result = self.make_onsave_msg_box(self.text_translations['iw_nosaveButton-text-close'][self.config_dict['OPTIONS'].get('language')])
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
        logging.debug('mainwindow.py - make_window_title - self.modified ' + str(self.modified) +
                      ' ; self.saved ' + str(self.saved))
        title_string = 'Prosim737 Updater v' + _updater_version
        saved_string = ''
        modified_string = ''
        if not self.saved:
            saved_string = ' - unsaved'
        if self.modified:
            modified_string = ' - modified'
        title_string = title_string + saved_string + modified_string
        self.setWindowTitle(title_string)

    def set_modified(self):
        logging.debug('mainwindow.py - set_modified')
        if not self.modified:
            self.modified = True
            self.make_window_title()

    def get_directory(self):
        logging.debug('mainwindow.py - get_directory')
        file_dialog = QtWidgets.QFileDialog()
        out_dir = file_dialog.getExistingDirectory(self, "Select Directory")
        logging.debug('mainwindow.py - get_directory - ' + str(out_dir))
        return str(out_dir)

    def reset_all_fields(self):
        logging.debug('mainwindow.py - reset_all_fields - starting...')
        all_check_boxes = self.findChildren(QtWidgets.QCheckBox)
        for check_box in all_check_boxes:
            check_box.setCheckState(False)
        all_line_edits = self.findChildren(Qt.QLineEdit)
        for widget in all_line_edits:
            widget.clear()
        all_list_widgets = self.findChildren(Qt.QListWidget)
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
        logging.debug('mainwindow.py - reset_all_fields - finished')

    def open_file(self):
        logging.debug('mainwindow.py - open_file')
        out_file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self,'Open XML File','','XML Files (*.xml)')
        logging.debug('mainwindow.py - open_file - out_file_name ' + str(out_file_name))
        if out_file_name:
            self.reset_all_fields()
            read_updater_xml(self, out_file_name)
            self.saved = True
            self.make_window_title()
            self.set_modified()

    def make_onsave_msg_box(self, string):
        logging.debug('mainwindow.py - make_onsave_msg_box - string ' + string)
        self.presaveWindow = MyWarning(string, self.config_dict, self.text_translations)
        x1, y1, w1, h1 = self.geometry().getRect()
        _, _, w2, h2 = self.presaveWindow.geometry().getRect()
        x2 = x1 + w1/2 - w2/2
        y2 = y1 + h1/2 - h2/2
        self.presaveWindow.setGeometry(x2, y2, w2, h2)
        self.presaveWindow.setMinimumSize(QtCore.QSize(500, self.presaveWindow.sizeHint().height()))
        self.presaveWindow.setMaximumSize(QtCore.QSize(500, self.presaveWindow.sizeHint().height()))
        self.presaveWindow.exec_()
        try:
            return self.presaveWindow.buttonName
        except AttributeError:
            return None
    
    def tool_button_clicked(self):
        logging.debug('mainwindow.py - tool_button_clicked - self.sender().objectName() ' + self.sender().objectName())
        if "info" in self.sender().objectName():
            info_button(self)
        elif "create" in self.sender().objectName():
            create_backup(self)
        elif "restore" in self.sender().objectName():
            restore_backup(self, self.config_dict['OPTIONS'].getboolean('terminate_processes'),
                                self.config_dict['OPTIONS'].getboolean('relaunch_processes'))
        elif "update" in self.sender().objectName():
            update_prosim(self, self.config_dict['OPTIONS'].getboolean('terminate_processes'),
                                self.config_dict['OPTIONS'].getboolean('relaunch_processes'))
        elif "store" in self.sender().objectName():
            store_update(self)
        elif "changelog" in self.sender().objectName():
            display_changelog(self)
        elif "new" in self.sender().objectName():
            new_path(self)
        elif "cred_delete" in self.sender().objectName():
            del_credentials(self)
        elif "delete_bt" in self.sender().objectName():
            del_path(self)
        elif "credentials" in self.sender().objectName():
            new_credentials(self)
        elif 'none' in self.sender().objectName():
            pass
        else:
            if "_bt_" in self.sender().objectName():
                add_path(self)
    
    def check_prosim737_local_updates(self):
        logging.debug('mainwindow.py - check_prosim737_local_updates')
        self.listWidget.clear()
        self.listWidget.addItem('checking in progress...')
        item = self.listWidget.item(0)
        item.setFlags(QtCore.Qt.NoItemFlags)
        path = self.home_ln_1.text() + '\\'
        file_list = []
        if os.path.isdir(path):
            for name in os.listdir(path):
                if os.path.isfile(os.path.join(path, name)):
                    file_list.append(name)
        else:
            logging.debug('mainwindow.py - check_prosim737_local_updates - no update ; path ' + str(path))
        if file_list:
            file_names = []
            file_names_beta = []
            for filename in file_list:
                if 'ProSim737' in filename and '.zip' in filename:
                    if 'b' in filename:
                        file_names_beta.append(filename)
                    else:
                        file_names.append(filename)      
            self.parse_prosim737_updates(['local', file_names, file_names_beta])
        else:
            self.listWidget.clear()
            self.listWidget.addItem('no update found')
            item = self.listWidget.item(0)
            item.setFlags(QtCore.Qt.NoItemFlags)
            self.listWidget.setEnabled(False)
            self.home_lb_3.setEnabled(False)
        logging.debug('mainwindow.py - check_prosim737_local_updates - len(file_list) ' + str(len(file_list)))
       
    def check_prosim737_online_updates(self):
        logging.debug('mainwindow.py - read_online_prosim_website')
        if self.home_ck_1.isChecked():
            self.listWidget_2.clear()
            self.listWidget_2.addItem('checking in progress...')
            item = self.listWidget_2.item(0)
            item.setFlags(QtCore.Qt.NoItemFlags)
            self.check_prosim737_online = CheckProsim737Online('online')
            self.check_prosim737_online.start()
            self.check_prosim737_online.finished.connect(self.parse_prosim737_updates)
        else:
            self.listWidget_2.clear()
            self.home_lb_4.setEnabled(False)
            self.listWidget_2.setEnabled(False)
        
    def parse_prosim737_updates(self, val):
        logging.debug('mainwindow.py - parse_prosim737_updates')
        if val[0] == 'online':
            widget = self.listWidget_2
            label = self.home_lb_4
        elif val[0] == 'local':
            widget = self.listWidget
            label = self.home_lb_3
        widget.clear()
        if val[1]:
            widget.setEnabled(True)
            label.setEnabled(True)
            widget.addItems(val[1])
        if val[1] and val[2]:
            widget.addItem('------------------------')
            item = widget.findItems('------------------------',Qt.Qt.MatchExactly)[0]
            item.setFlags(QtCore.Qt.NoItemFlags)
        elif not val[1] and not val[2]:
            widget.addItem('no update found')
            item = widget.item(0)
            item.setFlags(QtCore.Qt.NoItemFlags)
            label.setEnabled(False)
            widget.setEnabled(False)
        if val[2]:
            widget.setEnabled(True)
            label.setEnabled(True)
            widget.addItems(val[2])

    def select_list_item(self):
        logging.debug('mainwindow.py - select_list_item')
        if self.sender().objectName() == 'listWidget':
            if self.listWidget.currentItem():
                self.listWidget_2.clearSelection()
                self.update_package_name = self.listWidget.currentItem().text()
                self.update_package_path = self.home_ln_1.text() + '/'
                self.selected_list_widget = 'local'
        elif self.sender().objectName() == 'listWidget_2':
            if self.listWidget_2.currentItem():
                self.listWidget.clearSelection() 
                self.update_package_name = self.listWidget_2.currentItem().text()
                if 'b' in self.update_package_name:
                    self.update_package_path = 'http://download.prosim-ar.com/ProSim737beta/'
                else:
                    self.update_package_path = 'http://prosim-ar.com/download/'
                self.selected_list_widget = 'online'
        logging.debug('mainwindow.py - select_list_item - self.update_package_name ' + self.update_package_name 
                      + ' ; self.selected_list_widget ' + self.selected_list_widget)
    
    def update_backup_buttons_state(self):
        logging.debug('mainwindow.py - update_backup_buttons_state')
        if self.home_ln_2.text():
            if os.path.isdir(self.home_ln_2.text() + '\\'):
                self.home_create_backup.setEnabled(True)
                self.home_restore_backup.setEnabled(True)
            else:
                self.home_create_backup.setEnabled(False)
                self.home_restore_backup.setEnabled(False)
        else:
            self.home_create_backup.setEnabled(False)
            self.home_restore_backup.setEnabled(False)
        logging.debug('mainwindow.py - update_backup_buttons_state - self.home_create_backup.isEnabled() ' 
                      + str(self.home_create_backup.isEnabled()) + ' ; self.home_restore_backup.isEnabled() '
                      + str(self.home_restore_backup.isEnabled()))
            
    def update_store_button_state(self):
        logging.debug('mainwindow.py - update_store_button_state')
        try:
            if self.listWidget_2.currentItem().isSelected():
                if os.path.isdir(self.home_ln_1.text() + '\\'):
                    self.home_store.setEnabled(True)
                else:
                    self.home_store.setEnabled(False)
            else:
                self.home_store.setEnabled(False)
        except AttributeError:
            self.home_store.setEnabled(False)
        logging.debug('mainwindow.py - update_store_button_state - self.home_store.isEnabled() '
                      + str(self.home_store.isEnabled()))
    
    def update_update_button_state(self):
        logging.debug('mainwindow.py - update_update_button_state')
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
        logging.debug('mainwindow.py - update_update_button_state - self.home_update.isEnabled() '
                      + str(self.home_update.isEnabled()) + ' ; right '
                      + str(right) + ' ; left ' + str(left)) 
        
    def check_prosim737updater_update(self):
        logging.debug('mainwindow.py - check_prosim737updater_update')
        if self.config_dict['OPTIONS'].getboolean('check_update'):
            self.check_prosim737updater = CheckProsim737UpdaterOnline()
            self.check_prosim737updater.start()
            self.check_prosim737updater.finished.connect(self.parse_prosim737updater_update)
        else:
            self.actionUpdate.setEnabled(False)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/prosim_update_off_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.actionUpdate.setIcon(icon)
            self.actionUpdate.setToolTip('')
            logging.info('mainwindow.py - check_prosim737updater_update - from options, no update check')
    
    def parse_prosim737updater_update(self, val):
        logging.debug('mainwindow.py - parse_prosim737updater_update - val ' + str(val))
        if val == 'no new version':
            self.actionUpdate.setEnabled(False)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/prosim_update_off_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.actionUpdate.setIcon(icon)
            
            self.text_translations['Path-missing'][self.config_dict['OPTIONS'].get('language')]
            
            self.actionUpdate.setToolTip('No update available !')
        elif 'http' in val:
            self.actionUpdate.setEnabled(True)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/prosim_update_on_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.actionUpdate.setIcon(icon)
            self.actionUpdate.setToolTip('A new update is available for Prosim737 Updater ! Click here to install it automatically.')
            self.link_latest_version = val
              
    def download_and_install_prosim737updater_update(self):
        logging.debug('mainwindow.py - download_and_install_prosim737updater_update - link_latest_version ' + str(self.link_latest_version))
        if self.link_latest_version:
            temp_folder = tempfile.gettempdir()
            self.downloadWindow = MyUpdate(self.link_latest_version, temp_folder)
            self.downloadWindow.label.setText('Downloading ' + self.link_latest_version[self.link_latest_version.rfind('/')+1:] + '...')
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.downloadWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.downloadWindow.setGeometry(x2, y2, w2, h2)
            self.downloadWindow.setMinimumSize(QtCore.QSize(500, self.downloadWindow.sizeHint().height()))
            self.downloadWindow.setMaximumSize(QtCore.QSize(500, self.downloadWindow.sizeHint().height()))
            self.downloadWindow.exec_()
            if not self.downloadWindow.cancel:
                os.startfile(temp_folder + '\\' + self.link_latest_version[self.link_latest_version.rfind('/')+1:])
                time.sleep(0.1)
                self.close()

    def download_prosim737_changelog(self):
        logging.debug('mainwindow.py - download_prosim737_changelog')
        url_name = 'http://download.prosim-ar.com/ProSim737beta/changelog.txt'
        changelog_path = 'documentation\prosim_changelog.txt'
        self.thread = DownloadFile(url_name, self.config_dict, self.text_translations, changelog_path)
        self.thread.download_done.connect(self.activate_changelog_button)
        self.thread.start()
        
    def activate_changelog_button(self):
        logging.debug('mainwindow.py - activate_changelog_button')
        self.home_changelog.setEnabled(True)
        
    def create_language_list(self):
        logging.debug('mainwindow.py - create_language_list')
        value = next(iter(self.text_translations.values()))
        for key, _ in value.items():
            self.language_list[key] = key.title()
            
    def check_language_config(self):
        logging.debug('mainwindow.py - check_language_config')
        language = self.config_dict['OPTIONS'].get('language')
        try:
            self.language_list[language]
        except KeyError:
            logging.exception('mainwindow.py - check_language_config - language ' + str(language) + ' not found.')
            self.config_dict.set('OPTIONS', 'language', 'english')
            infoText = self.text_translations['Language-not-found'][self.config_dict['OPTIONS'].get('language')] % language
            self.infoWindow = MyInfo(infoText, self.config_dict, self.text_translations)
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.infoWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.infoWindow.setGeometry(x2, y2, w2, h2)
            self.infoWindow.setMinimumSize(QtCore.QSize(450, self.infoWindow.sizeHint().height()))
            self.infoWindow.setMaximumSize(QtCore.QSize(450, self.infoWindow.sizeHint().height()))
            self.infoWindow.exec_()
