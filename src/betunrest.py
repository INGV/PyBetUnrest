#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 

This file is part of pyBet.

"""

import os
#import shutil
import string
import sys
import wx
import numpy as np
import getmaps as gmaps
import globalfunctions as gf
import alphabeta as ab
import ventlocation as vl
import viztool as vt
import monitoringdata as md


# CLASS BetFrame
class BetFrame(wx.Frame):

    volname = ""
    selected_outcome = ""
    selected_node = "Unrest"
    selected_path = "Unrest"
    nodes_flag = []
    
    dflDir, workDir, localDir = gf.set_dirs()
  
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition)
        icn = os.path.join(self.workDir, "doc", "icons", "betvh.png")
        #self.SetIcon(wx.Icon(icn, wx.BITMAP_TYPE_ANY))
        
        self.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, 
                            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
    
    
        # main sizers
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox_top = wx.BoxSizer(wx.HORIZONTAL)
        hbox_bot = wx.BoxSizer(wx.HORIZONTAL)
    
        # panel top left   
        self.panelTopLeft = wx.Panel(self, wx.ID_ANY)
        vboxTopLeft = wx.StaticBoxSizer(wx.StaticBox(self.panelTopLeft, 
                                        wx.ID_ANY, "SELECT VOLCANO INPUT"), 
                                        orient = wx.VERTICAL)
    
    
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        txt = ("Select Volcano folder settings ")
        hbox4.Add(wx.StaticText(self.panelTopLeft, wx.ID_ANY, txt, size=(-1,-1)), 
                  0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 10)
    
        self.butLoadPVHA = wx.Button(self.panelTopLeft, wx.ID_ANY, 
                                     "Load Volcano", size=(-1,26))
        hbox4.Add(self.butLoadPVHA, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 0)
        self.Bind(wx.EVT_BUTTON, self.load_pvha, self.butLoadPVHA)
        vboxTopLeft.Add(hbox4, 0, wx.EXPAND|wx.ALL, 10)
    
        self.panelTopLeft.SetSizer(vboxTopLeft)
        hbox_top.Add(self.panelTopLeft, 1, wx.EXPAND|wx.ALL, 5)
    
        # panel top right 
        self.panelTopRight = wx.Panel(self, wx.ID_ANY)
        vbox_top_right = wx.StaticBoxSizer(wx.StaticBox(self.panelTopRight, 
                                           wx.ID_ANY,"SELECTED VOLCANO"), 
                                           orient = wx.VERTICAL)
    
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add(wx.StaticText(self.panelTopRight, wx.ID_ANY, "Name:"), 
                                0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.volname_text = wx.StaticText(self.panelTopRight, 
                                          wx.ID_ANY, "")
        hbox4.Add(self.volname_text, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        vbox_top_right.Add(hbox4)
    
        hbox41 = wx.BoxSizer(wx.HORIZONTAL)
        hbox41.Add(wx.StaticText(self.panelTopRight, wx.ID_ANY, 
                                 "Central coordinates (UTM):"), 0, 
                                 wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.volc_center_text = wx.StaticText(self.panelTopRight, 
                                              wx.ID_ANY, " ")
        hbox41.Add(self.volc_center_text, 0, 
                   wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        vbox_top_right.Add(hbox41)
    
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.b_vent = wx.Button(self.panelTopRight, 
                                wx.ID_ANY, "Show vent location")
        hbox5.Add(self.b_vent, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.vent_location, self.b_vent)
        #self.b_vent.Disable()
        vbox_top_right.Add(hbox5)
    
        hbox_top.Add(self.panelTopRight, 1, wx.EXPAND|wx.ALL, 5)
        self.panelTopRight.SetSizer(vbox_top_right)
        self.panelTopRight.Disable()
    
        # panel bottom left    
        self.panelBotLeft = wx.Panel(self, wx.ID_ANY)
        vbox_bot_left = wx.StaticBoxSizer(wx.StaticBox(self.panelBotLeft, 
                                          wx.ID_ANY, "EVENT TREE SELECTION"), 
                                          orient=wx.VERTICAL)
        self.tree = wx.TreeCtrl(self.panelBotLeft, wx.ID_ANY)
        #self.root = self.tree.AddRoot("N123: Eruption")
        self.root = self.tree.AddRoot("Volcano")
           
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_sel_changed, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.on_item_expanded, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.on_item_collapsed, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_activated, self.tree)
    
        vbox_bot_left.Add(self.tree, 1, wx.EXPAND|wx.ALL, 5)
        hbox_bot.Add(self.panelBotLeft, 1, wx.EXPAND|wx.ALL, 5)
        self.panelBotLeft.SetSizer(vbox_bot_left)
        self.panelBotLeft.Disable()
    
        # panel bottom right (a vertical sizer containing 2 panels)
        vbox_bot_right = wx.BoxSizer(wx.VERTICAL)
           
        # sub-panel 1 
        self.panelBotRight = wx.Panel(self, wx.ID_ANY)
        vbox0 = wx.BoxSizer(wx.VERTICAL)
    
        vbox1 = wx.StaticBoxSizer(wx.StaticBox(self.panelBotRight, 
                                  wx.ID_ANY, "ABSOLUTE PROBABILITY"), 
                                  orient=wx.VERTICAL)
        vbox1.Add(wx.StaticText(self.panelBotRight, 
                                wx.ID_ANY, "Selected Path:"), 0, 
                                # wx.ALIGN_BOTTOM|wx.TOP|wx.LEFT, 5)
                                wx.LEFT, 5)
        self.display_path = wx.StaticText(self.panelBotRight, 
                                          wx.ID_ANY, " ", size=(250,100), 
                                          style=wx.ALIGN_LEFT|wx.TE_WORDWRAP)
        self.display_path.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, 
                                          wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
    
        #vbox1.Add(self.display_path, 0, wx.ALIGN_BOTTOM|wx.TOP|wx.LEFT, 5)
        vbox1.Add(self.display_path, 0, wx.LEFT, 5)
    
        vbox2 = wx.StaticBoxSizer(wx.StaticBox(self.panelBotRight, 
                                  wx.ID_ANY, "CONDITIONAL PROBABILITY"), 
                                  orient=wx.VERTICAL)
        vbox2.Add(wx.StaticText(self.panelBotRight, 
                                wx.ID_ANY, "Selected Node:"), 0, 
                                # wx.ALIGN_BOTTOM|wx.TOP|wx.LEFT, 5)
                                wx.LEFT, 5)
        self.display_node = wx.StaticText(self.panelBotRight, 
                                          wx.ID_ANY, " ", size=(250,30), 
                                          style=wx.ALIGN_LEFT|wx.TE_WORDWRAP)
        self.display_node.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, 
                                          wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
    
        #vbox2.Add(self.display_node, 0, wx.ALIGN_BOTTOM|wx.TOP|wx.LEFT, 5)
        vbox2.Add(self.display_node, 0, wx.TOP|wx.LEFT, 5)
    
        vbox0.Add(vbox1, 0, wx.EXPAND|wx.ALL, 5)
        vbox0.Add(vbox2, 0, wx.EXPAND|wx.ALL, 5)
    
        self.panelBotRight.SetSizer(vbox0)
        self.panelBotRight.Disable()
        vbox_bot_right.Add(self.panelBotRight, 0, wx.EXPAND|wx.ALL, 0)
    
    
        # sub-panel 2 -- info and help buttons    
        self.panel_vis = wx.Panel(self, wx.ID_ANY)
    
        vbox3 = wx.BoxSizer(wx.VERTICAL)
    
        hboxComp = wx.BoxSizer(wx.HORIZONTAL)
        self.bComp = wx.Button(self.panel_vis, wx.ID_ANY, 
                                name="Compute", label="COMPUTE")
        self.Bind(wx.EVT_BUTTON, self.calc_prob, self.bComp)
        hboxComp.Add(self.bComp, 0, wx.ALIGN_BOTTOM|wx.TOP|wx.LEFT, 5)
        self.bComp.Disable()
        vbox3.Add(hboxComp, 0, wx.EXPAND|wx.ALL, 0)
    
        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        self.b_info = wx.Button(self.panel_vis, wx.ID_ANY, "INFO")
        self.Bind(wx.EVT_BUTTON, self.info_frame, self.b_info)
        #self.b_help = wx.Button(self.panel_vis, wx.ID_ANY, "HELP")
        #self.Bind(wx.EVT_BUTTON, self.help, self.b_help)
        hbox7.Add(self.b_info, 0, wx.ALIGN_BOTTOM|wx.TOP|wx.LEFT, 5)
        #hbox7.Add(self.b_help, 0, wx.ALIGN_BOTTOM|wx.TOP|wx.LEFT, 5)
    
        self.b_close = wx.Button(self.panel_vis, wx.ID_ANY, "CLOSE")
        self.Bind(wx.EVT_BUTTON, self.close_bet, self.b_close)
        hbox7.Add(self.b_close, 0, wx.ALIGN_BOTTOM|wx.TOP|wx.LEFT, 5)
    
        vbox3.Add(hbox7, 0, wx.EXPAND|wx.TOP, 10)
        
        self.panel_vis.SetSizer(vbox3)
        vbox_bot_right.Add(self.panel_vis, 0, wx.EXPAND|wx.ALL, 0)
    
        hbox_bot.Add(vbox_bot_right, 0, wx.EXPAND|wx.ALL, 0)
    
        vbox.Add(hbox_top, 0, wx.EXPAND|wx.ALL, 5)
        vbox.Add(hbox_bot, 1, wx.EXPAND|wx.ALL, 5)
    
        self.sb = self.CreateStatusBar()
        #self.sb.SetStatusText("You are running on a "+ gf.getOS() + " platform")
        self.SetSizer(vbox)
        self.SetBackgroundColour("#eeeeee")
        self.SetSize((800, 580))
        self.Centre()
  
  
    def close_bet(self, event): 
        self.Destroy()
  
  
    def selLTST(self, event):
        """
        """
        if (self.rb1.GetValue()):
            print("Long Term")
            self.bSelMonData.Enable(False)
        else:
            print("Short Term")
            self.bSelMonData.Enable(True)
  
      
  
    def sel_non_magmatic(self, event):
        """
        """
      
        if (self.cNMU.GetValue()):
            print("Non-Magmatic Yes")            
        else: 
            print("Non-Magmatic No")            
  
  
    def sel_mon_data(self, event):
        """
        """
        monitorFrame = md.InsertMonitoring(self, wx.ID_ANY, "Select Monitoring data")
  
  
    def load_pvha(self, event):
        """
  
        """
  
        voldir = gf.sel_dir(self, event)
        if (voldir == ""):
            return
        else:
            if os.path.exists(voldir):
                self.read_cfg_file(voldir)
                self.volname_text.SetLabel(self.volname)
                self.tree_creation()
            else:
                msg = ("ERROR:\n File " + v1def_file + " does not exist. "
                       "Check if the Volcano selection has been made correctly.")
                gf.show_error_message(self, msg, "ERROR")
                return
  
  
  
    def calc_prob(self, event):
        """
        """    
        nodes = len(self.nodes_flag)
        print(self.imgPath)
        print(nodes, self.nodes_flag)
  
  
        if (len(self.nodes_flag) > 0):
            pa, pc, pa_ave, pc_ave = self.calc_post()
        
            pframe = vt.pyBetVizTool(None, wx.ID_ANY, "PyBetUnrest - Plotting Tool", 
                                     self.selected_path, self.selected_node, 
                                     self.nodes_flag, nodes, self.volname, 
                                     self.dtau, self.sample, self.vcx, self.vcy, 
                                     self.imgPath, self.dip45, self.nvents, self.nsizes,
                                     self.xmap_min, self.xmap_max, self.ymap_min, self.ymap_max,
                                     self.geom, self.par1, self.par2, self.par3, 
                                     self.par4, self.par5, pa, pc, pa_ave, pc_ave)
            pframe.Show(True)
            pframe.Centre()
            return True
      
  
    def info_frame(self, event):
        hw = helpWindow.HelpWindow(None, wx.ID_ANY, "PyBetUnrest Info", "doc/info.html")
        hw.Show(True)
  
      
    def on_activated(self, event):
        """
        not used
        """
        pass
  
  
    def on_item_collapsed(self, event):
        """
        not used
        """
        pass
  
  
    def on_item_expanded(self, event):
        """
        Collapse unselected tree
        """
        item_ex = event.GetItem()
        sel = self.tree.GetItemText(item_ex)
        if self.tree.GetItemParent(item_ex).IsOk():
            par = self.tree.GetItemParent(item_ex)
            item, cookie = self.tree.GetFirstChild(par)
            while item:
                if (item != item_ex):
                    self.tree.Collapse(item)
                item, cookie = self.tree.GetNextChild(par,cookie)
  
  
    def on_sel_changed(self, event):
        """
        Get selected node and full path
        """
        
        self.nodes_flag = []
        item_sel = event.GetItem()
    
        if self.tree.GetItemParent(item_sel).IsOk():
            # get selected node
            self.selected_node = self.tree.GetItemText(item_sel)
      
            # get selected full path
            root = self.tree.GetItemText(self.tree.GetRootItem())
            par = self.tree.GetItemParent(item_sel)
            node = self.tree.GetItemText(par)
            path = [self.selected_node]
            while (node != root):
                path.append(node)
                par = self.tree.GetItemParent(par)
                node = self.tree.GetItemText(par)
      
            path.append(root)
            path.reverse()
            self.selected_path = str(path[0])
            for i in range(1, len(path)):
                self.selected_path = self.selected_path + "\n" + str(path[i])
      
            #print(selected_path, path)
            
            # re-defining nodes flags 
            for i in range(1, len(path)):
                if (i == 1):
                    if path[i] == "Unrest":
                        self.nodes_flag.append(0)
                    else:
                        self.nodes_flag.append(1)
        
                if (i == 2):
                    if path[i] == "Magmatic":
                        self.nodes_flag.append(0)
                    else:
                        self.nodes_flag.append(1)
        
                if (i == 3):
                    if path[2] == "Magmatic":
                        if path[i] == "Eruption":
                            self.nodes_flag.append(0)
                        else:
                            self.nodes_flag.append(1)
           
                    else:
                        if path[i] == "Hydrothermal":
                            self.nodes_flag.append(0)
                        else:
                            self.nodes_flag.append(1)
        
                if (i == 4):  
                    # node magmatic vent location
                    if path[2] == "Magmatic":
                        for index,item in enumerate(self.nodes4):
                            if (item == path[i]):
                                self.nodes_flag.append(index)
                    # node hydrothermal eruption
                    else:
                        if path[i] == "Eruption":
                            self.nodes_flag.append(0)
                        else:
                            self.nodes_flag.append(1)
                    
         
                if (i == 5):  
                    # node magmatic size/style 
                    if path[2] == "Magmatic":
                        for index,item in enumerate(self.nodes5):
                            if (item == path[i]):
                                self.nodes_flag.append(index + 1)
                    # node hydrothermal vent location
                    else:
                        for index,item in enumerate(self.nodes4hyd):
                            if (item == path[i]):
                                self.nodes_flag.append(index)
        
                if (i == 6):
                    if path[2] == "Magmatic":
                        for index,item in enumerate(self.nodes6):
                            if (item == path[3]):
                                self.selected_outcome = index
                                self.nodes_flag.append(index + 1)
                    # node hydrothermal style
                    else:
                        if path[i] == "Explosive":
                            self.nodes_flag.append(0)
                        else:
                            self.nodes_flag.append(1)
        
                if (i == 7):
                    if path[2] == "Magmatic":
                        self.nodes_flag.append(1)
        
                #if (i == 5):
                    #self.nodes_flag.append(1)
    
        else:
            self.selected_node = self.tree.GetItemText(self.tree.GetRootItem())
            self.selected_path = self.tree.GetItemText(self.tree.GetRootItem())
    
        self.display_node.SetLabel(self.selected_node)
        self.display_path.SetLabel(self.selected_path)
  
  
    def vent_location(self, event):
        """ 
        It opens a new frame showing the vent location by creating a
        new object  vl = ventLocation.VentLocation(), which is defined
        in modules/ventLocation.py
        """
        imgPath = self.imgPath
        if (imgPath == ""):
            msg = ("WARNING\nImage map file "
                   "in" + vol_dir + string.lower(vol_name)  + " does not exist. "
                   "You can continue but no background map will be plotted.")
            gf.show_warning_message(self, msg, "WARNING")
        else:
            if (imgPath[-3:] != "png"):
                msg = ("ERROR\nImage extension format" 
                       " must be .png only.")
                gf.show_error_message(self, msg, "ERROR")
                return
        
        pars = [self.par1, self.par2, self.par3, self.par4, self.par5]
        mapLimits = [self.xmap_min, self.xmap_max, self.ymap_min, self.ymap_max]
  
        #vloc = vl.VentLocation(self, wx.ID_ANY, "Vent Location", imgPath, 
                                       #pars, mapLimits, [vcx, vcy])
        vloc = vl.VentLocation(self, wx.ID_ANY, "Vent Location", imgPath, 
                                       pars, mapLimits, [self.vcx, self.vcy])
        #vloc.SetIcon(wx.Icon(os.path.join(self.workDir, "doc", "icons", 
                             #"vent_location.png"), wx.BITMAP_TYPE_ANY))
  
  
    def read_cfg_file(self, *kargs):
        """
        
        """
  
        volcano = kargs[0]
        
        if not os.path.isfile(os.path.join(volcano, "pybet.cfg")):
            print("Error")
          
        # Main Settings
        tmp = gf.read_main_settings(volcano)
        self.volname = tmp[0]
        self.vdir = os.path.join(self.localDir, self.volname.replace(" ", "_"))
        if not os.path.exists(self.vdir):
            os.makedirs(self.vdir)
  
        vctmp = tmp[1].strip().split(",")
        self.vcx, self.vcy = float(vctmp[0]), float(vctmp[1])
        self.geom = tmp[2]
        if (self.geom == "Field"):
            pars = tmp[3].strip().split(",")
            self.par1, self.par2 = float(pars[0]), float(pars[1])
            self.par3, self.par4, self.par5 = int(pars[2]), int(pars[3]), float(pars[4])
        elif (self.geom == "Cone"):
            pars = tmp[3].strip().split(",")
            self.par1, self.par2, self.par3 = float(pars[0]), float(pars[1]), float(pars[2])
            self.par4 = -9999
            self.par5 = -9999
        else:
            print("ERROR in vent geometry")
                
        utmZone = tmp[4]
        self.dtau = tmp[5]
        self.sample = tmp[6]
        bgimage = tmp[7]
        pars = tmp[8].strip().split(",")
        self.xmap_min = float(pars[0])
        self.xmap_max = float(pars[1])
        self.ymap_min = float(pars[2])
        self.ymap_max = float(pars[3])
        monitoring_file = tmp[9]

  
        if os.path.isfile(os.path.join(volcano, monitoring_file)):
            self.monitoring = True
            tmp_par = gf.read_monitoring(os.path.join(volcano, monitoring_file))
            self.par_name = tmp_par[0]
            self.par_val = tmp_par[1]
            self.par_th1 = tmp_par[2]
            self.par_th2 = tmp_par[3]
            self.par_rel = tmp_par[4]
            self.par_wei = tmp_par[5]
            self.anPars = [1.0-tmp[10], tmp[11], tmp[12]]    # 1-a, b, lambda
        elif monitoring_file == "None":
            self.monitoring = False
            self.anPars = [0, 0, 0]
        else:
            print("\nERROR: monitoring file name is wrong.\n"
                  "If you do not have monitoring files, please set the "
                  "corresponding field as None.\n")
            sys.exit()
        
        
        # Node Unrest
        tmp = gf.read_node123(volcano, "Node Unrest")
        self.p1 = [tmp[0], 1.0-tmp[0]]
        self.l1 = int(tmp[1])
        self.d1 = [tmp[2], tmp[3]-tmp[2]]
        
        # Node Magmatic
        tmp = gf.read_node123(volcano, "Node Magmatic")
        self.p2 = [tmp[0], 1.0-tmp[0]]
        self.l2 = int(tmp[1])
        self.d2 = [tmp[2], tmp[3]-tmp[2]]
        
        # Node Magmatic Eruption
        tmp = gf.read_node123(volcano, "Node Magmatic Eruption")
        self.p3 = [tmp[0], 1.0-tmp[0]]
        self.l3 = int(tmp[1])
        self.d3 = [tmp[2], tmp[3]-tmp[2]]
        
        # Node Vent Location Magmatic
        tmp = gf.read_node4(volcano, "Node Magmatic Vent Location")
        n4file = os.path.join(volcano,tmp[0])
        A = np.loadtxt(n4file)
        self.p4 = A[:,0]
        self.d4 = A[:,1]
        self.l4 = tmp[1]
        self.nvents = np.shape(A)[0]
        nvents = self.nvents
        
        if (self.monitoring):
            self.ventMagMon = os.path.join(volcano,tmp[2])
        
        # Node Style
        tmp = gf.read_node5(volcano)
        self.dip45 = tmp[0]
        self.nsizes = tmp[1]
        nsizes = self.nsizes
        
        n5file = os.path.join(volcano,tmp[2])
        A = np.loadtxt(n5file)
        self.p5 = np.zeros((nvents,nsizes))
        self.d5 = np.zeros((nvents,nsizes))
        self.l5 = np.zeros(nvents)
        
        if (self.dip45 is False):
            for i in range(nvents):
                self.p5[i,:] = A[0:nsizes]
                self.l5[i] = A[nsizes:nsizes+1]
                self.d5[i,:] = A[nsizes+1:]
        else:
            self.p5 = A[:,0:nsizes]
            self.l5 = A[:,nsizes:nsizes+1]
            self.d5 = A[:,nsizes+1:]
            self.l5 = np.reshape(l5, (nvents))
        
  
        # automatic download of background map
        if (bgimage == "None"):
            if (gf.verify_internet_conn()):
                self.imgPath = os.path.join(volcano, "map.png")
                gmaps.get_map(self.xmap_min, self.ymap_min, 
                              self.xmap_max, self.ymap_max, 
                              utmZone, self.imgPath)
            else:
                self.imgPath = ""
                msg = ("WARNING\nInternet connection is not available.\n"
                       "You can continue but no background map will be plotted.")
                gf.show_warning_message(self, msg, "WARNING")
  
        else:    
            self.imgPath = os.path.join(volcano, bgimage)
            if os.path.exists(self.imgPath):
                pass
            else:
                msg = ("WARNING\nBackground Image path does not exist.\n"
                       "Please check your pybet.cfg file and Load again.")
                gf.show_warning_message(self, msg, "WARNING")
  
          
  
        # Node Hydrotermal
        tmp = gf.read_node123(volcano, "Node Hydrothermal")
        self.p_hydro = [tmp[0], 1.0-tmp[0]]
        self.l_hydro = int(tmp[1])
        self.d_hydro = [tmp[2], tmp[3]-tmp[2]]
        
  
        # Node Hydrotermal Eruption
        tmp = gf.read_node123(volcano, "Node Hydrothermal Eruption")
        self.p_hydro_eru = [tmp[0], 1.0-tmp[0]]
        self.l_hydro_eru = int(tmp[1])
        self.d_hydro_eru = [tmp[2], tmp[3]-tmp[2]]
        
  
        # Node Hydrotermal Eruption Size
        tmp = gf.read_node123(volcano, "Node Hydrothermal Eruption Style")
        self.p_hydro_eru_size = [tmp[0], 1.0-tmp[0]]
        self.l_hydro_eru_size = int(tmp[1])
        self.d_hydro_eru_size = [tmp[2], tmp[3]-tmp[2]]
  
        # Node Vent Location Magmatic
        tmp = gf.read_node4(volcano, "Node Hydrothermal Vent Location")
        n4file = os.path.join(volcano,tmp[0])
        A = np.loadtxt(n4file)
        self.p4hyd = A[:,0]
        self.d4hyd = A[:,1]
        self.l4hyd = tmp[1]
        #nvents = np.shape(A)[0]
        if (self.monitoring):
            self.ventHydMon = os.path.join(volcano,tmp[2])
  
        return
      
  
    def calc_post(self, *kargs):
        """ 
        """ 
        
        nodes_flag = self.nodes_flag
        sample = self.sample
        par_name = self.par_name
        par_val = self.par_val 
        par_th1 = self.par_th1
        par_th2 = self.par_th2
        par_rel = self.par_rel
        par_wei = self.par_wei
        anPars = self.anPars
        nvents = self.nvents
        nsizes = self.nsizes
        ventMagMon = self.ventMagMon
        ventHydMon = self.ventHydMon
        monitoring = self.monitoring
        
  
        # tree selection
        #iout = 0                      # selected outcome
        nodes = len(nodes_flag)
        
        pp_con = []
        pp_con_ave = []
  
        if (nodes <= 0):
            print("Error")
  
        # Node Unrest
        if (nodes > 0):
            node = "Unrest"
            alpha_unrest = ab.make_alpha16(2, self.p1, self.l1, self.d1)
            posterior = np.random.dirichlet(alpha_unrest, sample).transpose()
            aveLT = ab.theoretical_average(alpha_unrest)
  
            if (monitoring):
                tmp = ab.calc_anomaly_degree(par_th1[node], par_th2[node], 
                                             par_rel[node], par_val[node])
                DegUnrest = 1 - np.prod(1.0-np.array(tmp))
                print("Degree of Unrest: {0}".format(DegUnrest))
                
                aveM = 1.0
                nmix = int(DegUnrest*sample)
                sample1 = np.ones((nmix))
                sample2 = np.array(posterior[0][:sample-nmix])
                pp_yes = np.concatenate([sample1,sample2])  
      
                sample1 = np.zeros((nmix))
                sample2 = np.array(posterior[1][:sample-nmix])
                pp_no = np.concatenate([sample1,sample2])  
                
                tmp = np.transpose(np.vstack((pp_yes,pp_no)))
                pp_unrest = np.random.permutation(tmp)
                pp_con_ave.append(ab.mixing_average(aveLT, aveM, DegUnrest))
      
            else:
                DegUnrest = 0
                pp_con_ave.append(aveLT)
                pp_unrest = posterior.transpose()
      
            pp_con.append(pp_unrest[:,nodes_flag[0]])
            pp_abs = pp_unrest[:,nodes_flag[0]]
            pp_abs_ave = np.prod(np.array(pp_con_ave))
            print("P Unrest: {0}".format(np.mean(pp_unrest, axis=0)))
          
        # Node Magmatic
        if (nodes > 1):
            node = "Magmatic"
            alpha_magma = ab.make_alpha16(2, self.p2, self.l2, self.d2)
            posterior = np.random.dirichlet(alpha_magma, sample).transpose()
            aveLT = ab.theoretical_average(alpha_magma)
            if (monitoring and node in list(par_name.keys())):
                probM, aveM = ab.calc_monitoring_prob(par_th1[node], par_th2[node], 
                                               par_rel[node], par_val[node], 
                                               par_wei[node], sample, nmix, anPars)     
                pp_magma = ab.mixing(posterior, probM, sample, nmix)
                pp_con_ave.append(ab.mixing_average(aveLT, aveM, DegUnrest))
            else:
                pp_con_ave.append(aveLT)
                pp_magma = posterior.transpose()
  
            pp_con.append(pp_magma[:,nodes_flag[1]])
            pp_abs = pp_abs*pp_magma[:,nodes_flag[1]]
            pp_abs_ave = np.prod(np.array(pp_con_ave))
            
            print("P Magmatic: {0}".format(np.mean(pp_magma, axis=0)))
  
  
        # Magmatic Branch
        if (nodes > 2 and nodes_flag[1] == 0):
  
            # Node Magmatic Eruption
            if (nodes > 2):
                node = "Magmatic Eruption"
                alpha_magma_eru = ab.make_alpha16(2, self.p3, self.l3, self.d3)
                posterior = np.random.dirichlet(alpha_magma_eru, sample).transpose()
                aveLT = ab.theoretical_average(alpha_magma_eru)
                if (monitoring and node in list(par_name.keys())):
                    probM, aveM = ab.calc_monitoring_prob(par_th1[node], par_th2[node], 
                                                   par_rel[node], par_val[node], 
                                                   par_wei[node], sample, nmix, anPars)
                    pp_magma_eru = ab.mixing(posterior, probM, sample, nmix)
                    pp_con_ave.append(ab.mixing_average(aveLT, aveM, DegUnrest))
                else:
                    pp_con_ave.append(aveLT)
                    pp_magma_eru = posterior.transpose()
      
                pp_con.append(pp_magma_eru[:,nodes_flag[2]])
                pp_abs = pp_abs*pp_magma_eru[:,nodes_flag[2]]
                pp_abs_ave = np.prod(np.array(pp_con_ave))
                print("P Magmatic Eru: {0}".format(np.mean(pp_magma_eru, axis=0)))
                #print("P Abs: {0}".format(np.mean(pp_abs, axis=0)))
  
  
            # Node 4 Magmatic Vents
            if (nodes > 3):
  
                if (nodes_flag[3] == 0):
                    ind4 = list(range(nvents)) 
                else:
                    ind4 = [int(nodes_flag[3]-1)]
                  
                alpha4 = ab.make_alpha16(nvents, self.p4, self.l4, self.d4)
                posterior = np.random.dirichlet(alpha4, sample).transpose()
                aveLT = ab.theoretical_average(alpha4)
                if (monitoring):
                    nmix4 = int(min(DegUnrest,0.5)*sample)
                    if (not os.path.isfile(ventMagMon)):
                        pp_vent = posterior.transpose()
                        pp_con_ave.append(aveLT)
                    else:
                        n4freq = np.loadtxt(ventMagMon)
                        npars_vent = np.size(n4freq)/nvents
                        print("Number of monitoring paramenters at Vent Location: {0}".format(npars_vent))
                        
                        if (1-(np.sum(n4freq)/npars_vent) > 0.05 ):
                            msg = "ERROR:\nPlease check the file {0}\n " \
                                  "The sum of frequencies in each column " \
                                  "is not 1.0 \nCorrect the values and " \
                                  "try again".format(ventMagMon)
                            gf.show_error_message(self, msg, "ERROR") 
                            return    
                          
                        if (len(np.shape(n4freq)) == 1):
                            n4pars = np.shape(n4freq)
                            alpha4M = nvents*n4freq
                        else:
                            n4pars, tmp = np.shape(n4freq)
                            alpha4M = nvents*(np.mean(n4freq,axis=1))
                          
                        aveM = alpha4M/np.sum(alpha4M)
                        probM = np.random.dirichlet(alpha4M, nmix4)     
                        pp_vent = ab.mixing(posterior, probM, sample, nmix4)
                        pp_con_ave.append(ab.mixing_average(aveLT, aveM, nmix4/float(sample)))
                else:
                    pp_con_ave.append(aveLT)
                    pp_vent = posterior.transpose()
  
                pp4 = pp_vent[:,ind4]
  
                pp_con.append(pp_vent)
                  
                pp_tmp = np.zeros((sample,len(ind4)))
                for i in range(len(ind4)):
                    pp_tmp[:,i] = pp_abs*pp4[:,i]
  
                pp_abs = pp_tmp
                pp_abs_ave = np.prod(np.array(pp_con_ave[0:3]))*pp_con_ave[-1][ind4]
                #print("P Magmatic Vent: {0}".format(np.mean(pp4, axis=0)))
      
            # Node 5 Magmatic Sizes/Styles 
            if (nodes > 4):
                tmp5 = np.zeros((nvents, sample, nsizes))
              
                alpha5 = [0]*(nvents)
                for i in range(nvents):
                    alpha5[i] = ab.make_alpha16(nsizes, self.p5[i,:], 
                                                       self.l5[i], 
                                                       self.d5[i,:])
                    posterior = np.random.dirichlet(alpha5[i], sample)
                    tmp5[i,:,:] = posterior
              
                if (int(nodes_flag[4])%2==0):
                    tmp = int(nodes_flag[4])/2 - 1
                    ind5 = list(range(tmp, nsizes)) 
                else:
                    ind5 = [int( (nodes_flag[4]+1)/2 - 1 )]
              
                
                pp5 = np.zeros((len(ind4),sample,len(ind5)))
                for i in range(len(ind4)):
                    #pp5[i,:,:] = np.transpose(tmp5[ind4[i],:,ind5])
                    pp5[i,:,:] = tmp5[ind4[i],:,:]
              
                aveLT = np.zeros((len(ind4),nsizes))
                for i in range(len(ind4)):
                    aveLT[i,:] = ab.theoretical_average(alpha5[ind4[i]])
  
                pp5cond = np.zeros((sample,nsizes))
                for j in range(nsizes):
                    tmp0 = 0
                    tmp1 = 0
                    for i in range(len(ind4)):
                        tmp0 += pp4[:,i]
                        tmp1 += pp4[:,i]*tmp5[ind4[i],:,j]
                    # p cond each size / selected vents
                    pp5cond[:,j] = tmp1/tmp0
  
                pp_con.append(pp5cond)
                pp_con_ave.append(np.mean(aveLT, axis=0))
                  
                ind = 0
                pp_tmp = np.zeros((sample,len(ind4)*len(ind5)))
                pp_abs_ave = np.zeros((len(ind4)*len(ind5)))
                pp_ave123 = np.prod(np.array(pp_con_ave[0:3]))
  
                for i in range(len(ind4)):
                    for j in range(len(ind5)):
                        pp_tmp[:,ind] = pp_abs[:,i]*pp5[i,:,j]
                        pp_abs_ave[ind] = pp_ave123*pp_con_ave[-2][ind4[i]]*pp_con_ave[-1][ind5[j]]
                        ind += 1
                
                pp_abs = pp_tmp
                #print("P Magmatic Size: {0}".format(np.mean(pp5cond, axis=0)))
                              
  
        else: # non-magamtic branch
  
          # Node Hydrotermal
          if (nodes > 2):
              node = "Hydrothermal"
              alpha_hydro = ab.make_alpha16(2, self.p_hydro, 
                                              self.l_hydro, 
                                              self.d_hydro)
              posterior = np.random.dirichlet(alpha_hydro, sample).transpose()
              aveLT = ab.theoretical_average(alpha_hydro)
              if (monitoring and node in list(par_name.keys())):
                  probM, aveM = ab.calc_monitoring_prob(par_th1[node], par_th2[node], 
                                                 par_rel[node], par_val[node], 
                                                 par_wei[node], sample, nmix, anPars)
                  pp_hydro = ab.mixing(posterior, probM, sample, nmix)
                  pp_con_ave.append(ab.mixing_average(aveLT, aveM, DegUnrest))
              else:
                  pp_con_ave.append(aveLT)
                  pp_hydro = posterior.transpose()
         
              pp_con.append(pp_hydro[:,nodes_flag[2]])
              pp_abs = pp_abs*pp_hydro[:,nodes_flag[2]]
              pp_abs_ave = np.prod(np.array(pp_con_ave))
              print("P Hydro: {0}".format(np.mean(pp_hydro, axis=0)))
  
      
          # Node Hydrotermal Eruption
          if (nodes > 3):
              node = "Hydrothermal Eruption"
              alpha_hydro_eru = ab.make_alpha16(2, self.p_hydro_eru, 
                                                  self.l_hydro_eru, 
                                                  self.d_hydro_eru)
              posterior = np.random.dirichlet(alpha_hydro_eru, sample).transpose()
              aveLT = ab.theoretical_average(alpha_hydro_eru)
              if (monitoring and node in list(par_name.keys())):
                  probM, aveM = ab.calc_monitoring_prob(par_th1[node], par_th2[node], 
                                                 par_rel[node], par_val[node], 
                                                 par_wei[node], sample, nmix, anPars)
                  pp_hydro_eru = ab.mixing(posterior, probM, sample, nmix)
                  pp_con_ave.append(ab.mixing_average(aveLT, aveM, DegUnrest))
              else:
                  pp_con_ave.append(aveLT)
                  pp_hydro_eru = posterior.transpose()
            
              pp_con.append(pp_hydro_eru[:,nodes_flag[3]])
              pp_abs = pp_abs*pp_hydro_eru[:,nodes_flag[3]]
              pp_abs_ave = np.prod(np.array(pp_con_ave))
              print("P Hydro Eru: {0}".format(np.mean(pp_hydro_eru, axis=0)))
  
      
          # Vent Location Hydrothermal
          if (nodes > 4):
              
              if (nodes_flag[4] == 0):
                  ind4 = list(range(nvents)) 
              else:
                  ind4 = [int(nodes_flag[4]-1)]
                
              alpha_vent = ab.make_alpha16(nvents, self.p4hyd, self.l4hyd, self.d4hyd)
              posterior = np.random.dirichlet(alpha_vent, sample).transpose()
              aveLT = ab.theoretical_average(alpha_vent)
  
              if (monitoring):
                  nmix4 = int(min(DegUnrest,0.5)*sample)
                  if (not os.path.isfile(ventHydMon)):
                      pp_vent = posterior.transpose()
                      pp_con_ave.append(aveLT)
                  else:
                      n4freq = np.loadtxt(ventHydMon)
                      npars_vent = np.size(n4freq)/nvents
                      print("Number of monitoring paramenters at Vent Location: {0}".format(npars_vent))
                      
                      if (1-(np.sum(n4freq)/npars_vent) > 0.05 ):
                          msg = "ERROR:\nPlease check the file {0}\n " \
                                "The sum of frequencies in each column " \
                                "is not 1.0 \nCorrect the values and " \
                                "try again".format(ventHydMon)
                          gf.show_error_message(self, msg, "ERROR") 
                          return    
                        
                      if (len(np.shape(n4freq)) == 1):
                          n4pars = np.shape(n4freq)
                          alpha4M = nvents*n4freq
                      else:
                          n4pars, tmp = np.shape(n4freq)
                          alpha4M = nvents*(np.mean(n4freq, axis=1))
                        
                      aveM = alpha4M/np.sum(alpha4M)
                      probM = np.random.dirichlet(alpha4M, nmix4)     
                      pp_vent = ab.mixing(posterior, probM, sample, nmix4)
                      pp_con_ave.append(ab.mixing_average(aveLT, aveM, nmix4/float(sample)))
              else:
                  pp_con_ave.append(aveLT)
                  pp_vent = posterior.transpose()
  
              #print(np.shape(pp_vent))
              pp4 = pp_vent[:,ind4]
  
              #pp_con.append(pp4)
              pp_con.append(pp_vent)
              pp_tmp = np.zeros((sample, len(ind4)))
              for i in range(len(ind4)):
                  pp_tmp[:,i] = pp_abs*pp4[:,i]
  
              pp_abs = pp_tmp
              pp_abs_ave = np.prod(np.array(pp_con_ave[0:4]))*pp_con_ave[-1][ind4]
              #print("P Hydrothermal Vent: {0}".format(np.mean(pp4, axis=0)))
            
  
          # Node Hydrotermal Eruption Style
          if (nodes > 5):
              node = "Hydrothermal Eruption Style"
              alpha_hydro_eru_size = ab.make_alpha16(2, self.p_hydro_eru_size, 
                                                       self.l_hydro_eru_size, 
                                                       self.d_hydro_eru_size)
              posterior = np.random.dirichlet(alpha_hydro_eru_size, sample).transpose()
              aveLT = ab.theoretical_average(alpha_hydro_eru)
              if (monitoring and node in list(par_name.keys())):
                  probM, aveM = ab.calc_monitoring_prob(par_th1[node], par_th2[node], 
                                                 par_rel[node], par_val[node], 
                                                 par_wei[node], sample, nmix, anPars)
                  pp_hydro_eru_size = ab.mixing(posterior, probM, sample, nmix)
                  pp_con_ave.append(ab.mixing_average(aveLT, aveM, DegUnrest))
              else:
                  pp_con_ave.append(aveLT)
                  pp_hydro_eru_size = posterior.transpose()
            
              ind = 0
              pp_tmp = np.zeros((sample,len(ind4)))
              pp_con.append(pp_hydro_eru_size[:,nodes_flag[5]])
              pp_abs_ave = np.zeros((len(ind4)))
              for i in range(len(ind4)):
                  pp_tmp[:,ind] = pp_abs[:,i]*pp_hydro_eru_size[:,nodes_flag[5]]
                  pp_abs_ave[ind] = np.prod(np.array(pp_con_ave[0:4]))*pp_con_ave[-2][ind4[i]]*pp_con_ave[-1]
                  ind += 1
              
              pp_abs = pp_tmp
              print("P Hydro Eru Size: {0}".format(np.mean(pp_hydro_eru_size, axis=0)))
      
  
  
        #print(" ")
        #print("P Abs: {0} {1}".format(np.mean(pp_abs, axis=0), 1.-np.mean(pp_abs, axis=0)))
        #print("P 10th: {0}".format(np.percentile(pp_abs, 10, axis=0)))
        #print("P 50th: {0}".format(np.percentile(pp_abs, 50, axis=0)))
        #print("P 90th: {0}".format(np.percentile(pp_abs, 90, axis=0)))
        #print(" ")
  
        return pp_abs, pp_con, pp_abs_ave, pp_con_ave[-1]
  
  
    def tree_creation(self):  
        """
        """
  
        nodes_flag = self.nodes_flag
        selected_node = self.selected_node
        selected_path = self.selected_path
        nvents = self.nvents
        nsizes = self.nsizes
        #nodes_flag = []
        #selected_node = "Unrest"
        #selected_path = "Unrest"
        
        # node unrest
        node_unrest = ["Unrest", "No Unrest"]
  
        # node magmatic
        node_magma = ["Magmatic", "Non-Magmatic"]
  
        # node magmatic eruption
        node_magma_eru = ["Eruption", "No Eruption"]
  
        # node hydrothermal
        node_hydro = ["Hydrothermal", "Tectonic"]
  
        # node hydrothermal eruption
        node_hydro_eru = ["Eruption", "No Eruption"]
  
        # node hydrothermal eruption size
        node_hydro_eru_size = ["Effusive", "Explosive"]
  
        # vent locations - magmatic branch
        if (nvents):
            self.nodes4 = ["Vent Location: All"]
            for i in range(nvents):
                self.nodes4.append("Vent Location: " + str(i+1))
  
        # vent locations - hydrothermal branch
        if (nvents):
            self.nodes4hyd = ["Vent Location: All"]
            for i in range(nvents):
                self.nodes4hyd.append("Vent Location: " + str(i+1))
  
        # node 5 -- size
        if (nsizes):
            self.nodes5 = []
            for i in range(nsizes):
                if (i != nsizes-1):
                    self.nodes5.append("Style/Size " + str(i+1))
  
                self.nodes5.append("Style/Size " + str(i+1) + "+")
  
        else:
            msg = "ERROR:\n Bad size value in v1def.txt"
            gf.show_error_message(self, msg, "ERROR") 
            return     
  
        ## nodes 6 -- outcomes 
        #self.nodes6 = []
        #for i in range(nouts):
            #self.nodes6.append("N6: " + string.capitalize(outcomes[i]))
  
        #self.nodes78 = []
        #for i in range(nouts):
            #self.nodes78.append("N78: Hazard curves")
  
  
        # creating the GUI tree 
        unrest_yes = self.tree.AppendItem(self.root,node_unrest[0])
        #unrest_no = self.tree.AppendItem(self.root,node_unrest[1])
        magma_yes = self.tree.AppendItem(unrest_yes,node_magma[0])
        magma_no = self.tree.AppendItem(unrest_yes,node_magma[1])
        # magmatic branches
        for magma_eru in node_magma_eru:
            n3 = self.tree.AppendItem(magma_yes,magma_eru)
            if (magma_eru == "Eruption"):
                for node4 in self.nodes4:
                    n4 = self.tree.AppendItem(n3,node4)
                    for node5 in self.nodes5:
                        n5 = self.tree.AppendItem(n4,node5)
                        #for i in range(len(self.nodes6)):
                            #n6 = self.tree.AppendItem(n5,self.nodes6[i])
                            #n7 = self.tree.AppendItem(n6,self.nodes78[i])
  
        # non-magmatic branches
        hydro_yes = self.tree.AppendItem(magma_no,node_hydro[0])
        hydro_no = self.tree.AppendItem(magma_no,node_hydro[1])
        hydro_eru_yes = self.tree.AppendItem(hydro_yes,node_hydro_eru[0])
        for node4hyd in self.nodes4hyd:
            n4hyd = self.tree.AppendItem(hydro_eru_yes,node4hyd)
            for item in node_hydro_eru_size:
                hydro_eru_size_yes = self.tree.AppendItem(n4hyd,item)
  
        hydro_eru_no = self.tree.AppendItem(hydro_yes,node_hydro_eru[1])
  
        self.panelTopRight.Enable()
        self.panelBotLeft.Enable()
        self.panelBotRight.Enable()
        self.bComp.Enable()
  
        selected_node = self.tree.GetItemText(self.tree.GetRootItem())
        selected_path = self.tree.GetItemText(self.tree.GetRootItem())
  
        self.display_node.SetLabel(selected_node)
        self.display_path.SetLabel(selected_path)
        
        self.Layout()



class pyBetGui(wx.App):
    """
    Instance of the main class 
    """
    def OnInit(self):
        frame = BetFrame(None, -1, "PyBetUnrest")
        frame.Show(True)
        self.SetTopWindow(frame)
        frame.Centre()
        return True


# starting the main gui
if __name__ == "__main__":
    app = pyBetGui(0)
    app.MainLoop()

