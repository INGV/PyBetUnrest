#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 

This file is part of pyBetVH.

"""

# standard modules
import os
import random
import string
import sys
import globalfunctions as gf
import plotlibs 
import wx
import numpy as np
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.patches import Circle, Wedge, Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.backends.backend_wx import _load_bitmap
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib as mpl


# some global plotting settings
mpl.rcParams["xtick.direction"]="out"
mpl.rcParams["ytick.direction"]="out"
mpl.rcParams["axes.labelsize"]="10"
mpl.rcParams["xtick.labelsize"]="10"
mpl.rcParams["ytick.labelsize"]="10"
mpl.rcParams["legend.fontsize"]="10"
mpl.rcParams["axes.titlesize"]="10"
mpl.rcParams["font.family"]="serif"
mpl.rcParams["font.sans-serif"]="Times"


class pyBetVizTool(wx.Frame):
    """ 
    CLASS pyBetVizTool
  
    """
  
    # default values
    ptSel = 0            # selected point
    hazSel = 0           # selected hazard model
    staSel = 0           # selected statistic
    probTh = 0.01        # selected probability threshold
    intTh = 1.0          # selected intensity threshold
    tw = 0               # selected time window
    figdpi = 75          # 
    figfmt = "png"       # 
    alpha_pts = 0.75     # 
    
    dflDir, workDir, localDir = gf.set_dirs()
    
    # initialization for input.dat file 
    seed = random.uniform(-100000, -10000)   # random seed 
  
    def __init__(self, parent, id, title,
                 sel_path, sel_node, nodes_flag,
                 nodes, volname, dtau, sample, vcx, vcy, imgpath,
                 dip45, nvents, nsizes,
                 xmin_map, xmax_map, ymin_map, ymax_map,
                 geom, par1, par2, par3, par4, par5, 
                 pabs, pcon, pabs_ave, pcon_ave):
                 #p123, p4, p5, p6, pabs, pcon):
      
  
        self.sel_path = sel_path
        self.sel_node = sel_node
        self.nodes_flag = nodes_flag
        self.nodes = nodes
        self.volname = volname
        self.dtau = dtau
        self.sample = sample
        self.vcx = vcx/1000
        self.vcy = vcy/1000
        self.imgpath = imgpath
        self.dip45 = dip45
        self.nvents = nvents
        self.nsizes = nsizes
        #self.nouts = nouts
        #self.nareas = nareas
        #self.lon = lon/1000
        #self.lat = lat/1000
        #self.idarea = idarea
        #self.iml = iml
        #self.nint = nint
        #self.outcomes = outcomes
        #self.imt = imt
        self.geom = geom
        self.par1 = par1
        self.par2 = par2
        self.par3 = par3
        self.par4 = par4
        self.par5 = par5
        #self.p123 = p123
        #self.p4 = p4
        #self.p5 = p5
        #self.p6 = p6
        self.pabs_ave = pabs_ave
        self.pcon_ave = pcon_ave
        self.pabs = pabs
        self.pcon_all = pcon
        self.pcon = self.pcon_all[self.nodes-1]
  
        self.xmin_map = xmin_map/1000
        self.xmax_map = xmax_map/1000
        self.ymin_map = ymin_map/1000
        self.ymax_map = ymax_map/1000
  
        self.npts = 0
  
        #print(np.shape(self.pabs), np.mean(self.pabs))
        #print(np.shape(self.pcon), np.mean(self.pcon))
  
        title = "Visualization Toolkit"
  
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition)
        icn = os.path.join(self.workDir, "doc", "icons", "plotting_tool.png")
        #self.SetIcon(wx.Icon(icn, wx.BITMAP_TYPE_ANY))
        
        
        if (self.nodes >=1 and self.nodes <= 6):
          
            self.hbox = wx.BoxSizer(wx.HORIZONTAL)
  
            self.p1 = wx.Panel(self, wx.ID_ANY)
            self.p1.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, 
                                       wx.FONTWEIGHT_NORMAL))
            
      
            # left panel
            self.vbox1 = wx.BoxSizer(wx.VERTICAL)
            
            self.vboxAC = wx.StaticBoxSizer(wx.StaticBox(self.p1, wx.ID_ANY, 
                                           "PROBABILITY"), orient=wx.VERTICAL)
            self.hbox_sta = wx.BoxSizer(orient=wx.HORIZONTAL)
            
            if (self.nodes == 1):
                txtN123 = ("Absolute and Conditional probabability\n"
                           "at Node 123 are equivalent. \n"
                           "")
                self.txtN123 = wx.StaticText(self.p1, wx.ID_ANY, txtN123, size=(-1,-1))
                self.vboxAC.Add(self.txtN123, 0, wx.ALL, 6)
                txt = ("SELECTED PATH/NODE:\n" + sel_path)
            else:
                self.rb1ac = wx.RadioButton(self.p1, wx.ID_ANY, "ABSOLUTE", 
                                             style=wx.RB_GROUP)
                self.rb2ac = wx.RadioButton(self.p1, wx.ID_ANY, "CONDITIONAL")
                self.rb1ac.SetValue(True)
                self.vboxAC.Add(self.rb1ac, 0, wx.TOP, 2)
                self.vboxAC.Add(self.rb2ac, 0, wx.TOP, 2)
      
                self.Bind(wx.EVT_RADIOBUTTON, self.sel_abs_con_n16, self.rb1ac)
                self.Bind(wx.EVT_RADIOBUTTON, self.sel_abs_con_n16, self.rb2ac)
  
  
                txt = ("SELECTED PATH:\n" + sel_path)
  
            self.selection = wx.StaticText(self.p1, wx.ID_ANY, txt, size=(-1,-1))
            self.selection.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, 
                                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            #self.vboxAC.Add(self.selection, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 10)
            self.vboxAC.Add(self.selection, 0, wx.LEFT|wx.TOP, 10)
  
            self.vbox1.Add(self.vboxAC, 0, wx.EXPAND|wx.LEFT|wx.TOP, 10)        
      
            self.show_table_abs(self.pabs, self.pabs_ave)
            self.nwedges = self.show_table_con(self.pcon, self.pcon_ave)
            self.lcCon.Hide()
            copyBtn = wx.Button(self.p1, label="Copy Table to Clipboard")
            copyBtn.Bind(wx.EVT_BUTTON, self.copy_table_data)
            # self.vbox1.Add(copyBtn, 0, wx.TOP|wx.ALIGN_RIGHT, 4)
            self.vbox1.Add(copyBtn, 0, wx.TOP, 4)
  
            self.hbox4 = wx.BoxSizer(wx.HORIZONTAL)
            b_close_pframe = wx.Button(self.p1, wx.ID_ANY, "Close")
            self.Bind(wx.EVT_BUTTON, self.close_pframe, b_close_pframe)
            # self.hbox4.Add(b_close_pframe, 0, wx.TOP|wx.ALIGN_RIGHT, 10)
            self.hbox4.Add(b_close_pframe, 0, wx.TOP, 10)
          
            # self.vbox1.Add(self.hbox4, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
            self.vbox1.Add(self.hbox4, 0, wx.ALL, 5)
            self.p1.SetSizer(self.vbox1)
            self.hbox.Add(self.p1, 0, wx.EXPAND|wx.ALL, 5)
  
  
            # right panel
            self.vbox2 = wx.BoxSizer(wx.VERTICAL)
            self.pnlCanvas = wx.Panel(self, wx.ID_ANY)
            self.nb = wx.Notebook(self.pnlCanvas)
            self.pn4 = plotlibs.pn4Canvas(self.nb)
            self.pn5 = plotlibs.pn5Canvas(self.nb)
            self.pn6 = plotlibs.pn6Canvas(self.nb)
            
            if (self.nodes > 1):
                if (self.nodes_flag[1] == 0 ):
                    if (self.nodes >= 4):
                        self.pa = np.sum(self.pabs, axis=1)
                        self.pa_ave = np.sum(self.pabs_ave)
                    else:
                        self.pa = self.pabs
                        self.pa_ave = self.pabs_ave
      
                elif (self.nodes_flag[1] == 1 ):
                    if (self.nodes >= 5):
                        self.pa = np.sum(self.pabs, axis=1)
                        self.pa_ave = np.sum(self.pabs_ave)
                    else:
                        self.pa = self.pabs
                        self.pa_ave = self.pabs_ave
                
                else:
                    sys.exit("Error in nodes_flag[1]")
  
                self.nb.AddPage(self.pn4, "ECDF")
                self.pn4.plot_absolute_prob(None, self.pa, self.pa_ave)
  
            if (self.nodes == 1):
                self.pn4bis = plotlibs.pn4Canvas(self.nb)
                self.nb.AddPage(self.pn4bis, "Pie Chart")
                self.pn4bis.plot_conditional_prob(None, self.pcon, self.nodes, self.nodes_flag)
              
              
            condVentMapMag = (self.nodes == 4 and self.nodes_flag[1] == 0 and self.nodes_flag[3] == 0)
            condVentMapHyd = (self.nodes == 5 and self.nodes_flag[1] == 1 and self.nodes_flag[4] == 0)
            if (condVentMapMag or condVentMapHyd):
                self.nb.AddPage(self.pn5, "Vent Map")
                limitsMap = [self.xmin_map, self.xmax_map, self.ymin_map, self.ymax_map]
                pars = [self.par1, self.par2, self.par3, self.par4, self.par5]
                #pvents = np.reshape(self.pabs,,1))*self.p4
                self.pn5.show_map(self.pabs_ave, limitsMap, pars, self.vcx, self.vcy, 
                                 self.imgpath)
                #if (self.dip45 == 2):
                  #self.show_vent_map_abs_button(self.pabs)
                  #if (self.nodes >= 5):
                    #self.nb.AddPage(self.pn6, "Size Map")
                    #self.show_size_map_button(self.pabs)
  
            
            self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_tab_changed)
            #self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.on_tab_changed)
            box_nb = wx.BoxSizer(orient=wx.VERTICAL)
            box_nb.Add(self.nb, 1, wx.EXPAND|wx.ALL, 10)
            self.pnlCanvas.SetSizer(box_nb)
            
            self.vbox2.Add(self.pnlCanvas, 1, wx.EXPAND)
            #self.fig = plt.figure()
            #self.fig.set_dpi(75)
            #self.canvas = FigureCanvas(self.p1, wx.ID_ANY, self.fig)
            #self.toolbar = NavigationToolbar(self.canvas)
            #self.toolbar.DeleteToolByPos(6)
            #self.toolbar.DeleteToolByPos(6)
  
            #self.p2.SetSizer(self.vbox2)
            self.hbox.Add(self.vbox2, 1, wx.EXPAND|wx.ALL, 5)
  
  
        else:
            msg = "ERROR:\n num_sel_nodes must be >= 3 and <= 7"
            gf.show_error_message(self, msg, "ERROR") 
            return
      
        self.Bind(wx.EVT_CLOSE, self.on_quit)
        self.SetBackgroundColour("#eeeeee")
        self.sb = self.CreateStatusBar()
        self.sb.SetStatusText("... ")
        self.SetSizer(self.hbox)
        self.SetSize((950,750))
        self.Centre()
        #self.Fit()
        self.Show()
        
  
    def copy_table_data(self, event):
        """
        """
        selectedItems = []
        for i in xrange(self.lcAbs.GetItemCount()):
            str_tmp = ""
            for j in xrange(self.lcAbs.GetColumnCount()):
                str_tmp += " " + self.lcAbs.GetItemText(i,col=j)
            
            selectedItems.append(str_tmp)
  
        self.dataObj = wx.TextDataObject()
        self.dataObj.SetText("\n".join(selectedItems))
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(self.dataObj)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")
  
  
    def savefig(self, event):
        figfmt = self.cfmt.GetValue()
        figdpi = float(self.cdpi.GetValue())
  
        wld = "*." + figfmt
        dlg = wx.FileDialog(self, message="Save Figure as...", 
                            defaultDir=self.dflDir, defaultFile="", 
                            wildcard=wld, style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        
        if (dlg.ShowModal() == wx.ID_OK):
            figpath = dlg.GetPath()
            if (figpath[-4:] == "." + figfmt):
                saved_fig = figpath
            else:
                saved_fig = figpath + "." + figfmt
  
            self.fig.savefig(saved_fig, dpi=figdpi, format=figfmt, 
                             bbox_inches="tight")
          
        dlg.Destroy()
      
  
    def close_pframe(self, event):
        plt.close("all")
        self.Destroy()
  
  
    def expHazMapTab(self, event):
        """
        """
        wildcard = "Text files (*.txt; *.dat)|*.txt;*.dat| All files (*.*)|*.*"  
        dlg = wx.FileDialog(self, message="Save File as...", 
                            defaultDir=self.dflDir, defaultFile="", 
                            wildcard=wildcard, style=wx.SAVE|wx.FD_OVERWRITE_PROMPT)
        
        rows = len(self.zi)
        
        if (dlg.ShowModal() == wx.ID_OK):
            savepath = dlg.GetPath()
            
            if (savepath[-4:-3] == "."):
                filename = savepath
            else:
                filename = savepath + ".txt"
              
            fp = open(filename, "w")
            for i in range(rows):
                fp.write("{:f} {:f} {:f}\n".format(self.lon[i], self.lat[i], self.zi[i]))
                
            fp.close()
        
        dlg.Destroy()
      
      
    def expProMapTab(self, event):
        """
        """
          
        wildcard = "Text files (*.txt; *.dat)|*.txt;*.dat|All files (*.*)|*.*"  
        dlg = wx.FileDialog(self, message="Save File as...", 
                            defaultDir=self.dflDir, defaultFile="", 
                            wildcard=wildcard, style=wx.SAVE|wx.FD_OVERWRITE_PROMPT)
        
        rows = len(self.zp)
        
        if (dlg.ShowModal() == wx.ID_OK):
            savepath = dlg.GetPath()
            
            if (savepath[-4:-3] == "."):
                filename = savepath
            else:
                filename = savepath + ".txt"
              
            fp = open(filename, "w")
            for i in range(rows):
                fp.write("{:f} {:f} {:f}\n".format(self.lon[i], self.lat[i], self.zp[i]))
                
            fp.close()
        
        dlg.Destroy()
  
  
    def exp_haz_cur_tab(self, event):
        """
        """
          
        wildcard = "Text files (*.txt; *.dat)|*.txt;*.dat| All files (*.*)|*.*"  
        dlg = wx.FileDialog(self, message="Save File as...", 
                            defaultDir=self.dflDir, defaultFile="", 
                            wildcard=wildcard, style=wx.SAVE|wx.FD_OVERWRITE_PROMPT)
        
        rows = len(self.iml)
        
        if (dlg.ShowModal() == wx.ID_OK):
            savepath = dlg.GetPath()
            
            if (savepath[-4:-3] == "."):
                filename = savepath
            else:
                filename = savepath + ".txt"
              
            fp = open(filename, "w")
            for i in range(rows):
                fp.write("{:f} {:f} {:f} {:f} {:f} \n".format(self.iml[i], 
                                                          self.hcp[0][i],
                                                          self.hcp[1][i],
                                                          self.hcp[2][i],
                                                          self.hcp[3][i]))
              
            fp.close()
        
        dlg.Destroy()
  
  
    def load_data(self, *kargs):
        """
        
        """
        self.hc = kargs[0]
        # opening waiting pop-up frame
        busydlg = wx.BusyInfo("The task is in progress.. please wait", parent=self)
        wx.Yield()
  
        self.limits = [self.xmin, self.xmax, self.ymin, self.ymax]
        
        self.zi = self.pn1.hazard_map(self.hc, self.lon, self.lat, self.idarea,
                                      self.nareas, self.npts, self.ptSel, 
                                      self.staSel, self.probTh, self.intTh, 
                                      self.imgpath, self.limits, self.iml, 
                                      self.imt)
  
        self.zp = self.pn2.probability_map(self.hc, self.lon, self.lat, self.idarea,
                                           self.nareas, self.npts, self.ptSel, 
                                           self.staSel, self.probTh, self.intTh, 
                                           self.imgpath, self.limits, self.iml, 
                                           self.imt)
  
        self.hcp = self.pn3.hazard_curve(self.hc, self.ptSel, self.iml, self.imt, 
                                         self.probTh, self.intTh, self.dtau)
  
  
        #self.sb.SetStatusText("Hazard successfully loaded")
  
  
    def on_click(self, event):
        """
        1) Finding the closest point in the data grid to the point clicked 
           by the mouse on the map at the top canvas. 
        2) Updating the hazard curve plot in the bottom canvas to the 
           selected point.  
        """
        
        if (self.pn1.toolbar.mode == ""):
  
            if (event.inaxes != self.pn1.ax1): 
                return
            else:
                lon1 = min(self.lon)
                lon2 = max(self.lon)
                lat1 = min(self.lat)
                lat2 = max(self.lat)
                xsel, ysel = event.xdata, event.ydata
                if ( xsel >= lon1 and xsel <= lon2 and ysel >= lat1 and ysel <= lat2 ):
                    dist = np.sqrt( (self.lon-xsel)**2 + (self.lat-ysel)**2 )
                    self.ptSel = np.argmin(dist)
                    
                    self.zi = self.pn1.hazard_map(self.hc, self.lon, self.lat, self.idarea,
                                                  self.nareas, self.npts, self.ptSel, 
                                                  self.staSel, self.probTh, self.intTh, 
                                                  self.imgpath, self.limits, self.iml, 
                                                  self.imt)
              
                    self.zp = self.pn2.probability_map(self.hc, self.lon, self.lat, self.idarea,
                                                       self.nareas, self.npts, self.ptSel, 
                                                       self.staSel, self.probTh, self.intTh, 
                                                       self.imgpath, self.limits, self.iml, 
                                                       self.imt)
              
                    self.hcp = self.pn3.hazard_curve(self.hc, self.ptSel, self.iml, self.imt, 
                                                     self.probTh, self.intTh, self.dtau)
  
  
                                         
                    self.carea.SetValue(str(self.ptSel+1))
                  
                else:      
                    return
  
  
    def on_quit(self, event):
        """
        """
        plt.close("all")
        self.Destroy()
  
  
    def on_tab_changed(self, event):
        """
        Switching between tabs of bottom canvas
        """
        
        sel = self.nb.GetSelection()
        old = event.GetOldSelection()
        
        #if (sel == 1):
          #self.nb.ChangeSelection(old)
          #msg = ("WARNING:\nThis feature has not been implemented yet")
          #gf.show_warning_message(self, msg, "WARNING")
          #return
        
        #elif (sel == 2):
          #self.nb.ChangeSelection(old)
          #msg = ("WARNING:\nThis feature has not been implemented yet")
          #gf.show_warning_message(self, msg, "WARNING")
          #return
        
        #else:
          #pass
  
  
    def sel_abs_con_n16(self, event):
        """
        """
        if (self.rb1ac.GetValue()):
            self.selection.SetLabel("SELECTED PATH:\n" + self.sel_path)
            self.nb.DeleteAllPages()
            self.pn4 = plotlibs.pn4Canvas(self.nb)
            self.pn5 = plotlibs.pn5Canvas(self.nb)
            self.pn6 = plotlibs.pn6Canvas(self.nb)
            self.nb.AddPage(self.pn4, "ECDF")
            self.pn4.plot_absolute_prob(None, self.pa, self.pa_ave)
            condVentMapMag = (self.nodes == 4 and self.nodes_flag[1] == 0 and self.nodes_flag[3] == 0)
            condVentMapHyd = (self.nodes == 5 and self.nodes_flag[1] == 1 and self.nodes_flag[4] == 0)
            if (condVentMapMag or condVentMapHyd):
                self.nb.AddPage(self.pn5, "Vent Map")
                limitsMap = [self.xmin_map, self.xmax_map, self.ymin_map, self.ymax_map]
                pars = [self.par1, self.par2, self.par3, self.par4, self.par5]
                #pvents = np.reshape(self.p123,(len(self.p123),1))*self.p4
                self.pn5.show_map(self.pabs_ave, limitsMap, pars, self.vcx, self.vcy, 
                                 self.imgpath)
                #if (self.dip45 == 2):
                  #self.show_vent_map_abs_button(self.pabs)
                  #if (self.nodes >= 5):
                    #self.nb.AddPage(self.pn6, "Size Map")
                    #self.show_size_map_button(self.pabs)
            self.lcAbs.Show()
            self.lcCon.Hide()
            self.Layout()
                
        else:
            self.selection.SetLabel("SELECTED NODE:\n" + self.sel_node)
            self.nb.DeleteAllPages()
            self.pn4 = plotlibs.pn4Canvas(self.nb)
            self.pn5 = plotlibs.pn5Canvas(self.nb)
            self.pn6 = plotlibs.pn6Canvas(self.nb)
            #nwedges = np.shape(self.pcon)[1]
            if (self.nwedges < 2 or self.nwedges < 10):
                self.nb.AddPage(self.pn4, "Pie Chart")
                self.pn4.plot_conditional_prob(None, self.pcon, self.nodes, self.nodes_flag)
            else:
                pass
                 
            condVentMapMag = (self.nodes == 4 and self.nodes_flag[1] == 0 and self.nodes_flag[3] == 0)
            condVentMapHyd = (self.nodes == 5 and self.nodes_flag[1] == 1 and self.nodes_flag[4] == 0)
            if (condVentMapMag or condVentMapHyd):
                self.nb.AddPage(self.pn5, "Vent Map")
                limitsMap = [self.xmin_map, self.xmax_map, self.ymin_map, self.ymax_map]
                pars = [self.par1, self.par2, self.par3, self.par4, self.par5]
                self.pn5.show_map(self.pcon_ave, limitsMap, pars, self.vcx, self.vcy, self.imgpath)
            #if (self.nodes >= 5 and self.nodes_flag[3] == 0):
                #self.show_vent_map_button(self.pcon)
                #if (self.dip45 == 2):
                    #self.show_size_map_button(self.pcon)
            #if (self.staSel <= 0 or self.staSel > 100):
                #msg = ("ERROR\nInput value in percentile field is not correct")
                #gf.show_error_message(self, msg, "ERROR")
                #self.Raise()
                #return
        
            self.lcCon.Show()
            self.lcAbs.Hide()
            self.Layout()
  
        self.p1.Fit()
          
  
    def sel_abs_con_n78(self, event):
        """
        """
        if (self.rb1acN78.GetValue()):
            self.load_data(self.pabs)
            self.selection.SetLabel("SELECTED PATH:\n" + self.sel_path)
        else:
            self.load_data(self.pcon)
            self.selection.SetLabel("SELECTED NODE:\n" + self.sel_node)
  
        self.pnlLT.Fit()
  
  
    def sel_area(self, event):
        """
        """
  
        self.ptSel = int(self.carea.GetValue())
        
        self.zi = self.pn1.hazard_map(self.hc, self.lon, self.lat, self.idarea,
                                      self.nareas, self.npts, self.ptSel, 
                                      self.staSel, self.probTh, self.intTh, 
                                      self.imgpath, self.limits, self.iml, 
                                      self.imt)
  
        self.zp = self.pn2.probability_map(self.hc, self.lon, self.lat, self.idarea,
                                           self.nareas, self.npts, self.ptSel, 
                                           self.staSel, self.probTh, self.intTh, 
                                           self.imgpath, self.limits, self.iml, 
                                           self.imt)
  
        self.hcp = self.pn3.hazard_curve(self.hc, self.ptSel, self.iml, self.imt, 
                                         self.probTh, self.intTh, self.dtau)
  
  
  
  
    def sel_intensity_th(self, event):
        """
        """
  
        self.intTh = float(self.cith.GetValue())
  
        self.zi = self.pn1.hazard_map(self.hc, self.lon, self.lat, self.idarea,
                                      self.nareas, self.npts, self.ptSel, 
                                      self.staSel, self.probTh, self.intTh, 
                                      self.imgpath, self.limits, self.iml, 
                                      self.imt)
  
        self.zp = self.pn2.probability_map(self.hc, self.lon, self.lat, self.idarea,
                                           self.nareas, self.npts, self.ptSel, 
                                           self.staSel, self.probTh, self.intTh, 
                                           self.imgpath, self.limits, self.iml, 
                                           self.imt)
  
        self.hcp = self.pn3.hazard_curve(self.hc, self.ptSel, self.iml, self.imt, 
                                         self.probTh, self.intTh, self.dtau)
  
  
  
    def sel_probability_th(self, event):
        """
        """
  
        self.probTh = float(self.cpth.GetValue())
        self.zi = self.pn1.hazard_map(self.hc, self.lon, self.lat, self.idarea,
                                      self.nareas, self.npts, self.ptSel, 
                                      self.staSel, self.probTh, self.intTh, 
                                      self.imgpath, self.limits, self.iml, 
                                      self.imt)
  
        self.zp = self.pn2.probability_map(self.hc, self.lon, self.lat, self.idarea,
                                           self.nareas, self.npts, self.ptSel, 
                                           self.staSel, self.probTh, self.intTh, 
                                           self.imgpath, self.limits, self.iml, 
                                           self.imt)
  
        self.hcp = self.pn3.hazard_curve(self.hc, self.ptSel, self.iml, self.imt, 
                                         self.probTh, self.intTh, self.dtau)
  
  
    def sel_statistic(self, event):
        """
        """
  
        if (self.rb1sta.GetValue()):
          self.staSel = 0
        elif (self.rb2sta.GetValue()):
          self.staSel = int(self.cperc.GetValue())
          if (self.staSel <= 0 or self.staSel > 100):
            msg = ("ERROR\nInput value in percentile field is not correct")
            gf.show_error_message(self, msg, "ERROR")
            self.Raise()
            return
            
        else:
          msg = ("ERROR\nInput in Select Statistic is wrong")
          gf.show_error_message(self, msg, "ERROR")
          self.Raise()
          return
          
  
        self.zi = self.pn1.hazardMap(self.hc, self.lon, self.lat, self.idarea,
                                     self.nareas, self.npts, self.ptSel, 
                                     self.staSel, self.probTh, self.intTh, 
                                     self.imgpath, self.limits, self.iml, 
                                     self.imt)
  
        self.zp = self.pn2.probabilityMap(self.hc, self.lon, self.lat, self.idarea,
                                          self.nareas, self.npts, self.ptSel, 
                                          self.staSel, self.probTh, self.intTh, 
                                          self.imgpath, self.limits, self.iml, 
                                          self.imt)
  
        self.hcp = self.pn3.hazardCurve(self.hc, self.ptSel, self.iml, self.imt, 
                                        self.probTh, self.intTh, self.dtau)
  
  
  
    # NOT USED
    #def export_table(self, event, *args):
      #s1 = self.fmt_rb1.GetValue()
      #s2 = self.fmt_rb2.GetValue()
      ##s3 = str(self.fmt_rb3.GetValue())
      
      #if (s1):
        #sep = " "
        #wc = "*.txt"
        #ext = ".txt"
      #elif (s2):
        #sep = ","
        #wc = "*.csv"
        #ext = ".csv"
      #else:
        #print("error export table")  
        
      #dlg = wx.FileDialog(self, message="Save File as...", 
                          #defaultDir=self.dflDir, defaultFile="", 
                          #wildcard=wc, style=wx.SAVE|wx.FD_OVERWRITE_PROMPT)
      
      #rows = len(args[0])
      #cols = len(args[0][0])
      
      #if (dlg.ShowModal() == wx.ID_OK):
        #savepath = dlg.GetPath()
        
        #if (savepath[-4:] == ext):
          #filename = savepath
        #else:
          #filename = savepath + ext
          
        #fp = open(filename, "w")
  
        #for i in range(rows):
          #for j in range(cols):
            #if (j == cols-1):
              #fp.write("%f\n" %(args[0][i][j]))
            #else:  
              #fp.write("%f%1s" %(args[0][i][j], sep))
            
        #fp.close()
      
      #dlg.Destroy()
      
  
  
    def show_table_abs(self, *kargs):
        """
           Table                
        """
        
        pabs = kargs[0]
        pabs_ave = kargs[1]
        ilab = 0
        # label correction inverting P for binary cases
        if (self.nodes < 4 or self.nodes_flag[1] == 1):
            if (self.nodes_flag[self.nodes-1] == 1):
                ilab = 1
  
        hrow=[]
        if (self.nodes == 1):
            label =  ["Unrest", "No Unrest"]
            header_list = ("", label[ilab])
            hrow.append("Average")
            hrow.append("10th Perc")
            hrow.append("50th Perc")
            hrow.append("90th Perc")
            values = np.array([pabs_ave,
                               np.percentile(pabs,10),
                               np.percentile(pabs,50),
                               np.percentile(pabs,90)])
            ncols = 1
            nrows = len(values)
            nwedges = ncols
  
        elif (self.nodes == 2):
            label = ["Magmatic", "No Magmatic"]
            header_list = ("", label[ilab])
            hrow.append("Average")
            hrow.append("10th Perc")
            hrow.append("50th Perc")
            hrow.append("90th Perc")
            values = np.array([pabs_ave,
                               np.percentile(pabs,10),
                               np.percentile(pabs,50),
                               np.percentile(pabs,90)])
            ncols = 1
            nrows = len(values)
            nwedges = ncols
  
        elif (self.nodes == 3):
            if (self.nodes_flag[1] == 0):
                label = ["Eruption", "No Eruption"]
                header_list = ("", label[ilab])
                hrow.append("Average")
                hrow.append("10th Perc")
                hrow.append("50th Perc")
                hrow.append("90th Perc")
                values = np.array([pabs_ave,
                                   np.percentile(pabs,10),
                                   np.percentile(pabs,50),
                                   np.percentile(pabs,90)])
                ncols = 1
                nrows = len(values)
                nwedges = ncols
            else:
                label = ["Hydrothermal Unrest", "Tectonic Unrest"]
                header_list = ("", label[ilab])
                hrow.append("Average")
                hrow.append("10th Perc")
                hrow.append("50th Perc")
                hrow.append("90th Perc")
                values = np.array([pabs_ave,
                                   np.percentile(pabs,10),
                                   np.percentile(pabs,50),
                                   np.percentile(pabs,90)])
                ncols = 1
                nrows = len(values)
                nwedges = ncols
  
        elif (self.nodes == 4):
            if (self.nodes_flag[1] == 0):
                header_list = ("", "Average", "10th Perc", "50th Perc", "90th Perc")
                values = np.array([ pabs_ave,
                                    np.percentile(pabs,10,axis=0),
                                    np.percentile(pabs,50,axis=0),
                                    np.percentile(pabs,90,axis=0) ])
                ncols, nrows = np.shape(values)
                nwedges = nrows
                
                if (self.nodes_flag[3] == 0):
                    for i in range(nrows):
                        hrow.append("Vent " + str(i + 1))
                else:
                    hrow.append("Vent " + str(self.nodes_flag[3]))
  
            else:
                label = ["Hydrothermal Eruption", "No Hydrothermal Eruption"]
                header_list = ("", label[ilab])
                hrow.append("Average")
                hrow.append("10th Perc")
                hrow.append("50th Perc")
                hrow.append("90th Perc")
                values = np.array([pabs_ave,
                                   np.percentile(pabs,10),
                                   np.percentile(pabs,50),
                                   np.percentile(pabs,90)])
                ncols = 1
                nrows = len(values)
                nwedges = ncols
  
        elif (self.nodes == 5):
            if (self.nodes_flag[1] == 0):
                if (int(self.nodes_flag[4])%2==0):
                    tmp = int(self.nodes_flag[4])/2 - 1
                    ind5 = range(tmp,self.nsizes) 
                else:
                    ind5 = [int(self.nodes_flag[4]+1)/2 - 1]
      
                if (self.nodes_flag[3] == 0):
                    tmp = np.zeros((self.sample,len(ind5)))
                    tmp_ave = np.zeros((len(ind5)))
                    for i in range(len(ind5)):
                        tmp[:,i] = np.sum(pabs[:,i:-1:len(ind5)], axis=1) 
                        tmp_ave[i] = np.sum(pabs_ave[i:-1:len(ind5)]) 
                else:
                    tmp = pabs
                    tmp_ave = pabs_ave
      
                values = np.array([ tmp_ave,
                                    np.percentile(tmp,10,axis=0),
                                    np.percentile(tmp,50,axis=0),
                                    np.percentile(tmp,90,axis=0) ])
      
                ncols, nrows = np.shape(values)
                header_list = ("", "Average", "10th Perc", "50th Perc", "90th Perc")
                for i in ind5:
                    hrow.append("Size " + str(i+1))
      
                nwedges = nrows
  
            else:
                header_list = ("", "Average", "10th Perc", "50th Perc", "90th Perc")
                values = np.array([ pabs_ave,
                                    np.percentile(pabs,10,axis=0),
                                    np.percentile(pabs,50,axis=0),
                                    np.percentile(pabs,90,axis=0) ])
                ncols, nrows = np.shape(values)
                nwedges = nrows
                
                if (self.nodes_flag[4] == 0):
                    for i in range(nrows):
                        hrow.append("Vent " + str(i + 1))
                else:
                    hrow.append("Vent " + str(self.nodes_flag[4]))
  
  
        elif (self.nodes == 6):
            if (self.nodes_flag[1] == 0):
                pass
            else:
                label = ["Effusive", "Explosive"]
                header_list = ("", label[ilab])
                hrow.append("Average")
                hrow.append("10th Perc")
                hrow.append("50th Perc")
                hrow.append("90th Perc")
                values = np.array([np.sum(pabs_ave),
                                   np.percentile(np.sum(pabs, axis=1),10),
                                   np.percentile(np.sum(pabs, axis=1),50),
                                   np.percentile(np.sum(pabs, axis=1),90)])
                ncols = 1
                nrows = len(values)
                nwedges = ncols
  
  
        else:
            print("Error in show_table_abs")
  
  
        self.lcAbs = wx.ListCtrl(self.p1, wx.ID_ANY, style=wx.LC_REPORT, size=(-1,-1))
        context = []
        tmp_list = []
        for i in range(ncols+1):
            self.lcAbs.InsertColumn(i, header_list[i])
        for i in range(nrows):
            # self.lcAbs.InsertStringItem(i, hrow[i])
            self.lcAbs.InsertItem(i, hrow[i])
            for j in range(ncols):
                if (self.nodes <= 3 or (self.nodes_flag[1]==1 and self.nodes == 4 ) or self.nodes == 6):
                    # self.lcAbs.SetStringItem(i, j+1, "{0:.3e}".format(values[i]))
                    self.lcAbs.SetItem(i, j+1, "{0:.3e}".format(values[i]))
                    tmp_list.append(values[i]) 
                else:
                    # self.lcAbs.SetStringItem(i, j+1, "{0:.3e}".format(values[j,i]))
                    self.lcAbs.SetItem(i, j+1, "{0:.3e}".format(values[j,i]))
                    tmp_list.append(values[j,i]) 
  
            context.append(tmp_list)
            tmp_list = []
  
  
        self.vbox1.Add(self.lcAbs, 0, wx.ALL|wx.EXPAND, 5)
        
        return nwedges
  
  
    def show_table_con(self, *kargs):
        """
           Table                
        """
  
        pcon = kargs[0]
        pcon_ave = kargs[1]
        # label correction inverting P for binary cases
        if (self.nodes < 4 or self.nodes_flag[1] == 1):
            if (self.nodes_flag[self.nodes-1] == 1):
                pcon = 1.0-pcon
  
        hrow=[]
  
        if (self.nodes == 1):
            header_list = ("", "Unrest", "No Unrest")
            hrow.append("Average")
            hrow.append("10th Perc")
            hrow.append("50th Perc")
            hrow.append("90th Perc")
            values = np.array([pcon_ave,
                               np.percentile(pcon,10),
                               np.percentile(pcon,50),
                               np.percentile(pcon,90)])
            ncols = 1
            nrows = len(values)
            nwedges = ncols
  
        elif (self.nodes == 2):
            header_list = ("", "Magmatic", "No Magmatic")
            hrow.append("Average")
            hrow.append("10th Perc")
            hrow.append("50th Perc")
            hrow.append("90th Perc")
            values = np.array([pcon_ave,
                               np.percentile(pcon,10),
                               np.percentile(pcon,50),
                               np.percentile(pcon,90)])
            ncols = 1
            nrows = len(values)
            nwedges = ncols
  
        elif (self.nodes == 3):
            if (self.nodes_flag[1] == 0):
                header_list = ("", "Eruption", "No Eruption")
                hrow.append("Average")
                hrow.append("10th Perc")
                hrow.append("50th Perc")
                hrow.append("90th Perc")
                values = np.array([pcon_ave,
                                   np.percentile(pcon,10),
                                   np.percentile(pcon,50),
                                   np.percentile(pcon,90)])
                ncols = 1
                nrows = len(values)
                nwedges = ncols
            else:
                header_list = ("", "Hydrothermal", "Tectonic")
                hrow.append("Average")
                hrow.append("10th Perc")
                hrow.append("50th Perc")
                hrow.append("90th Perc")
                values = np.array([pcon_ave,
                                   np.percentile(pcon,10),
                                   np.percentile(pcon,50),
                                   np.percentile(pcon,90)])
                ncols = 1
                nrows = len(values)
                nwedges = ncols
  
  
        elif (self.nodes == 4):
            if (self.nodes_flag[1] == 0):
                values = np.array([ pcon_ave,
                                    np.percentile(pcon,10,axis=0),
                                    np.percentile(pcon,50,axis=0),
                                    np.percentile(pcon,90,axis=0) ])
                ncols, nrows = np.shape(values)
                header_list = ("", "Average", "10th Perc", "50th Perc", "90th Perc")
                nwedges = nrows
                for i in range(nrows):
                    hrow.append("Vent" + " " + str(i + 1))
  
            else:
                header_list = ("", "Eruption", "No Eruption")
                hrow.append("Average")
                hrow.append("10th Perc")
                hrow.append("50th Perc")
                hrow.append("90th Perc")
                values = np.array([pcon_ave,
                                   np.percentile(pcon,10),
                                   np.percentile(pcon,50),
                                   np.percentile(pcon,90)])
                ncols = 1
                nrows = len(values)
                nwedges = ncols
  
        elif (self.nodes == 5):
            if (self.nodes_flag[1] == 0):
                values = np.array([ pcon_ave,
                                    np.percentile(pcon,10,axis=0),
                                    np.percentile(pcon,50,axis=0),
                                    np.percentile(pcon,90,axis=0) ])
                
                ncols, nrows = np.shape(values)
                header_list = ("", "Average", "10th Perc", "50th Perc", "90th Perc")
                nwedges = nrows
                for i in range(nrows):
                    hrow.append("Size" + " " + str(i + 1))
  
            else:
                values = np.array([ pcon_ave,
                                    np.percentile(pcon,10,axis=0),
                                    np.percentile(pcon,50,axis=0),
                                    np.percentile(pcon,90,axis=0) ])
                ncols, nrows = np.shape(values)
                header_list = ("", "Average", "10th Perc", "50th Perc", "90th Perc")
                nwedges = nrows
                for i in range(nrows):
                    hrow.append("Vent" + " " + str(i + 1))
  
        elif (self.nodes == 6):
            if (self.nodes_flag[1] == 0):
                pass
            else:
                header_list = ("", "Effusive", "Explosive")
                hrow.append("Average")
                hrow.append("10th Perc")
                hrow.append("50th Perc")
                hrow.append("90th Perc")
                values = np.array([pcon_ave,
                                   np.percentile(pcon,10),
                                   np.percentile(pcon,50),
                                   np.percentile(pcon,90)])
                ncols = 1
                nrows = len(values)
                nwedges = ncols
            
  
        else:
            print("Error in show_table_con")
  
  
        self.lcCon = wx.ListCtrl(self.p1, wx.ID_ANY, style=wx.LC_REPORT, size=(-1,-1))
        context = []
        tmp_list = []
        for i in range(ncols+1):
            self.lcCon.InsertColumn(i, header_list[i])
        for i in range(nrows):
            # self.lcCon.InsertStringItem(i, hrow[i])
            self.lcCon.InsertItem(i, hrow[i])
            for j in range(ncols):
                if (self.nodes <= 3 or (self.nodes_flag[1]==1 and self.nodes == 4 ) or self.nodes == 6):
                    # self.lcCon.SetStringItem(i, j+1, "{0:.3e}".format(values[i]))
                    self.lcCon.SetItem(i, j+1, "{0:.3e}".format(values[i]))
                    tmp_list.append(values[i]) 
                else:
                    # self.lcCon.SetStringItem(i, j+1, "{0:.3e}".format(values[j,i]))
                    self.lcCon.SetItem(i, j+1, "{0:.3e}".format(values[j,i]))
                    tmp_list.append(values[j,i]) 
  
            context.append(tmp_list)
            tmp_list = []
  
  
        self.vbox1.Add(self.lcCon, 0, wx.ALL|wx.EXPAND, 5)
        return nwedges

