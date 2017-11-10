import logging
import os
import sys
import configparser
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ui.mainwindow import MainWindow
from ui._version import _updater_version


def launch_prosim_updater(path):
    app = QApplication(sys.argv)
    splash_pix = QPixmap('icons\splash_screen.svg')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    config_dict = configparser.ConfigParser()
    if not os.path.exists(os.path.join(path, 'prosim_updater.ini')):
        config_dict['LOG'] = {'level': 'DEBUG',
                              'path': ''}
        config_dict['OPTIONS'] = {'language':'english',
                                  'check_update':'False',
                                  'terminate_processes':'False',
                                  'relaunch_processes':'False'}
        with open(os.path.join(path, 'prosim_updater.ini'), 'w') as configfile:
            config_dict.write(configfile)
    config_dict.read(os.path.join(path, 'prosim_updater.ini'))
    if not config_dict['OPTIONS'].get('language'):
        config_dict.set('OPTIONS', 'language', 'english')
        with open(os.path.join(path, 'prosim_updater.ini'), 'w') as configfile:
            config_dict.write(configfile)
    if not config_dict.get('LOG', 'path'):
        log_filename = os.path.join(path, 'emc_creator_log.out')
    else:
        log_filename = os.path.join(config_dict.get('LOG', 'path'),'emc_creator_log.out')
    logging.getLogger('').handlers = []
    logging.basicConfig(filename = log_filename,
                        level = getattr(logging, config_dict.get('LOG', 'level')),
                        filemode = 'w',
                        format = '%(asctime)s : %(levelname)s : %(message)s')
    formatter = logging.Formatter('%(levelname)s : %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.info('*****************************************')
    logging.info('Prosim737 Updater ' + _updater_version + ' is starting ...')
    logging.info('*****************************************')
    translations = read_translations()
    ui = MainWindow(path, config_dict, translations)
    ui.show()
    splash.finish(ui)
    sys.exit(app.exec_())


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    
def read_translations():
    translations = {}
    file_list = os.listdir('translations/')
    file_list.remove('read_me.txt')
    for file in file_list:
        name = file[:-4]
        f = open('translations/' + file, 'r', encoding='utf-8')
        for line in f:
            if line[:3] != '###':
                index = line.find('=')
                widget = line[:index]
                text = line[index + 1:].replace('\n','')
                if '|' in text:
                    tmp = []
                    index = text.find('|')
                    tmp.append(text[:index])
                    tmp.append(text[index + 1:])
                    text = tmp
                if text:
                    try :
                        existing_dict = translations[widget]
                    except KeyError:
                        existing_dict = {}
                    existing_dict[name] = text
                    translations[widget] = existing_dict
        f.close()
    return translations
    

sys.excepthook = handle_exception


if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(__file__))
    launch_prosim_updater(path)
