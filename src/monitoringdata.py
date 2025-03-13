#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 

This file is part of pyBetVH.

"""

#import ConfigParser
import configparser
import os
import shutil
import string
import sys
import wx
import wx.lib.mixins.listctrl  as  listmix


class MyFrame(wx.Frame):
    """
    """
   
    def __init__(self, nPars, nodeNames):
        """
        """
        wx.Frame.__init__(self, None, wx.ID_ANY, "Editable List Control")
        
        iParTot = 0
        self.nodes = []
        self.parameters = []
        self.values = []
        self.thresholds1 = []
        self.thresholds2 = []
        self.relations = []
        for inode in range(len(nPars)):
            if (nPars[inode] != 0):
                for ipar in range(nPars[inode]):
                    section = nodeNames[inode] + ' - Parameter ' + str(iParTot+1)
                    self.nodes.append(nodeNames[inode])
                    self.parameters.append("Parameter Name")
                    self.values.append("0")
                    self.thresholds1.append("0")
                    self.thresholds2.append("0")
                    self.relations.append("")
                    iParTot += 1
  
  
        self.list_ctrl = EditableListCtrl(self, style=wx.LC_REPORT)
  
        self.list_ctrl.InsertColumn(0, "Level")
        self.list_ctrl.InsertColumn(1, "Parameter")
        self.list_ctrl.InsertColumn(2, "Value")
        self.list_ctrl.InsertColumn(3, "Threshold 1")
        self.list_ctrl.InsertColumn(4, "Threshold 2")
        self.list_ctrl.InsertColumn(5, "Relation")
  
        for i in range(iParTot):
            self.list_ctrl.InsertStringItem(i, self.nodes[i])
            self.list_ctrl.SetStringItem(i, 1, self.parameters[i])
            self.list_ctrl.SetStringItem(i, 2, self.values[i])
            self.list_ctrl.SetStringItem(i, 3, self.thresholds1[i])
            self.list_ctrl.SetStringItem(i, 4, self.thresholds2[i])
            self.list_ctrl.SetStringItem(i, 5, self.relations[i])
  
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 0, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)
        self.Fit()
        self.Centre()
        self.Layout()
        self.Raise()
        self.Show(True)
     

class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):
    ''' TextEditMixin allows any column to be edited. '''
  
    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,
                   size=wx.DefaultSize, style=0):
        """Constructor"""
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)



# CLASS InsertMonitoring
class InsertMonitoring(wx.Frame):

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition)
  
        
        self.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, 
                            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
  
        self.vbox = wx.BoxSizer(orient=wx.VERTICAL)
  
  
        hboxN0 = wx.BoxSizer(wx.HORIZONTAL)
        txt1N0 = wx.StaticText(self, wx.ID_ANY, "Nodes", size=(140,-1))
        txt1N0.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, 
                               wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        hboxN0.Add(txt1N0, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.EXPAND, 10)
  
        txt2N0 = wx.StaticText(self, wx.ID_ANY, "N. Parameters", 
                   size=(-1,-1))
        txt2N0.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, 
                               wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        hboxN0.Add(txt2N0, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 10)
        self.vbox.Add(hboxN0, 0, wx.EXPAND|wx.ALL, 5)
  
  
        self.nodeNames = ["Unrest", "Magmatic", "Magmatic Eruption", 
                          "Hydrothermal", "Hydrothermal Eruption", 
                          "Hydrothermal Eruption Size"]        
  
        for n in range(len(self.nodeNames)):
            hboxNode = wx.BoxSizer(wx.HORIZONTAL)
            hboxNode.Add(wx.StaticText(self, wx.ID_ANY, self.nodeNames[n], 
                         size=(200,-1)), 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 10)
      
            self.nParsNodes = wx.TextCtrl(self, wx.ID_ANY, size=(30,-1), 
                                          name=self.nodeNames[n])
            self.nParsNodes.SetValue("0")
            hboxNode.Add(self.nParsNodes, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 0)
            self.vbox.Add(hboxNode, 0, wx.EXPAND|wx.TOP, 5)
  
  
        hboxSub = wx.BoxSizer(wx.HORIZONTAL)
        self.bSub = wx.Button(self, wx.ID_ANY, 
                                name="Save", label="Save")
        self.Bind(wx.EVT_BUTTON, self.subMonData, self.bSub)
        hboxSub.Add(self.bSub, 0, wx.ALIGN_BOTTOM|wx.TOP|wx.LEFT, 5)
        self.vbox.Add(hboxSub, 0, wx.EXPAND|wx.TOP, 15)
  
        #self.fr.Bind(wx.EVT_CLOSE, self.closeInputFr)
        self.SetSizer(self.vbox)
        self.SetSize((680,420))
        self.Fit()
        self.Centre()
        self.Layout()
        self.Raise()
        self.Show(True)


    def subMonData(self, event):
        """
        """
        txtCtrls = [w for w in self.GetChildren() if isinstance(w, wx.TextCtrl)]
        nPars = []
        for ctrl in txtCtrls:
            nPars.append(int(ctrl.GetValue()))
          
        
        #config = ConfigParser.RawConfigParser()
        config = configparser.RawConfigParser()
        iParTot = 0
        for inode in range(len(self.nodeNames)):
            if (nPars[inode] != 0):
                for ipar in range(nPars[inode]):
                    section = self.nodeNames[inode] + ' - Parameter ' + str(ipar+1)
                    config.add_section(section)
                    #config.set(section, 'Node', )
                    config.set(section, 'Name')
                    config.set(section, 'Value', '0')
                    config.set(section, 'Threshold 1')
                    config.set(section, 'Threshold 2')
                    config.set(section, 'Relation')
                    config.set(section, 'Weight', '1')
                    iParTot += 1
          
        # Writing our configuration file to 'example.cfg'
        with open('../test/pybet_monitoring.cfg', 'wb') as configfile:
            config.write(configfile)
        
        #frame = MyFrame(nPars, self.nodeNames)
  
        
        self.Close()
    

