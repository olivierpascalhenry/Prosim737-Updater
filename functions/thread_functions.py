import tempfile
import zipfile
import xml.dom.minidom
import logging
import os
import time
import requests
import wmi
import pythoncom
from shutil import copy, rmtree
from PyQt5 import QtCore, Qt
from bs4 import BeautifulSoup
from distutils.version import LooseVersion
from natsort import natsorted
from ui._version import _updater_version
from urllib.request import urlopen
from hurry.filesize import size, alternative  # @UnresolvedImport

        
class DownloadFile(Qt.QThread):
    download_update = QtCore.pyqtSignal(list)
    download_done = QtCore.pyqtSignal()
    download_failed = QtCore.pyqtSignal()
    def __init__(self, url_name, config_dict, translations, update_file=None):
        Qt.QThread.__init__(self)
        logging.debug('thread_functions.py - DownloadFile - __init__ - url_name ' + str(url_name)
                      + ' ; update_file ' + str(update_file))
        self.url_name = url_name
        self.update_file = update_file
        self.config_dict = config_dict
        self.translations = translations
        self.cancel = False
        
    def run(self):
        logging.debug('thread_functions.py - DownloadFile - run - download started')
        if not self.update_file:
            self.update_file = tempfile.gettempdir() + '\prosim_update_package.zip'
        text_light = self.translations['Download-light'][self.config_dict['OPTIONS'].get('language')]
        text_complete = self.translations['Download-complete'][self.config_dict['OPTIONS'].get('language')]
        self.download_update.emit([0, text_light % self.url_name[self.url_name.rfind("/")+1:]])
        opened_file = open(self.update_file, 'wb')
        try:
            opened_url = urlopen(self.url_name, timeout=10)
            totalFileSize = int(opened_url.info()['Content-Length'])
            bufferSize = 9192
            fileSize = 0
            start = time.clock()
            while True:
                if self.cancel:
                    opened_file.close()
                    break
                buffer = opened_url.read(bufferSize)
                if not buffer:
                    break
                fileSize += len(buffer)
                opened_file.write(buffer)
                download_speed = size(fileSize/(time.clock() - start), system=alternative) + '/s'
                self.download_update.emit([round(fileSize * 100 / totalFileSize), text_complete % (self.url_name[self.url_name.rfind("/")+1:], download_speed)])
            opened_file.close()
            if not self.cancel:
                logging.debug('thread_functions.py - DownloadFile - run - download finished')
                self.download_done.emit()
            else:
                logging.debug('thread_functions.py - DownloadFile - run - download canceled')
        except Exception:
            logging.exception('thread_functions.py - DownloadFile - run - connexion issue ; self.url_name ' + self.url_name)
            opened_file.close()
            self.download_failed.emit()
            
    
    def cancel_download(self):
        logging.debug('thread_functions.py - DownloadFile - cancel_download')
        self.cancel = True
    
    def stop(self):
        logging.debug('thread_functions.py - DownloadFile - stop')
        self.terminate()


class UnpackFile(Qt.QThread):
    unpack_update = QtCore.pyqtSignal(list)
    unpack_done = QtCore.pyqtSignal()
    def __init__(self, in_file, target_name, config_dict, text_translations, backup=False):
        logging.debug('thread_functions.py - UnpackFile - __init__ - in_file ' + str(in_file) + ' ; target_name '
                      + str(target_name) + ' ; backup ' + str(backup))
        Qt.QThread.__init__(self)
        self.backup = backup
        self.in_file = in_file
        self.target_name = target_name
        self.config_dict = config_dict
        self.text_translations = text_translations
        self.prosim_list = ['ProSim737', 'ProSimAudio', 'ProSimCDU',
                            'ProSimDisplay', 'ProSimMCP', 'ProSimPanel']
        self.cancel = False
        
    def run(self):
        logging.debug('thread_functions.py - UnpackFile - run')
        self.unpack(self.in_file, self.target_name)
        if self.backup:
            file_list = []
            try:
                for name in os.listdir(self.target_name + '\\'):
                    if os.path.isfile(os.path.join(self.target_name, name)):
                        file_list.append(name)
            except Exception:
                logging.exception('thread_functions.py - UnpackFile - run')
            if file_list:
                for file_name in file_list:
                    if self.cancel:
                        break
                    if '.zip' in file_name:
                        self.unpack(self.target_name + '\\' + file_name, self.target_name + '\\' + file_name[:-4])
        else:
            for folder in self.prosim_list:
                if self.cancel:
                    break
                file_in = self.target_name + '\\' + folder + '.zip'
                self.unpack(file_in, self.target_name)
        if not self.cancel:
            self.unpack_done.emit()
        
    def unpack(self, in_file, target_name):
        logging.debug('thread_functions.py - UnpackFile - unpack - started')
        self.unpack_update.emit([0, self.text_translations['Unpacking-complete'][self.config_dict['OPTIONS'].get('language')] % os.path.basename(in_file)])
        zf = zipfile.ZipFile(in_file, 'r')
        uncompress_size = sum((file.file_size for file in zf.infolist()))
        extracted_size = 0
        for file in zf.infolist():
            if self.cancel:
                zf.close()
                break
            extracted_size += file.file_size
            percentage = round(extracted_size * 100/uncompress_size)
            if self.backup:
                folder = os.path.basename(os.path.normpath(target_name))
            else:
                folder = file.filename[:file.filename.find('/')]
            self.unpack_update.emit([percentage, self.text_translations['Unpacking-complete'][self.config_dict['OPTIONS'].get('language')] % folder])
            zf.extract(file, target_name)
        logging.debug('thread_functions.py - UnpackFile - unpack - finished')
    
    def cancel_unzipping(self):
        logging.debug('thread_functions.py - UnpackFile - cancel_download')
        self.cancel = True
    
    def stop(self):
        logging.debug('thread_functions.py - UnpackFile - unpack - stop')
        self.terminate()


class InstallFile(Qt.QThread):
    install_update = QtCore.pyqtSignal(list)
    install_done = QtCore.pyqtSignal()
    install_failed = QtCore.pyqtSignal()
    def __init__(self, directory, config_dict, text_translations, prosim_path=None, backup=False):
        logging.debug('thread_functions.py - InstallFile - __init__ - directory ' + str(directory) + ' ; prosim_path '
                      + str(prosim_path) + ' ; backup ' + str(backup))
        Qt.QThread.__init__(self)
        self.backup = backup
        self.directory = directory
        self.prosim_path = prosim_path
        self.config_dict = config_dict
        self.text_translations = text_translations

    def run(self):
        logging.debug('thread_functions.py - InstallFile - run')
        if self.backup:
            prosim_directories = self.prosim_path
            for key in prosim_directories:
                prosim_folder = self.directory + '\\' + key
                num_files = self.count_files(prosim_folder)
                try:
                    num_copied = 0
                    text = self.text_translations['Restore-complete'][self.config_dict['OPTIONS'].get('language')]
                    for path, _, filenames in os.walk(prosim_folder):
                        percentage = int(round((num_copied/float(num_files))*100))
                        self.install_update.emit([percentage, text % str(key)])
                        for file in filenames:
                            source_file = os.path.join(path, file)
                            destFile = os.path.join(path.replace(prosim_folder, prosim_directories[key]), file)
                            if not os.path.isdir(os.path.dirname(destFile)):
                                os.makedirs(os.path.dirname(destFile))
                            copy(source_file, destFile)
                            num_copied += 1
                            percentage = int(round((num_copied/float(num_files))*100))
                            self.install_update.emit([percentage, text % str(key)])
                except PermissionError:
                    logging.exception('thread_functions.py - InstallFile - run - installation failed')
                    self.install_failed.emit()
                    break
        else:
            prosim_list = ['ProSim737', 'ProSimMCP', 'ProSimCDU', 
                            'ProSimDisplay', 'ProSimPanel', 'ProSimAudio']
            text = self.text_translations['Install-complete'][self.config_dict['OPTIONS'].get('language')]
            for folder in prosim_list:
                try:
                    prosim_target = self.prosim_path[folder]
                    num_files = self.count_files(self.directory + folder)
                    try:
                        for dest in prosim_target:
                            num_copied = 0
                            for path, _, filenames in os.walk(self.directory + folder):
                                for file in filenames:
                                    percentage = int(round((num_copied/float(num_files))*100))
                                    self.install_update.emit([percentage, text % (str(folder), str(os.path.basename(os.path.normpath(dest))))])
                                    source_file = os.path.join(path, file)
                                    dest_file = os.path.join(path.replace(self.directory + folder, dest), file)
                                    if not os.path.isdir(os.path.dirname(dest_file)):
                                        os.makedirs(os.path.dirname(dest_file))
                                    copy(source_file, dest_file)
                                    num_copied += 1
                                    percentage = int(round((num_copied/float(num_files))*100))
                                    self.install_update.emit([percentage, text % (str(folder), str(os.path.basename(os.path.normpath(dest))))])
                    except PermissionError:
                        logging.exception('thread_functions.py - InstallFile - run - installation failed')
                        self.install_failed.emit()
                        break
                except KeyError:
                    logging.exception('thread_functions.py - InstallFile - run - folder ' + folder + ' is missing')
        self.install_done.emit()
    
    def count_files(self, directory):
        logging.debug('thread_functions.py - InstallFile - count_files - directory ' + directory)
        files = []
        if os.path.isdir(directory):
            for _, _, filenames in os.walk(directory):
                files.extend(filenames)
        return len(files)
    
    def read_backup_xml(self, xml_file):
        logging.debug('thread_functions.py - InstallFile - read_backup_xml')
        path_dict = {}
        f = open(xml_file, 'r')
        doc = xml.dom.minidom.parse(f)
        backup_element = self.get_element(doc, 'BackupInstance')
        for element in backup_element:
            prosim_folder = self.get_element_value(element, 'BackupFile')[:-4]
            target_folder = self.get_element_value(element, 'BackupPath')
            logging.debug('button_functions.py - InstallFile - read_backup_xml - prosim_folder ' + str(prosim_folder)
                          + ' ; target_folder ' + target_folder)
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
        logging.debug('thread_functions.py - InstallFile - stop')
        self.terminate()
    
    
class ZipProsim(Qt.QThread):
    zip_update = QtCore.pyqtSignal(list)
    zip_done = QtCore.pyqtSignal()
    def __init__(self, directory, prosim_path, credentials, config_dict, text_translations):
        logging.debug('thread_functions.py - ZipProsim - __init__ - directory ' + str(directory)
                      + ' ; prosim_path' + str(prosim_path))
        Qt.QThread.__init__(self)
        self.config_dict = config_dict
        self.text_translations = text_translations
        self.directory = directory
        self.prosim_path = prosim_path
        self.credentials = credentials
        self.temp_directory = tempfile.mkdtemp()

    def run(self):
        logging.debug('thread_functions.py - ZipProsim - run')
        multiple_folder_list = []
        for _, value in self.prosim_path.items():
            if isinstance(value, list):
                for folder in value:
                    multiple_folder_list.append(os.path.basename(os.path.normpath(folder)))
            else:
                multiple_folder_list.append(os.path.basename(os.path.normpath(value)))
        for x in set(multiple_folder_list):
            multiple_folder_list.remove(x)
        multiple_folder_list = list(set(multiple_folder_list))
        timestr = time.strftime("%Y-%m-%dT%H-%M-%S")
        timexml = time.strftime("%Y-%m-%d %H:%M:%S")
        backup_list = []
        i = 0
        for _, value in self.prosim_path.items():
            if isinstance(value, list):
                for path in value:
                    zip_name = os.path.basename(os.path.normpath(path))
                    if multiple_folder_list:
                        if zip_name in multiple_folder_list:
                            zip_name += '_' + str(i)
                            i += 1
                    logging.debug('thread_functions.py - ZipProsim - run - self.temp_directory ' + str(self.temp_directory)
                                  + ' ; zip_name ' + str(zip_name) + '.zip ; path ' + str(path))
                    zipf = zipfile.ZipFile(self.temp_directory + '\\' + zip_name + '.zip', 'w', zipfile.ZIP_DEFLATED)
                    self.zipdir(path + '\\', zipf)
                    zipf.close()
                    backup_list.append([zip_name + '.zip', path])
            else:
                zip_name = os.path.basename(os.path.normpath(value))
                if multiple_folder_list:
                    if zip_name in multiple_folder_list:
                        zip_name += '_' + str(i)
                        i += 1
                logging.debug('thread_functions.py - ZipProsim - run - self.temp_directory ' + str(self.temp_directory)
                              + ' ; zip_name ' + str(zip_name) + '.zip ; path ' + str(value))
                zipf = zipfile.ZipFile(self.temp_directory + '\\' + zip_name + '.zip', 'w', zipfile.ZIP_DEFLATED)
                self.zipdir(value + '\\', zipf)
                zipf.close()
                backup_list.append([zip_name + '.zip', value])
        self.create_backup_xml(self.temp_directory + '\\backup_options.xml', timexml, backup_list) 
        zipb = zipfile.ZipFile(self.directory + '\\Prosim737_backup_' + timestr + '.zip', 'w', zipfile.ZIP_DEFLATED)
        self.zipdir(self.temp_directory, zipb)
        zipb.close()
        rmtree(self.temp_directory)
        self.zip_done.emit() 
        
    def zipdir(self, path, ziph):
        logging.debug('thread_functions.py - ZipProsim - zipdir')
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
                    if path == self.temp_directory:
                        folder = ziph.filename[:-4]
                    else:
                        folder = path
                    text = self.text_translations['Compressing-complete'][self.config_dict['OPTIONS'].get('language')]
                    self.zip_update.emit([percentage, text % os.path.basename(os.path.normpath(folder))])

    def create_backup_xml(self, out_file_name, timestr, backup_list):
        logging.debug('thread_functions.py - ZipProsim - create_backup_xml')
        doc = xml.dom.minidom.Document()
        doc_root = self.add_element(doc, "BackupOptions", doc)
        doc_root.setAttribute("xmlns:updater", 'ProsimUpdater')
        self.add_element(doc, "CreationTime", doc_root, timestr)
        for sublist in backup_list:
                backup_element = self.add_element(doc, "BackupInstance", doc_root)
                self.add_element(doc, "BackupFile", backup_element, sublist[0])
                self.add_element(doc, "BackupPath", backup_element, sublist[1])
        for key, value in self.credentials.items():
            backup_element = self.add_element(doc, "CredentialInstance", doc_root)
            self.add_element(doc, "CredentialComputer", backup_element, key)
            self.add_element(doc, "CredentialUsername", backup_element, value['username'])
            self.add_element(doc, "CredentialPassword", backup_element, value['password'])
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
        logging.debug('thread_functions.py - ZipProsim - stop')
        self.terminate()


class CheckProsimPath(Qt.QThread):
    check_done = QtCore.pyqtSignal(list)
    def __init__(self, folders):
        logging.debug('thread_functions.py - CheckProsimPath - __init__ - folders ' + str(folders))
        Qt.QThread.__init__(self)
        self.folders = folders
        
    def run(self):
        logging.debug('thread_functions.py - CheckProsimPath - run')
        wrong_path = []
        for _, value in self.folders.items():
            if isinstance(value, list):
                for path in value:
                    if not os.path.isdir(path):
                        wrong_path.append(path)
            else:
                if not os.path.isdir(value):
                    wrong_path.append(value)
        self.check_done.emit(wrong_path)
         
    def stop(self):
        logging.debug('thread_functions.py - CheckProsimPath - stop')
        self.terminate()
        

class CheckProsimProcesses(Qt.QThread):
    check_done = QtCore.pyqtSignal(list)
    check_relaunch = QtCore.pyqtSignal(list)
    check_wrong = QtCore.pyqtSignal(list)
    def __init__(self, folders, prosim_credentials, kill, relaunch):
        logging.debug('thread_functions.py - CheckProsimProcesses - __init__ - folders ' + str(folders))
        Qt.QThread.__init__(self)
        self.kill = kill
        self.relaunch = relaunch
        self.folders = folders
        self.prosim_credentials = prosim_credentials
        self.process_list = []
   
    def run(self):
        logging.debug('thread_functions.py - CheckProsimProcesses - run')
        pythoncom.CoInitialize()  # @UndefinedVariable
        prosim_processes = ['Prosim737.exe', 'ProsimAudio.exe', 'ProsimCDU.exe',
                            'ProsimMCP.exe', 'ProsimPanel.exe', 'ProsimDisplay.exe']
        computer_list = []
        wrong_computer_list = []
        for _, value in self.folders.items():
            if isinstance(value, list):
                for folder in value:
                    if ':' in os.path.splitdrive(folder)[0]:
                        computer_list.append(':')
            else:
                if ':' in os.path.splitdrive(value)[0]:
                    computer_list.append(':')
        for key, _ in self.prosim_credentials.items():
            find = False
            for _, value in self.folders.items():
                if isinstance(value, list):
                    for folder in value:
                        if folder[:2] == '\\\\':
                            index = folder[2:].find('\\')
                            if key == folder[2:][:index]:
                                computer_list.append(key)
                                find = True
                else:
                    if value[:2] == '\\\\':
                            index = value[2:].find('\\')
                            if key == value[2:][:index]:
                                computer_list.append(key)
                                find = True
            if not find:
                wrong_computer_list.append(key)
        if not self.prosim_credentials:
            logging.debug('thread_functions.py - CheckProsimProcesses  - run - no credentials')
        if wrong_computer_list:
            self.check_wrong.emit(wrong_computer_list)
            time.sleep(10)
        computer_list = list(set(computer_list))
        running_processes = []
        #relaunch_process = []
        try:
            for computer in computer_list:
                if computer == ':':
                    connection = wmi.WMI()
                    local_list = connection.Win32_Process()
                    local_list_name = []
                    for process in local_list:
                        local_list_name.append(process.Name)
                    for process in prosim_processes:
                        while process in local_list_name:
                            index = local_list_name.index(process)
                            if self.kill:    
                                '''if self.relaunch:
                                    relaunch_process.append('local - ' + local_list[index].ExecutablePath)'''
                                local_list[index].Terminate()   
                            else:
                                running_processes.append('Local - ' + process)
                            local_list_name.remove(process)
                            local_list.pop(index)
                else:
                    username = self.prosim_credentials[computer]['username']
                    password = self.prosim_credentials[computer]['password']
                    connection = wmi.WMI(computer, user=username, password=password)
                    local_list = connection.Win32_Process()
                    connection = None
                    local_list_name = []
                    for process in local_list:
                        local_list_name.append(process.Name)
                    for process in prosim_processes:
                        while process in local_list_name:
                            index = local_list_name.index(process)
                            if self.kill:    
                                '''if self.relaunch:
                                    relaunch_process.append(computer + ' - ' + local_list[index].ExecutablePath)'''
                                local_list[index].Terminate()   
                            else:
                                running_processes.append(computer + ' - ' + process)
                            local_list_name.remove(process)
                            local_list.pop(index)
        except Exception:
            logging.exception('thread_functions.py - CheckProsimProcesses  - run')
            running_processes = [computer]
        '''if relaunch_process:
            self.check_relaunch.emit(relaunch_process)'''
        self.check_done.emit(running_processes)  
        
    def stop(self):
        logging.debug('thread_functions.py - CheckProsimProcesses - stop')
        self.terminate()


class CheckProsim737Online(Qt.QThread):
    finished = QtCore.pyqtSignal(list)
    
    def __init__(self, domain):
        Qt.QThread.__init__(self)
        logging.debug('thread_functions.py - CheckProsim737Online - __init__')
        self.url = ['http://prosim-ar.com/downloads/',
                    'http://download.prosim-ar.com/ProSim737beta/']
        self.domain = domain
        
    def run(self):
        logging.debug('mainwindow.py - CheckProsim737Online - run')
        file_names_beta = []
        file_names = []
        for index, url in enumerate(self.url):
            try:
                soup = BeautifulSoup(requests.get(url).text, "html.parser")
                file_list = (soup.find_all('a'))
                for i in file_list:
                    link = i.get('href', None)
                    if link is not None and 'zip' in link and 'ProSim737-v' in link:
                        filename = link[link.rfind('/')+1:]
                        if index == 0:
                            file_names.append(filename)
                        elif index == 1 and 'b' in filename:
                            file_names_beta.append(filename)
            except Exception:
                logging.exception('thread_functions.py - CheckProsim737Online - run - internet '
                              + 'connection error - url ' + url)
                if index == 0:
                    file_names = None
                else:
                    file_names_beta = None
        if file_names:
            file_names = natsorted(file_names)
        if file_names_beta:
            file_names_beta = natsorted(file_names_beta)
        self.finished.emit([self.domain, file_names, file_names_beta])
        
    def stop(self):
        self.terminate()
        
        
class CheckProsim737UpdaterOnline(Qt.QThread):
    finished = QtCore.pyqtSignal(str)
    
    def __init__(self):
        Qt.QThread.__init__(self)
        logging.debug('thread_functions.py - CheckProsim737UpdaterOnline - __init__')
    
    def run(self):
        logging.debug('thread_functions.py - CheckProsim737UpdaterOnline - run')
        url = 'https://api.github.com/repos/olivierpascalhenry/Prosim737-Updater/releases/latest'
        try:
            json_object = requests.get(url=url).json()
            if LooseVersion(_updater_version) < LooseVersion(json_object['tag_name']):
                self.finished.emit(json_object['assets'][0]['browser_download_url'])
            else:
                self.finished.emit('no new version')
        except Exception:
            logging.exception('thread_functions.py - CheckProsim737UpdaterOnline - run - internet connection error - url ' + url)
    
    def stop(self):
        self.terminate()    
    