import logging

def objectsInit(self):
    logging.debug('object_functions.py - objectsInit - loading ...')
    self.server_hl_list = []
    self.server_lb_list = []
    self.server_ln_list = []
    self.server_bt_list = []
    self.server_no_list = []
    self.server_dl_list = []
    self.server_num = 0
    self.mcp_hl_list = []
    self.mcp_lb_list = []
    self.mcp_ln_list = []
    self.mcp_bt_list = []
    self.mcp_no_list = []
    self.mcp_dl_list = []
    self.mcp_num = 0
    self.cdu_hl_list = []
    self.cdu_lb_list = []
    self.cdu_ln_list = []
    self.cdu_bt_list = []
    self.cdu_no_list = []
    self.cdu_dl_list = []
    self.cdu_num = 0
    self.display_hl_list = []
    self.display_lb_list = []
    self.display_ln_list = []
    self.display_bt_list = []
    self.display_no_list = []
    self.display_dl_list = []
    self.display_num = 0
    self.panel_hl_list = []
    self.panel_lb_list = []
    self.panel_ln_list = []
    self.panel_bt_list = []
    self.panel_no_list = []
    self.panel_dl_list = []
    self.panel_num = 0
    self.audio_hl_list = []
    self.audio_lb_list = []
    self.audio_ln_list = []
    self.audio_bt_list = []
    self.audio_no_list = []
    self.audio_dl_list = []
    self.audio_num = 0
    self.cred_hl_1_list = []
    self.cred_hl_2_list = []
    self.cred_hl_3_list = []
    self.cred_vl_1_list = []
    self.cred_lb_1_list = []
    self.cred_lb_2_list = []
    self.cred_lb_3_list = []
    self.cred_ln_1_list = []
    self.cred_ln_2_list = []
    self.cred_ln_3_list = []
    self.cred_dl_list = []
    self.cred_num = 0
    
    self.category_name = {
        'server':'Server',
        'mcp':'MCP',
        'cdu':'CDU',
        'display':'Display',
        'panel':'Panel',
        'audio':'Audio'}
    
    self.button_information = [
        ("<html><head/><body><p align=\"justify\">Add here the folder in which all Prosim737 updates are stored."
         + " That folder will be used to store an update donwloaded from the Official Prosim737 website if the user click "
         + "the <b><font size='4'>&laquo;</font></b> button.</p></body></html>"),
        ("<html><head/><body><p align=\"justify\">Add here the folder which will welcome all Prosim737 backups.</p></bod"
         + "y></html>"),
        ("<html><head/><body><p align=\"justify\">By clicking on <b>Create a backup</b>, a backup with a time stamp will be c"
         + "reated in the backup folder. Click on <b>Restore a backup</b> to display a list of all backups available in the "
         + "backup folder and have the possibility to restore one of them.</p></body></html>"),
        ("<html><head/><body><p align=\"justify\">Once a file is selected, click on <b>Update</b> to install the correspondi"
         + "ng update. if an update file has been selected from the online repository, it will be downloaded and installed"
         + " at the same time.</p><p align=\"justify\">To store an online update locally, just click on the <b><font size='4'>"
         + " &laquo;</font></b> button."
         + "The update will be downloaded and stored, but not installed.</p></p><p align=\"justify\">Click on <b>Changelog</b>"
         + " to display the changelog from Prosim737 website.</p></body></html>"),
        ("<html><head/><body><p align=\"justify\">Add here the folder in which ProsimServer is installed. It is possible to "
         + "add multiple folders.</p><p>Examples:<ul><li>C:\Simulator\Prosim737</li><li>\\\COMPUTER\Simulator\Prosim737</li>"
         + "</ul></p></body></html>"),
        ("<html><head/><body><p align=\"justify\">Add here the folder in which ProsimMCP is installed. It is possible to "
         + "add multiple folders.</p><p>Examples:<ul><li>C:\Simulator\ProsimMCP</li><li>\\\COMPUTER\Simulator\ProsimMCP</li>"
         + "</ul></p></body></html>"),
        ("<html><head/><body><p align=\"justify\">Add here the folder in which ProsimCDU is installed. It is possible to "
         + "add multiple folders.</p><p>Examples:<ul><li>C:\Simulator\ProsimCDU</li><li>\\\COMPUTER\Simulator\ProsimCDU</li>"
         + "</ul></p></body></html>"),
        ("<html><head/><body><p align=\"justify\">Add here the folder in which ProsimDisplay is installed. It is possible to "
         + "add multiple folders.</p><p>Examples:<ul><li>C:\Simulator\ProsimDisplay</li><li>\\COMPUTER\Simulator\ProsimDisplay</li>"
         + "</ul></p></body></html>"),
        ("<html><head/><body><p align=\"justify\">Add here the folder in which ProsimPanel is installed. It is possible to "
         + "add multiple folders.</p><p>Examples:<ul><li>C:\Simulator\ProsimPanel</li><li>\\\COMPUTER\Simulator\ProsimPanel</li>"
         + "</ul></p></body></html>"),                   
        ("<html><head/><body><p align=\"justify\">Add here the folder in which ProsimAudio is installed. It is possible to "
         + "add multiple folders.</p><p>Examples:<ul><li>C:\Simulator\ProsimAudio</li><li>\\\COMPUTER\Simulator\ProsimAudio</li>"
         + "</ul></p></body></html>"),
        ("<html><head/><body><p align=\"justify\">If one or more Prosim737 modules are installed on one or more remote computers, Prosim737 Updater"
         + " can check running processes and terminate them before installing an update. It can be performed only if it has an access to "
         + "remote computers. You can enter here credentials to provide the access to Prosim737 Updater.</p><p>Computer name"
         + " / IP address: write the name / IP of the remote computer ; it should be the same as the one displayed in the paths entered "
         + "in the different sections (COMPUTER for \\\COMPUTER\Prosim737, or 192.168.1.12 for \\\ 192.168.1.12\Prosim737."
         + "</p><p>Password and Username: the usual Windows password and username used to login.</p></body></html>")]
    
    logging.debug('object_functions.py - objectsInit - loaded ...')