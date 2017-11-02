import xml.dom.minidom
import datetime
import logging
from PyQt5.QtWidgets import QLineEdit
from functions.button_functions import new_path
from functions.button_functions import new_credentials


NAMESPACE_URI = 'ProsimUpdater'

def create_updater_xml(self, out_file_name):
    logging.info('updater_xml.py - create_updater_xml - starting ...')
    doc = xml.dom.minidom.Document()
    doc_root = add_element(doc, "UpdaterOptions", doc)
    doc_root.setAttribute("xmlns:updater", NAMESPACE_URI)
    add_element(doc, "CreationDate", doc_root, datetime.date.isoformat(datetime.date.today()))
    
    ############################
    # Home page
    ############################
    logging.debug('updater_xml.py - create_updater_xml - home page options creation ...')
    add_element(doc, "UpdateLocation", doc_root, self.home_ln_1.text())
    if self.home_ck_1.isChecked():
        add_element(doc, "OnlineLocation", doc_root, 'yes')
    else:
        add_element(doc, "OnlineLocation", doc_root, 'no')
    add_element(doc, "BackupLocation", doc_root, self.home_ln_2.text())
    
    ############################
    # Server page
    ############################
    logging.debug('updater_xml.py - create_updater_xml - server page options creation ...')
    server_element = add_element(doc, "ServerSection", doc_root)
    all_lines = self.tabWidgetPage2.findChildren(QLineEdit)
    for widget in all_lines:
        if widget.text():
            add_element(doc, "ServerLocation", server_element, widget.text())
        
    ############################
    # MCP page
    ############################
    logging.debug('updater_xml.py - create_updater_xml - mcp page options creation ...')
    server_element = add_element(doc, "MCPSection", doc_root)
    all_lines = self.tabWidgetPage3.findChildren(QLineEdit)
    for widget in all_lines:
        if widget.text():
            add_element(doc, "MCPLocation", server_element, widget.text())
    
    ############################
    # CDU page
    ############################
    logging.debug('updater_xml.py - create_updater_xml - cdu page options creation ...')
    server_element = add_element(doc, "CDUSection", doc_root)
    all_lines = self.tabWidgetPage4.findChildren(QLineEdit)
    for widget in all_lines:
        if widget.text():
            add_element(doc, "CDULocation", server_element, widget.text())
        
    ############################
    # Display page
    ############################
    logging.debug('updater_xml.py - create_updater_xml - display page options creation ...')
    server_element = add_element(doc, "DisplaySection", doc_root)
    all_lines = self.tabWidgetPage5.findChildren(QLineEdit)
    for widget in all_lines:
        if widget.text():
            add_element(doc, "DisplayLocation", server_element, widget.text())
        
    ############################
    # Panel page
    ############################
    logging.debug('updater_xml.py - create_updater_xml - panel page options creation ...')
    server_element = add_element(doc, "PanelSection", doc_root)
    all_lines = self.tabWidgetPage6.findChildren(QLineEdit)
    for widget in all_lines:
        if widget.text():
            add_element(doc, "PanelLocation", server_element, widget.text())
        
    ############################
    # Audio page
    ############################
    logging.debug('updater_xml.py - create_updater_xml - audio page options creation ...')
    server_element = add_element(doc, "AudioSection", doc_root)
    all_lines = self.tabWidgetPage7.findChildren(QLineEdit)
    for widget in all_lines:
        if widget.text():
            add_element(doc, "AudioLocation", server_element, widget.text())
    
    ############################
    # Credentials page
    ############################
    logging.debug('updater_xml.py - create_updater_xml - credential page options creation ...')
    server_element = add_element(doc, "CredentialSection", doc_root)
    if self.cred_num > 0:
        for i in range(0, self.cred_num):
            computer_name = self.cred_ln_1_list[i].text()
            username = self.cred_ln_2_list[i].text()
            password = self.cred_ln_3_list[i].text()
            if computer_name and username:
                computer = add_element(doc, "RemoteComputer", server_element, computer_name)
                computer.setAttribute('password', password)
                computer.setAttribute('username', username)
    
    ############################
    # File Creation
    ############################
    logging.debug('updater_xml.py - create_updater_xml - file creation ...')
    f = open(out_file_name, 'w')
    f.write(doc.toprettyxml())
    f.close()
    self.saved = True
    self.modified = False
    logging.info('updater_xml.py - create_updater_xml - xml file successfully created')
    

def read_updater_xml(self, xml_file):
    logging.info('updater_xml.py - read_updater_xml - xml file reading in progress (' + str(xml_file) + ') ...')
    f = open(xml_file, 'r')
    doc = xml.dom.minidom.parse(f)
    
    ############################
    # Home page
    ############################
    logging.debug('updater_xml.py - read_updater_xml - home page options reading ...')
    updaterOptions = get_element(doc, "UpdaterOptions")
    set_text_value(self.home_ln_1, updaterOptions, "UpdateLocation")
    if get_check_value(updaterOptions, "OnlineLocation") == 'yes':
        self.home_ck_1.setChecked(True)
    set_text_value(self.home_ln_2, updaterOptions, "BackupLocation")
    
    ############################
    # Server page
    ############################
    logging.debug('updater_xml.py - read_updater_xml - server page options reading ...')
    server_element = get_element(doc, "ServerSection")
    server_list = get_element_values(server_element, 'ServerLocation')
    for index, server in enumerate(server_list):
        if index == 0:
            self.server_ln_1.setText(server.replace('/','\\'))
        else:
            new_path(self, category='server', path=server)
        
    ############################
    # MCP page
    ############################
    logging.debug('updater_xml.py - read_updater_xml - mcp page options reading ...')
    server_element = get_element(doc, "MCPSection")
    mcp_list = get_element_values(server_element, 'MCPLocation')
    for index, mcp in enumerate(mcp_list):
        if index == 0:
            self.mcp_ln_1.setText(mcp.replace('/','\\'))
        else:
            new_path(self, category='mcp', path=mcp)
    
    ############################
    # CDU page
    ############################
    logging.debug('updater_xml.py - read_updater_xml - cdu page options reading ...')
    server_element = get_element(doc, "CDUSection")
    cdu_list = get_element_values(server_element, 'CDULocation')
    for index, cdu in enumerate(cdu_list):
        if index == 0:
            self.cdu_ln_1.setText(cdu.replace('/','\\'))
        else:
            new_path(self, category='cdu', path=cdu)
     
    ############################
    # Display page
    ############################
    logging.debug('updater_xml.py - read_updater_xml - display page options reading ...')
    server_element = get_element(doc, "DisplaySection")
    display_list = get_element_values(server_element, 'DisplayLocation')
    for index, display in enumerate(display_list):
        if index == 0:
            self.display_ln_1.setText(display.replace('/','\\'))
        else:
            new_path(self, category='display', path=display)
        
    ############################
    # Panel page
    ############################
    logging.debug('updater_xml.py - read_updater_xml - panel page options reading ...')
    server_element = get_element(doc, "PanelSection")
    panel_list = get_element_values(server_element, 'PanelLocation')
    for index, panel in enumerate(panel_list):
        if index == 0:
            self.panel_ln_1.setText(panel.replace('/','\\'))
        else:
            new_path(self, category='panel', path=panel)
        
    ############################
    # Audio page
    ############################
    logging.debug('updater_xml.py - read_updater_xml - audio page options reading ...')
    server_element = get_element(doc, "AudioSection")
    audio_list = get_element_values(server_element, 'AudioLocation')
    for index, audio in enumerate(audio_list):
        if index == 0:
            self.audio_ln_1.setText(audio.replace('/','\\'))
        else:
            new_path(self, category='audio', path=audio)
    
    ############################
    # Credentials page
    ############################
    logging.debug('updater_xml.py - read_updater_xml - credential page options reading ...')
    server_element = get_element(doc, "CredentialSection")
    try:
        cred_list = get_element_values(server_element, 'RemoteComputer')
        for key, value in cred_list.items():
            new_credentials(self, [key, value['username'], value['password']])
    except AttributeError:
        pass
        
    self.modified = False
    self.make_window_title()
    logging.info('updater_xml.py - read_updater_xml - xml file successfully parsed')


def add_element(doc, element_name, parent, value=None):
    new_element = doc.createElementNS(NAMESPACE_URI, 'updater:' + element_name)
    if value:
        new_text = doc.createTextNode(value)
        new_element.appendChild(new_text)
    parent.appendChild(new_element)
    return new_element


def get_element(parent, element_name):
    return parent.getElementsByTagNameNS(NAMESPACE_URI, element_name)[0]


def set_text_value(text_widget, parent, element_name):
    node_data = get_element_value(parent, element_name)
    if node_data:
        text_widget.setText(node_data.replace('/','\\'))


def get_element_value(parent, element_name):
    elements = parent.getElementsByTagNameNS(NAMESPACE_URI, element_name)
    if elements:
        element = elements[0]
        nodes = element.childNodes
        for node in nodes:
            if node.nodeType == node.TEXT_NODE:
                return node.data.strip()


def get_check_value(parent, element_name):
    elements = parent.getElementsByTagNameNS(NAMESPACE_URI, element_name)
    return elements[0].childNodes[0].data.strip()


def get_element_values(parent, element_name):
    value_list = []
    value_dict = {}
    try:
        elements = parent.getElementsByTagNameNS(NAMESPACE_URI, element_name)
        for element in elements:
            if element.attributes.keys():
                tmp_dict = {}
                tmp_dict[element.attributes['password'].name] = element.attributes['password'].value
                tmp_dict[element.attributes['username'].name] = element.attributes['username'].value
                value_dict[element.childNodes[0].data.strip()] = tmp_dict
            else:
                value_list.append(element.childNodes[0].data.strip())
    except IndexError:
        pass
    if value_dict:
        value_list = value_dict
    return value_list
