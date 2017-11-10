import tempfile
import zipfile
import xml.dom.minidom
import logging
import os
import time
from shutil import copyfile, rmtree
from ui.Ui_infowindow import Ui_infoWindow
from ui.Ui_downloadwindow import Ui_downloadWindow
from ui.Ui_unpackwindow import Ui_unpackWindow
from ui.Ui_storewindow import Ui_storeWindow
from ui.Ui_compresswindow import Ui_compressWindow
from ui.Ui_restorewindow import Ui_restoreWindow
from ui.Ui_pathwindow import Ui_pathWindow
from ui.Ui_aboutwindow import Ui_aboutWindow
from ui.Ui_logwindow import Ui_Changelog
from ui.Ui_presavewindow import Ui_presaveWindow
from ui.Ui_optionwindow import Ui_optionWindow
from functions.thread_functions import DownloadFile, UnpackFile, InstallFile, ZipProsim
from functions.thread_functions import CheckProsimPath, CheckProsimProcesses
from functions.utilities import translate_elements
from ui._version import _updater_version, _eclipse_version, _py_version, _qt_version
from PyQt5 import QtWidgets, QtCore, QtGui


class MyInfo(QtWidgets.QDialog, Ui_infoWindow):
    def __init__(self, infoText, config_dict, text_translations):
        logging.debug('window_functions.py - MyInfo - __init__')
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(text_translations['MyInfo'][config_dict['OPTIONS'].get('language')])
        self.iw_label_1.setText(infoText)
        self.iw_okButton.clicked.connect(self.closeWindow)
        
    def closeWindow(self):
        logging.debug('window_functions.py - MyInfo - closeWindow')
        self.close()
        
        
class MyDownload(QtWidgets.QDialog, Ui_downloadWindow):
    def __init__(self, url_name, prosim_path, prosim_credentials, kill, relaunch, config_dict, text_translations):
        logging.debug('window_functions.py - MyDownload - __init__')
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.config_dict = config_dict
        self.text_translations = text_translations
        translate_elements(self, self, self.config_dict['OPTIONS'].get('language'), self.text_translations)
        self.setWindowTitle(self.text_translations['MyDownload'][self.config_dict['OPTIONS'].get('language')])
        self.dw_cancelButton.setEnabled(False)
        self.label.setText('')
        self.url_name = url_name
        self.filename = self.url_name[self.url_name.rfind('/')+1:]
        self.prosim_path = prosim_path
        self.prosim_credentials = prosim_credentials
        self.kill = kill
        self.relaunch = relaunch
        self.relaunch_processes = []
        self.dw_quitButton.clicked.connect(self.close)
        self.dw_downloadButton.clicked.connect(self.check_prosim_path)
        self.cancel = False
    
    def check_prosim_path(self):
        logging.debug('window_functions.py - MyDownload  - check_prosim_path')
        self.label.setText(self.text_translations['Check-path'][self.config_dict['OPTIONS'].get('language')])
        self.dw_quitButton.setEnabled(False)
        self.dw_cancelButton.setEnabled(False)
        self.dw_downloadButton.setEnabled(False)
        self.thread = CheckProsimPath(self.prosim_path)
        self.thread.check_done.connect(self.check_prosim_processes)
        self.thread.start()
    
    def check_prosim_processes(self, val):
        logging.debug('window_functions.py - MyDownload  - check_prosim_processes')
        self.thread.stop()
        if val:
            self.label.setText('')
            self.dw_quitButton.setEnabled(True)
            self.dw_cancelButton.setEnabled(False)
            self.dw_downloadButton.setEnabled(True)
            self.pathWindow = MyPath(val, self.config_dict, self.text_translations, 
                                     self.text_translations['Path-missing'][self.config_dict['OPTIONS'].get('language')])
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.pathWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
            self.pathWindow.exec_()
        else:
            self.label.setText(self.text_translations['Check-process'][self.config_dict['OPTIONS'].get('language')])
            self.dw_quitButton.setEnabled(False)
            self.dw_cancelButton.setEnabled(False)
            self.dw_downloadButton.setEnabled(False)
            self.thread = CheckProsimProcesses(self.prosim_path, self.prosim_credentials, self.kill, self.relaunch)
            #self.thread.check_relaunch.connect(self.prepare_relaunch_processes)
            self.thread.check_done.connect(self.download_update)
            self.thread.check_wrong.connect(self.computer_path_not_match)
            self.thread.start()
        
    '''def prepare_relaunch_processes(self, val):
        logging.debug('window_functions.py - MyDownload  - prepare_relaunch_processes')
        self.relaunch_processes = val'''
    
    def computer_path_not_match(self, val):
        logging.debug('window_functions.py - MyDownload - computer_path_not_match')
        self.label.setText('')
        self.dw_quitButton.setEnabled(True)
        self.dw_cancelButton.setEnabled(False)
        self.dw_downloadButton.setEnabled(True)
        self.thread.stop()
        self.pathWindow = MyPath(val, self.config_dict, self.text_translations, 
                                 self.text_translations['Path-credential-not-match'][self.config_dict['OPTIONS'].get('language')])
        x1, y1, w1, h1 = self.geometry().getRect()
        _, _, w2, h2 = self.pathWindow.geometry().getRect()
        x2 = x1 + w1/2 - w2/2
        y2 = y1 + h1/2 - h2/2
        self.pathWindow.iw_label_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pathWindow.iw_label_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
        self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
        self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
        self.pathWindow.exec_()
    
    def download_update(self, val):
        logging.debug('window_functions.py - MyDownload - download_update')
        if val:
            self.label.setText('')
            self.dw_quitButton.setEnabled(True)
            self.dw_cancelButton.setEnabled(False)
            self.dw_downloadButton.setEnabled(True)
            text = None
            if not ' - ' in val[0]:
                text = self.text_translations['Process-Exception'][self.config_dict['OPTIONS'].get('language')]
            else:
                text = self.text_translations['Process-running'][self.config_dict['OPTIONS'].get('language')]
            self.pathWindow = MyPath(val, self.config_dict, self.text_translations, text)
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.pathWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
            self.pathWindow.exec_()
        else:
            self.dw_cancelButton.clicked.connect(self.cancel_download)
            self.cancel = False
            self.dw_quitButton.setEnabled(False)
            self.dw_cancelButton.setEnabled(True)
            self.dw_downloadButton.setEnabled(False)
            self.label.setText(self.text_translations['Download-light'][self.config_dict['OPTIONS'].get('language')] % self.filename)
            self.thread = DownloadFile(self.url_name, self.config_dict, self.text_translations)
            self.thread.download_update.connect(self.update_progress_bar)
            self.thread.download_done.connect(self.unzip_update)
            self.thread.download_failed.connect(self.download_failed)
            self.thread.start()
    
    def update_progress_bar(self, val):
        if isinstance(val, list):
            self.progressBar.setValue(val[0])
            self.label.setText(val[1])
        else:
            self.progressBar.setValue(val)
    
    def unzip_update(self):
        logging.debug('window_functions.py - MyDownload - unzip_update')
        self.dw_cancelButton.clicked.disconnect(self.cancel_download)
        self.dw_cancelButton.clicked.connect(self.cancel_unzipping)
        self.dw_quitButton.setEnabled(False)
        self.dw_cancelButton.setEnabled(True)
        self.dw_downloadButton.setEnabled(False)
        self.label.setText(self.text_translations['Unpacking-light'][self.config_dict['OPTIONS'].get('language')])
        self.thread.download_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        self.update_progress_bar(0)
        zip_name = tempfile.gettempdir() + '\prosim_update_package.zip'
        unpack_folder = tempfile.gettempdir() + '\prosim_update_package'
        self.thread = UnpackFile(zip_name, unpack_folder, self.config_dict, self.text_translations)
        self.thread.unpack_update.connect(self.update_progress_bar)
        self.thread.unpack_done.connect(self.install_update)
        self.thread.start()
    
    def install_update(self):
        logging.debug('button_functions.py - MyDownload - install_update')
        self.dw_cancelButton.clicked.disconnect(self.cancel_unzipping)
        self.dw_quitButton.setEnabled(False)
        self.dw_cancelButton.setEnabled(False)
        self.dw_downloadButton.setEnabled(False)
        self.thread.unpack_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        self.update_progress_bar(0)
        self.label.setText(self.text_translations['Install-light'][self.config_dict['OPTIONS'].get('language')])
        unpack_folder = tempfile.gettempdir() + '\prosim_update_package\\'
        self.thread = InstallFile(unpack_folder, self.config_dict, self.text_translations, self.prosim_path)
        self.thread.install_update.connect(self.update_progress_bar)
        self.thread.install_done.connect(self.relaunch_prosim_processes)
        self.thread.install_failed.connect(self.install_failed)
        self.thread.start()
        
    def relaunch_prosim_processes(self):
        logging.debug('window_functions.py - MyDownload  - relaunch_processes')
        self.thread.install_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        '''self.label.setText('Launching Prosim737 processes...')
        if self.relaunch_processes:
            for process in self.relaunch_processes:
                index = process.find(' - ')
                computer = process[:index]
                exe_path = process[index +3:]
                if computer == 'local':
                    connection = wmi.WMI()
                    connection.Win32_Process.Create(CommandLine=exe_path, CurrentDirectory=os.path.dirname(exe_path))
                else:
                    username = self.prosim_credentials[computer]['username']
                    password = self.prosim_credentials[computer]['password']
                    connection = wmi.WMI(computer, user=username, password=password)
                    connection.Win32_Process.Create(CommandLine=exe_path, CurrentDirectory=os.path.dirname(exe_path))'''
        self.end_process()

    def end_process(self):
        logging.debug('window_functions.py - MyDownload - end_process')
        self.dw_quitButton.setEnabled(True)
        self.dw_cancelButton.setEnabled(False)
        self.dw_downloadButton.setEnabled(True)
        if not self.cancel:
            self.update_progress_bar([100, 'Job finished !'])
    
    def cancel_download(self):
        logging.debug('window_functions.py - MyDownload - cancel_download')
        self.thread.download_update.disconnect(self.update_progress_bar)
        self.thread.download_done.disconnect(self.unzip_update)
        self.thread.download_failed.disconnect(self.download_failed)
        self.thread.cancel_download()
        self.cancel = True
        self.update_progress_bar([0, self.text_translations['Download-canceled'][self.config_dict['OPTIONS'].get('language')]])
        self.end_process()
        
    def download_failed(self):
        logging.debug('window_functions.py - MyDownload - download_failed')
        self.update_progress_bar([0, self.text_translations['Download-failed'][self.config_dict['OPTIONS'].get('language')]])
        self.cancel = True
        self.end_process()
    
    def cancel_unzipping(self):
        logging.debug('window_functions.py - MyDownload - cancel_unzipping')
        self.thread.unpack_update.disconnect(self.update_progress_bar)
        self.thread.unpack_done.disconnect(self.install_update)
        self.thread.cancel_unzipping()
        self.cancel = True
        self.update_progress_bar([0, self.text_translations['Unpacking-canceled'][self.config_dict['OPTIONS'].get('language')]])
        self.end_process()
    
    def install_failed(self):
        logging.debug('window_functions.py - MyDownload  - install_failed')
        self.thread.install_update.disconnect(self.update_progress_bar)
        self.thread.install_done.disconnect(self.relaunch_prosim_processes)
        self.cancel = True
        self.update_progress_bar([0, self.text_translations['Install-failed'][self.config_dict['OPTIONS'].get('language')]])
        self.end_process()
    
    def closeEvent(self, event):
        logging.debug('window_functions.py - MyDownload - closeEvent')
        try:
            self.thread.terminated = True
            self.thread.exit()
        except AttributeError:
            pass
        try:
            os.remove(tempfile.gettempdir() + '\prosim_update_package.zip')
        except FileNotFoundError:
            pass
        try:
            rmtree(tempfile.gettempdir() + '\prosim_update_package')
        except FileNotFoundError:
            pass


class MyUnpack(QtWidgets.QDialog, Ui_unpackWindow):
    def __init__(self, prosim_path, prosim_credentials, kill, relaunch, config_dict, text_translations):
        logging.debug('window_functions.py - MyUnpack  - __init__')
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.config_dict = config_dict
        self.text_translations = text_translations
        translate_elements(self, self, self.config_dict['OPTIONS'].get('language'), self.text_translations)
        self.setWindowTitle(self.text_translations['MyUnpack'][self.config_dict['OPTIONS'].get('language')])
        self.uw_cancelButton.setEnabled(False)
        self.uw_label_2.setText('')
        self.prosim_path = prosim_path
        self.prosim_credentials = prosim_credentials
        self.kill = kill
        self.relaunch = relaunch
        self.relaunch_processes = []
        self.uw_quitButton.clicked.connect(self.close)
        self.uw_cancelButton.clicked.connect(self.cancel_unzipping)
        self.uw_downloadButton.clicked.connect(self.check_prosim_path)
        self.cancel = False
    
    def update_progress_bar(self, val):
        if isinstance(val, list):
            self.uw_progressBar.setValue(val[0])
            self.uw_label_2.setText(val[1])
        else:
            self.uw_progressBar.setValue(val)
    
    def check_prosim_path(self):
        logging.debug('window_functions.py - MyUnpack  - check_prosim_path')
        self.uw_label_2.setText(self.text_translations['Check-path'][self.config_dict['OPTIONS'].get('language')])
        self.uw_quitButton.setEnabled(False)
        self.uw_cancelButton.setEnabled(False)
        self.uw_downloadButton.setEnabled(False)
        self.thread = CheckProsimPath(self.prosim_path)
        self.thread.check_done.connect(self.check_prosim_processes)
        self.thread.start()
    
    def check_prosim_processes(self, val):
        logging.debug('window_functions.py - MyUnpack  - check_prosim_processes')
        self.thread.stop()
        if val:
            self.uw_label_2.setText('')
            self.uw_quitButton.setEnabled(True)
            self.uw_cancelButton.setEnabled(False)
            self.uw_downloadButton.setEnabled(True)
            self.pathWindow = MyPath(val, self.config_dict, self.text_translations, 
                                     self.text_translations['Path-missing'][self.config_dict['OPTIONS'].get('language')])
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.pathWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
            self.pathWindow.exec_()
        else:
            self.uw_label_2.setText(self.text_translations['Check-process'][self.config_dict['OPTIONS'].get('language')])
            self.uw_quitButton.setEnabled(False)
            self.uw_cancelButton.setEnabled(False)
            self.uw_downloadButton.setEnabled(False)
            self.thread = CheckProsimProcesses(self.prosim_path, self.prosim_credentials, self.kill, self.relaunch)
            #self.thread.check_relaunch.connect(self.prepare_relaunch_processes)
            self.thread.check_done.connect(self.unzip_update)
            self.thread.check_wrong.connect(self.computer_path_not_match)
            self.thread.start()
        
    '''def prepare_relaunch_processes(self, val):
        logging.debug('window_functions.py - MyUnpack  - prepare_relaunch_processes')
        self.relaunch_processes = val'''
    
    def computer_path_not_match(self, val):
        logging.debug('window_functions.py - MyUnpack - computer_path_not_match')
        self.uw_label_2.setText('')
        self.uw_quitButton.setEnabled(True)
        self.uw_cancelButton.setEnabled(False)
        self.uw_downloadButton.setEnabled(True)
        self.thread.stop()
        self.pathWindow = MyPath(val, self.config_dict, self.text_translations, 
                                 self.text_translations['Path-credential-not-match'][self.config_dict['OPTIONS'].get('language')])
        x1, y1, w1, h1 = self.geometry().getRect()
        _, _, w2, h2 = self.pathWindow.geometry().getRect()
        x2 = x1 + w1/2 - w2/2
        y2 = y1 + h1/2 - h2/2
        self.pathWindow.iw_label_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pathWindow.iw_label_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
        self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
        self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
        self.pathWindow.exec_()
    
    def unzip_update(self, val):
        logging.debug('window_functions.py - MyUnpack  - unzip_update')
        if val:
            self.uw_label_2.setText('')
            self.uw_quitButton.setEnabled(True)
            self.uw_cancelButton.setEnabled(False)
            self.uw_downloadButton.setEnabled(True)
            text = None
            if not ' - ' in val[0]:
                text = self.text_translations['Process-Exception'][self.config_dict['OPTIONS'].get('language')]
            else:
                text = self.text_translations['Process-running'][self.config_dict['OPTIONS'].get('language')]
            self.pathWindow = MyPath(val, self.config_dict, self.text_translations, text)
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.pathWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
            self.pathWindow.exec_()
        else:
            self.cancel = False
            self.uw_quitButton.setEnabled(False)
            self.uw_cancelButton.setEnabled(True)
            self.uw_downloadButton.setEnabled(False)
            self.uw_label_2.setText(self.text_translations['Unpacking-light'][self.config_dict['OPTIONS'].get('language')])
            self.update_progress_bar(0)
            zip_name = tempfile.gettempdir() + '\prosim_update_package.zip'
            unpack_folder = tempfile.gettempdir() + '\prosim_update_package'
            self.thread = UnpackFile(zip_name, unpack_folder, self.config_dict, self.text_translations)
            self.thread.unpack_update.connect(self.update_progress_bar)
            self.thread.unpack_done.connect(self.install_update)
            self.thread.start()
    
    def install_update(self):
        logging.debug('window_functions.py - MyUnpack  - install_update')
        self.uw_quitButton.setEnabled(False)
        self.uw_cancelButton.setEnabled(False)
        self.uw_downloadButton.setEnabled(False)
        self.thread.unpack_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        self.update_progress_bar(0)
        self.uw_label_2.setText(self.text_translations['Install-light'][self.config_dict['OPTIONS'].get('language')])
        unpack_folder = tempfile.gettempdir() + '\prosim_update_package\\'
        self.thread = InstallFile(unpack_folder, self.config_dict, self.text_translations, self.prosim_path)
        self.thread.install_update.connect(self.update_progress_bar)
        self.thread.install_done.connect(self.relaunch_prosim_processes)
        self.thread.install_failed.connect(self.install_failed)
        self.thread.start()
    
    def relaunch_prosim_processes(self):
        logging.debug('window_functions.py - MyUnpack  - relaunch_processes')
        self.thread.install_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        '''self.label.setText('Launching Prosim737 processes...')
        if self.relaunch_processes:
            for process in self.relaunch_processes:
                index = process.find(' - ')
                computer = process[:index]
                exe_path = process[index +3:]
                if computer == 'local':
                    connection = wmi.WMI()
                    connection.Win32_Process.Create(CommandLine=exe_path, CurrentDirectory=os.path.dirname(exe_path))
                else:
                    username = self.prosim_credentials[computer]['username']
                    password = self.prosim_credentials[computer]['password']
                    connection = wmi.WMI(computer, user=username, password=password)
                    connection.Win32_Process.Create(CommandLine=exe_path, CurrentDirectory=os.path.dirname(exe_path))'''
        self.end_process()
    
    def end_process(self):
        logging.debug('window_functions.py - MyUnpack  - end_process')
        self.uw_quitButton.setEnabled(True)
        self.uw_cancelButton.setEnabled(False)
        self.uw_downloadButton.setEnabled(True)
        if not self.cancel:
            self.update_progress_bar([100, self.text_translations['Install-finished'][self.config_dict['OPTIONS'].get('language')]])
    
    def cancel_unzipping(self):
        logging.debug('window_functions.py - MyUnpack  - cancel_unzipping')
        self.thread.cancel_unzipping()
        self.cancel = True
        self.update_progress_bar([0, self.text_translations['Unpacking-canceled'][self.config_dict['OPTIONS'].get('language')]])
        self.end_process()
        
    def install_failed(self):
        logging.debug('window_functions.py - MyUnpack  - install_failed')
        self.thread.install_update.disconnect(self.update_progress_bar)
        self.thread.install_done.disconnect(self.relaunch_prosim_processes)
        self.cancel = True
        self.update_progress_bar([0, self.text_translations['Install-failed'][self.config_dict['OPTIONS'].get('language')]])
        self.end_process()
    
    def closeEvent(self, event):
        logging.debug('window_functions.py - MyUnpack  - closeEvent')
        try:
            self.thread.terminated = True
            self.thread.exit()
        except AttributeError:
            pass
        try:
            os.remove(tempfile.gettempdir() + '\prosim_update_package.zip')
        except FileNotFoundError:
            pass
        try:
            rmtree(tempfile.gettempdir() + '\prosim_update_package')
        except FileNotFoundError:
            pass


class MyStore(QtWidgets.QDialog, Ui_storeWindow):
    def __init__(self, url_name, update_file, config_dict, text_translations):
        logging.debug('window_functions.py - MyStore - __init__')
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.config_dict = config_dict
        self.text_translations = text_translations
        translate_elements(self, self, self.config_dict['OPTIONS'].get('language'), self.text_translations)
        self.setWindowTitle(self.text_translations['MyStore'][self.config_dict['OPTIONS'].get('language')])
        self.update_file = update_file
        self.url_name = url_name
        self.sw_button.clicked.connect(self.cancel_download)
        self.cancel = False
        self.download_update()
    
    def update_progress_bar(self, val):
        if isinstance(val, list):
            self.progressBar.setValue(val[0])
            self.sw_label.setText(val[1])
        else:
            self.progressBar.setValue(val)
    
    def download_update(self):
        logging.debug('window_functions.py - MyStore - download_update')
        self.thread = DownloadFile(self.url_name, self.config_dict, self.text_translations, self.update_file)
        self.thread.download_update.connect(self.update_progress_bar)
        self.thread.download_done.connect(self.close)
        self.thread.download_failed.connect(self.download_failed)
        self.thread.start()
    
    def cancel_download(self):
        logging.debug('window_functions.py - MyStore - cancel_download')
        self.thread.cancel_download()
        self.cancel = True
        time.sleep(0.25)
        self.close()
        
    def download_failed(self):
        logging.debug('window_functions.py - MyStore - download_failed')
        self.update_progress_bar(0)
        self.sw_label.setText(self.text_translations['Download-failed'][self.config_dict['OPTIONS'].get('language')])
        self.cancel = True
        self.button.setText(self.text_translations['Download-failed-label'][self.config_dict['OPTIONS'].get('language')])
        
    def closeEvent(self, event):
        logging.debug('window_functions.py - MyStore - closeEvent')
        self.thread.download_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        if self.cancel:
            os.remove(self.update_file)
        
        
class MyCompress(QtWidgets.QDialog, Ui_compressWindow):
    def __init__(self, backup_directory, prosim_path, credentials, config_dict, text_translations):
        logging.debug('window_functions.py - MyCompress - __init__')
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.config_dict = config_dict
        self.text_translations = text_translations
        self.setWindowTitle(self.text_translations['MyCompress'][self.config_dict['OPTIONS'].get('language')])
        self.backup_directory = backup_directory
        self.prosim_path = prosim_path
        self.credentials = credentials
        self.check_prosim_path()
        
    def check_prosim_path(self):
        logging.debug('window_functions.py - MyCompress  - check_prosim_path')
        self.label.setText(self.text_translations['Check-path'][self.config_dict['OPTIONS'].get('language')])
        self.thread = CheckProsimPath(self.prosim_path)
        self.thread.check_done.connect(self.compress_directories)
        self.thread.start()
    
    def update_progress_bar(self, val):
        if isinstance(val, list):
            self.progressBar.setValue(val[0])
            self.label.setText(val[1])
        else:
            self.progressBar.setValue(val)
    
    def compress_directories(self, val):
        logging.debug('window_functions.py - MyCompress - compress directories')
        if val:
            self.label.setText('')
            self.pathWindow = MyPath(val, self.config_dict, self.text_translations, 
                                     self.text_translations['Path-missing'][self.config_dict['OPTIONS'].get('language')])
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.pathWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
            self.pathWindow.exec_()
            self.close()
        else:
            self.thread = ZipProsim(self.backup_directory, self.prosim_path, self.credentials, self.config_dict, self.text_translations)
            self.thread.zip_update.connect(self.update_progress_bar)
            self.thread.zip_done.connect(self.closeWindow)
            self.thread.start()

    def closeWindow(self):
        logging.debug('window_functions.py - MyStore - closeWindow')
        self.thread.zip_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        self.close()


class MyRestore(QtWidgets.QDialog, Ui_restoreWindow):
    def __init__(self, backup_folder, kill, relaunch, config_dict, text_translations):
        logging.debug('window_functions.py - MyRestore - __init__')
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.text_translations = text_translations
        self.config_dict = config_dict
        translate_elements(self, self, self.config_dict['OPTIONS'].get('language'), self.text_translations)
        self.setWindowTitle(text_translations['MyRestore'][config_dict['OPTIONS'].get('language')])
        self.label.setText('')
        self.backup_folder = backup_folder
        self.prosim_credentials = {}
        self.kill = kill
        self.relaunch = relaunch
        self.cancel = False
        self.rw_cancelButton.clicked.connect(self.close)
        self.rw_restoreButton.clicked.connect(self.check_prosim_path)
        self.rw_deleteButton.clicked.connect(self.delete_backup)
        self.rw_restoreButton.setEnabled(False)
        self.rw_deleteButton.setEnabled(False)
        self.progressBar.setEnabled(False)
        self.progressBar.setVisible(False)
        self.listWidget.itemClicked.connect(self.select_list_item)
        self.listWidget.itemDoubleClicked.connect(self.show_backup_information)
        self.list_backups()
        
    def update_progress_bar(self, val):
        if isinstance(val, list):
            self.progressBar.setValue(val[0])
            self.label.setText(val[1])
        else:
            self.progressBar.setValue(val)
    
    def list_backups(self):
        logging.debug('window_functions.py - MyRestore - list backups')
        file_list = []
        try:
            for name in os.listdir(self.backup_folder):
                if os.path.isfile(os.path.join(self.backup_folder, name)):
                    file_list.append(name)
        except Exception:
            logging.exception('window_functions.py - MyRestore - list_backups - ' + str(Exception))
        if file_list:
            for file_name in file_list:
                if 'Prosim737_backup_' in file_name and '.zip' in file_name:
                    self.listWidget.addItem(str(file_name))
    
    def select_list_item(self):
        logging.debug('window_functions.py - MyRestore - select_list_item')
        self.rw_restoreButton.setEnabled(True)
        self.rw_deleteButton.setEnabled(True)
    
    def show_backup_information(self, val):
        logging.debug('window_functions.py - MyRestore - show_backup_information - val ' + str(val.objectName()))
        xml_file = zipfile.ZipFile(self.backup_folder + '\\' + val.text()).read('backup_options.xml')
        backup_folders = self.read_backup_xml(xml_file)
        infoText = self.text_translations['Restore-info'][self.config_dict['OPTIONS'].get('language')]
        infoText += '<ul>'
        text_len = 0
        for key, val in backup_folders.items():
            tmp = '<li>' + key + '.zip -> ' + val + '</li>'
            if len(tmp) > text_len:
                text_len = len(tmp)
            infoText += tmp
        if text_len < 45:
            text_len = 45
        infoText += '</ul>'
        self.infoWindow = MyInfo(infoText, self.config_dict, self.text_translations)
        x1, y1, w1, h1 = self.geometry().getRect()
        _, _, w2, h2 = self.infoWindow.geometry().getRect()
        x2 = x1 + w1/2 - w2/2
        y2 = y1 + h1/2 - h2/2
        self.infoWindow.setGeometry(x2, y2, w2, h2)
        self.infoWindow.setMinimumSize(QtCore.QSize(text_len * 10, len(backup_folders) * 27 + 3 * 27))
        self.infoWindow.setMaximumSize(QtCore.QSize(text_len * 10, len(backup_folders) * 27 + 3 * 27))
        self.infoWindow.exec_()
    
    def delete_backup(self):
        file_name = self.listWidget.currentItem().text()
        logging.debug('window_functions.py - MyRestore - delete backup - file_name' + str(file_name))
        os.remove(self.backup_folder + '\\' + file_name)
        self.listWidget.clear()
        self.list_backups()
        self.rw_restoreButton.setEnabled(False)
        self.rw_deleteButton.setEnabled(False)
    
    def check_prosim_path(self):
        logging.debug('window_functions.py - MyRestore - check_prosim_path')
        self.rw_cancelButton.setText(self.text_translations['Restore-cancel-button'][self.config_dict['OPTIONS'].get('language')])
        self.label.setText(self.text_translations['Check-path'][self.config_dict['OPTIONS'].get('language')])
        self.rw_restoreButton.setEnabled(False)
        self.rw_deleteButton.setEnabled(False)
        self.rw_cancelButton.setEnabled(False)
        xml_file = zipfile.ZipFile(self.backup_folder + '\\' + self.listWidget.currentItem().text()).read('backup_options.xml')
        self.backup_folders = self.read_backup_xml(xml_file)
        self.thread = CheckProsimPath(self.backup_folders)
        self.thread.check_done.connect(self.check_prosim_processes)
        self.thread.start()
    
    def check_prosim_processes(self, val):
        logging.debug('window_functions.py - MyRestore - check_prosim_processes')
        self.thread.stop()
        if val:
            self.label.setText('')
            self.rw_restoreButton.setEnabled(True)
            self.rw_deleteButton.setEnabled(True)
            self.rw_cancelButton.setEnabled(True)
            self.rw_cancelButton.setText(self.text_translations['Restore-quit-button'][self.config_dict['OPTIONS'].get('language')])
            self.pathWindow = MyPath(val, self.text_translations['Path-missing'][self.config_dict['OPTIONS'].get('language')])
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.pathWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.pathWindow.iw_label_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
            self.pathWindow.iw_label_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
            self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
            self.pathWindow.exec_()
        else:
            self.label.setText(self.text_translations['Check-process'][self.config_dict['OPTIONS'].get('language')])
            self.rw_restoreButton.setEnabled(False)
            self.rw_deleteButton.setEnabled(False)
            self.rw_cancelButton.setEnabled(False)
            self.thread = CheckProsimProcesses(self.backup_folders, self.prosim_credentials, self.kill, self.relaunch)
            #self.thread.check_relaunch.connect(self.prepare_relaunch_processes)
            self.thread.check_done.connect(self.restore_backup)
            self.thread.check_wrong.connect(self.computer_path_not_match)
            self.thread.start()
        
    '''def prepare_relaunch_processes(self, val):
        logging.debug('window_functions.py - MyRestore - prepare_relaunch_processes')
        self.relaunch_processes = val'''
    
    def computer_path_not_match(self, val):
        logging.debug('window_functions.py - MyRestore - computer_path_not_match')
        self.label.setText('')
        self.rw_restoreButton.setEnabled(True)
        self.rw_deleteButton.setEnabled(True)
        self.rw_cancelButton.setEnabled(True)
        self.rw_cancelButton.setText(self.text_translations['Restore-quit-button'][self.config_dict['OPTIONS'].get('language')])
        self.thread.stop()
        self.pathWindow = MyPath(val, self.text_translations['Path-credential-not-match'][self.config_dict['OPTIONS'].get('language')])
        x1, y1, w1, h1 = self.geometry().getRect()
        _, _, w2, h2 = self.pathWindow.geometry().getRect()
        x2 = x1 + w1/2 - w2/2
        y2 = y1 + h1/2 - h2/2
        self.pathWindow.iw_label_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pathWindow.iw_label_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
        self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
        self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
        self.pathWindow.exec_()
    
    def restore_backup(self, val):
        logging.debug('window_functions.py - MyRestore - restore backup')
        if val:
            self.label.setText('')
            self.rw_restoreButton.setEnabled(True)
            self.rw_deleteButton.setEnabled(True)
            self.rw_cancelButton.setEnabled(True)
            self.rw_cancelButton.setText(self.text_translations['Restore-quit-button'][self.config_dict['OPTIONS'].get('language')])
            self.pathWindow = MyPath(val, self.text_translations['Process-running'][self.config_dict['OPTIONS'].get('language')])
            x1, y1, w1, h1 = self.geometry().getRect()
            _, _, w2, h2 = self.pathWindow.geometry().getRect()
            x2 = x1 + w1/2 - w2/2
            y2 = y1 + h1/2 - h2/2
            self.pathWindow.setMinimumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setMaximumSize(QtCore.QSize(600, self.pathWindow.sizeHint().height()))
            self.pathWindow.setGeometry(x2, y2, 600, self.pathWindow.sizeHint().height())
            self.pathWindow.exec_()
        else:
            self.rw_cancelButton.clicked.disconnect(self.close)
            self.rw_cancelButton.clicked.connect(self.cancel_unzipping)
            self.rw_restoreButton.setEnabled(False)
            self.rw_deleteButton.setEnabled(False)
            self.rw_cancelButton.setEnabled(True)
            self.label.setText(self.text_translations['Unpacking-light'][self.config_dict['OPTIONS'].get('language')])
            self.progressBar.setEnabled(True)
            self.progressBar.setVisible(True)
            temp_path = tempfile.gettempdir()
            copyfile(self.backup_folder + '\\' + self.listWidget.currentItem().text(), temp_path + '\prosim_update_package.zip')
            unpack_folder = temp_path + '\prosim_update_package'
            self.thread = UnpackFile(temp_path + '\prosim_update_package.zip', unpack_folder, self.config_dict, self.text_translations, True)
            self.thread.unpack_update.connect(self.update_progress_bar)
            self.thread.unpack_done.connect(self.install_backup)
            self.thread.start()
    
    def install_backup(self):
        logging.debug('window_functions.py - MyRestore - install_backup')
        self.rw_restoreButton.setEnabled(False)
        self.rw_deleteButton.setEnabled(False)
        self.rw_cancelButton.setEnabled(False)
        self.thread.unpack_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        self.update_progress_bar(0)
        self.label.setText(self.text_translations['Install-light'][self.config_dict['OPTIONS'].get('language')])
        unpack_folder = tempfile.gettempdir() + '\prosim_update_package\\'
        self.thread = InstallFile(unpack_folder, self.config_dict, self.text_translations, self.backup_folders, backup=True)
        self.thread.install_update.connect(self.update_progress_bar)
        self.thread.install_done.connect(self.relaunch_prosim_processes)
        self.thread.install_failed.connect(self.install_failed)
        self.thread.start()

    def relaunch_prosim_processes(self):
        logging.debug('window_functions.py - MyRestore  - relaunch_processes')
        self.thread.install_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        '''self.label.setText('Launching Prosim737 processes...')
        if self.relaunch_processes:
            for process in self.relaunch_processes:
                index = process.find(' - ')
                computer = process[:index]
                exe_path = process[index +3:]
                if computer == 'local':
                    connection = wmi.WMI()
                    connection.Win32_Process.Create(CommandLine=exe_path, CurrentDirectory=os.path.dirname(exe_path))
                else:
                    username = self.prosim_credentials[computer]['username']
                    password = self.prosim_credentials[computer]['password']
                    connection = wmi.WMI(computer, user=username, password=password)
                    connection.Win32_Process.Create(CommandLine=exe_path, CurrentDirectory=os.path.dirname(exe_path))'''
        self.end_process()

    def end_process(self):
        logging.debug('window_functions.py - MyRestore - end_process')
        self.rw_cancelButton.clicked.connect(self.close)
        self.rw_cancelButton.clicked.disconnect(self.cancel_unzipping)
        self.rw_cancelButton.setText(self.text_translations['Restore-quit-button'][self.config_dict['OPTIONS'].get('language')])
        self.rw_restoreButton.setEnabled(True)
        self.rw_deleteButton.setEnabled(True)
        self.rw_cancelButton.setEnabled(True)
        if not self.cancel:
            self.update_progress_bar([100, self.text_translations['Install-finished'][self.config_dict['OPTIONS'].get('language')]])
    
    def cancel_unzipping(self):
        logging.debug('window_functions.py - MyRestore  - cancel_unzipping')
        self.thread.cancel_unzipping()
        self.cancel = True
        self.update_progress_bar([0, self.text_translations['Unpacking-canceled'][self.config_dict['OPTIONS'].get('language')]])
        self.end_process()
    
    def install_failed(self):
        logging.debug('window_functions.py - MyRestore  - install_failed')
        self.thread.install_update.disconnect(self.update_progress_bar)
        self.thread.install_done.disconnect(self.relaunch_prosim_processes)
        self.cancel = True
        self.update_progress_bar([0, self.text_translations['Install-failed'][self.config_dict['OPTIONS'].get('language')]])
        self.end_process()
    
    def read_backup_xml(self, xml_file):
        logging.debug('window_functions.py - MyRestore - read_backup_xml')
        path_dict = {}
        doc = xml.dom.minidom.parseString(str(xml_file,'utf-8'))
        backup_element = self.get_element(doc, 'BackupInstance')
        for element in backup_element:
            prosim_folder = self.get_element_value(element, 'BackupFile')[:-4]
            target_folder = self.get_element_value(element, 'BackupPath')
            path_dict[prosim_folder] = target_folder
        credential_element = self.get_element(doc, 'CredentialInstance')
        for element in credential_element:
            computer = self.get_element_value(element, 'CredentialComputer')
            username = self.get_element_value(element, 'CredentialUsername')
            password = self.get_element_value(element, 'CredentialPassword')
            self.prosim_credentials[computer] = {'username': username, 'password': password}
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
    
    def closeEvent(self, event):
        logging.debug('window_functions.py - MyRestore - closeEvent')
        try:
            self.thread.terminated = True
            self.thread.exit()
        except AttributeError:
            pass
        try:
            os.remove(tempfile.gettempdir() + '\prosim_update_package.zip')
        except FileNotFoundError:
            pass
        try:
            rmtree(tempfile.gettempdir() + '\prosim_update_package')
        except FileNotFoundError:
            pass


class MyPath(QtWidgets.QDialog, Ui_pathWindow):
    def __init__(self, wrong_path, config_dict, text_translations, text=None):
        logging.debug('window_functions.py - MyPath - __init__')
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(text_translations['MyPath'][config_dict['OPTIONS'].get('language')])
        self.wrong_path = wrong_path
        self.iw_okButton.clicked.connect(self.closeWindow)
        if text:
            self.iw_label_1.setText(text[0])
            self.iw_label_3.setText(text[1])
        self.add_path_ui()
    
    def add_path_ui(self):
        logging.debug('window_functions.py - MyPath - add_path_ui')
        font = QtGui.QFont()
        font.setFamily("fonts/SourceSansPro-Regular.ttf")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        for path in self.wrong_path:
            if len(path) > 55:
                path = path[:20] + ' ... ' + path[-30:]
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
        logging.debug('window_functions.py - MyPath - closeWindow')
        self.close()


class MyUpdate(QtWidgets.QDialog, Ui_storeWindow):
    def __init__(self, url, folder, config_dict, text_translations):
        logging.debug('window_functions.py - MyStore - __init__')
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.config_dict = config_dict
        self.text_translations = text_translations
        translate_elements(self, self, self.config_dict['OPTIONS'].get('language'), self.text_translations)
        self.setWindowTitle(self.text_translations['MyStore'][self.config_dict.get('OPTIONS', 'language')])
        self.temp_folder = folder
        self.url = url
        self.update_file = self.temp_folder + '\\' + self.url[self.url.rfind('/')+1:]
        self.button.clicked.connect(self.cancel_download)
        self.cancel = False
        self.download_update()
    
    def update_progress_bar(self, val):
        if isinstance(val, list):
            self.progressBar.setValue(val[0])
            self.label.setText(val[1])
        else:
            self.progressBar.setValue(val)
    
    def download_update(self):
        logging.debug('window_functions.py - MyStore - download_update')
        self.thread = DownloadFile(self.url, self.update_file)
        self.thread.download_update.connect(self.update_progress_bar)
        self.thread.download_done.connect(self.close)
        self.thrad.download_failed(self.download_failed)
        self.thread.start()
    
    def cancel_download(self):
        logging.debug('window_functions.py - MyStore - cancel_download')
        self.thread.cancel_download()
        self.cancel = True
        time.sleep(0.25)
        self.close()
        
    def download_failed(self):
        logging.debug('window_functions.py - MyStore - download_failed')
        self.update_progress_bar(0)
        self.label.setText(self.text_translations['Download-failed'][self.config_dict.get('OPTIONS', 'language')])
        self.cancel_download()
        
    def closeEvent(self, event):
        logging.debug('window_functions.py - MyStore - closeEvent')
        self.thread.download_update.disconnect(self.update_progress_bar)
        self.thread.stop()
        if self.cancel:
            os.remove(self.update_file)


class MyAbout(QtWidgets.QDialog, Ui_aboutWindow):
    def __init__(self, config_dict, translations):
        logging.debug('window_functions.py - MyAbout - __init__')
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(translations['MyAbout'][config_dict.get('OPTIONS', 'language')])
        about_text = translations[self.aw_label_1.objectName()][config_dict.get('OPTIONS', 'language')] % (_updater_version, _eclipse_version, _py_version, _qt_version)
        self.aw_label_1.setText(about_text)
        self.aw_okButton.clicked.connect(self.closeWindow)

    def closeWindow(self):
        logging.debug('window_functions.py - MyAbout - closeWindow')
        self.close()
        
        
class MyLog(QtWidgets.QDialog, Ui_Changelog):
    def __init__(self):
        logging.debug('window_functions.py - MyLog - __init__')
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.lg_txBrower.setPlainText(open("documentation/changelog.txt").read())
        self.lg_okButton.clicked.connect(self.closeWindow)
        
    def closeWindow(self):
        logging.debug('window_functions.py - MyLog - closeWindow')
        self.close()
        
        
class MyWarning(QtWidgets.QDialog, Ui_presaveWindow):
    def __init__(self, string, config_dict, text_translations):
        logging.debug('window_functions.py - MyWarning - __init__')
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        translate_elements(self, self, config_dict['OPTIONS'].get('language'), text_translations)
        self.setWindowTitle(text_translations['MyWarning'][config_dict['OPTIONS'].get('language')])
        self.iw_cancelButton.setFocus(True)
        all_buttons = self.findChildren(QtWidgets.QToolButton)
        for widget in all_buttons:
            widget.clicked.connect(self.closeWindow)
        self.iw_nosaveButton.setText(text_translations['iw_nosaveButton'][config_dict['OPTIONS'].get('language')] % string)

    def closeWindow(self):
        logging.debug('window_functions.py - MyWarning - closeWindow - self.sender().objectName() ' + self.sender().objectName())
        self.buttonName = self.sender().objectName()
        self.close()


class MyOptions(QtWidgets.QDialog, Ui_optionWindow):
    def __init__(self, config_dict, text_translations, language_list):
        logging.debug('window_functions.py - MyOptions - __init__')
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.config_dict = config_dict
        self.text_translations = text_translations
        translate_elements(self, self, self.config_dict['OPTIONS'].get('language'), self.text_translations)
        self.setWindowTitle(text_translations['MyOptions'][config_dict['OPTIONS'].get('language')])
        itemDelegate = QtWidgets.QStyledItemDelegate()
        self.ow_comboBox_1.setItemDelegate(itemDelegate)
        self.ow_comboBox_2.setItemDelegate(itemDelegate)
        self.language_list = language_list
        self.ow_okButton.clicked.connect(self.save_and_close)
        self.ow_cancelButton.clicked.connect(self.close_window)
        #self.ow_checkBox_2.stateChanged.connect(self.activate_checkbox)
        self.ow_openButton_1.clicked.connect(self.get_directory)
        self.ow_infoButton_1.clicked.connect(self.info_button)
        self.ow_infoButton_2.clicked.connect(self.info_button)
        self.ow_infoButton_3.clicked.connect(self.info_button)
        self.ow_infoButton_4.clicked.connect(self.info_button)
        self.ow_infoButton_5.clicked.connect(self.info_button)
        self.cancel = True
        self.populate_language_combobox()
        self.read_config_dict()
    
    def populate_language_combobox(self):
        language_list = []
        for _, value in self.language_list.items():
            language_list.append(value)
        language_list = sorted(language_list)
        self.ow_comboBox_2.addItems(language_list)
    
    def read_config_dict(self):
        logging.debug('window_functions.py - MyOptions - read_config_dict')
        log_level = self.config_dict.get('LOG', 'level')
        log_path = self.config_dict.get('LOG', 'path')
        language = self.config_dict.get('OPTIONS', 'language')
        check_update = self.config_dict['OPTIONS'].getboolean('check_update')
        terminate_processes = self.config_dict['OPTIONS'].getboolean('terminate_processes')
        relaunch_processes = self.config_dict['OPTIONS'].getboolean('relaunch_processes')
        self.ow_comboBox_2.setCurrentIndex(self.ow_comboBox_2.findText(self.language_list[language]))
        self.ow_comboBox_1.setCurrentIndex(self.ow_comboBox_1.findText(log_level))
        self.ow_lineEdit.setText(log_path)
        self.ow_checkBox_1.setChecked(check_update)
        self.ow_checkBox_2.setChecked(terminate_processes)
        self.ow_checkBox_3.setChecked(relaunch_processes)
    
    def get_directory(self):
        logging.debug('window_functions.py - MyOptions - get_directory invoked')
        file_dialog = QtWidgets.QFileDialog()
        out_dir = file_dialog.getExistingDirectory(self, "Select Directory")
        self.ow_lineEdit.setText(str(out_dir.replace('/','\\')))
        logging.debug('window_functions.py - MyOptions - get_directory: ' + str(out_dir))
    
    def activate_checkbox(self):
        logging.debug('window_functions.py - MyOptions - activate_checkbox')
        if self.ow_checkBox_2.isChecked():
            self.ow_checkBox_3.setEnabled(True)
        else:
            self.ow_checkBox_3.setEnabled(False)
            self.ow_checkBox_3.setChecked(False)
    
    def save_and_close(self):
        logging.debug('window_functions.py - MyOptions - save_and_close')
        self.cancel = False
        language = ''
        for key, value in self.language_list.items():
            if value == self.ow_comboBox_2.currentText():
                language = key
        self.config_dict.set('LOG', 'level', str(self.ow_comboBox_1.currentText()))
        self.config_dict.set('LOG', 'path', str(self.ow_lineEdit.text()))
        self.config_dict.set('OPTIONS', 'language', language)
        self.config_dict.set('OPTIONS', 'check_update', str(self.ow_checkBox_1.isChecked()))
        self.config_dict.set('OPTIONS', 'terminate_processes', str(self.ow_checkBox_2.isChecked()))
        self.config_dict.set('OPTIONS', 'relaunch_processes', str(self.ow_checkBox_3.isChecked()))
        self.close_window()
    
    def info_button(self):
        logging.debug('window_functions.py - MyOptions - info_button - self.sender().objectName() ' + self.sender().objectName())
        infoText = self.text_translations[self.sender().objectName()][self.config_dict['OPTIONS'].get('language')]
        x = QtGui.QCursor.pos().x()
        y = QtGui.QCursor.pos().y()
        x = x - 175
        y = y + 50
        self.infoWindow = MyInfo(infoText, self.config_dict, self.text_translations)
        self.infoWindow.setMinimumSize(QtCore.QSize(450, self.infoWindow.sizeHint().height()))
        self.infoWindow.setMaximumSize(QtCore.QSize(450, self.infoWindow.sizeHint().height()))
        self.infoWindow.setGeometry(x, y, 450, self.infoWindow.sizeHint().height())
        self.infoWindow.exec_()
    
    def close_window(self):
        logging.debug('window_functions.py - MyOptions - closeWindow')
        self.close()
