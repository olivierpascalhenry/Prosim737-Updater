import logging

def objectsInit(self):
    logging.debug('object_functions.py - objectsInit - loading ...')
    self.language_list = {}
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

    logging.debug('object_functions.py - objectsInit - loaded ...')