#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 

This file is part of pyBetVH.

"""

#import ConfigParser
import configparser
import os
import sys
#import urllib2
import urllib.request, urllib.error, urllib.parse
import wx
import numpy as np

## global variables
#dflDir = os.path.expanduser("~")
#workDir = os.path.dirname(os.path.realpath(__file__))[:-3]

  

def set_dirs():
    """
    """

    dflDir = os.path.expanduser("~")
    workDir = os.path.dirname(os.path.realpath(__file__))
    localDir = os.path.join(dflDir,".betvh")
    if not os.path.exists(localDir):
        os.makedirs(localDir)
        # os.makedirs(os.path.join(localDir, "volcList"))


    return dflDir, workDir, localDir


def read_main_settings(pvhapath):
    """
    """

    # config = ConfigParser.RawConfigParser()
    config = configparser.RawConfigParser()
    filecfg = os.path.join(pvhapath, "pybet.cfg")
    config.read(filecfg)
    vname = config.get("Main Settings", "Volcano Name")
    vc = config.get("Main Settings", "Volcano Center")
    shape = config.get("Main Settings", "Shape")
    geom = config.get("Main Settings", "Geometry")
    utm = config.get("Main Settings", "UTM Zone")
    tw = config.getfloat("Main Settings", "Time Window")
    sp = config.getint("Main Settings", "Sampling")
    bg = config.get("Main Settings", "Background Image")
    bg_lims = config.get("Main Settings", "Map Limits (m UTM)")
    mfile = config.get("Main Settings", "Monitoring")
    anpars = config.get("Main Settings", "Anomaly Function Parameters").split(",")
    a = float(anpars[0])
    b = float(anpars[1])
    l = float(anpars[2])

    return vname, vc, shape, geom, utm, tw, sp, bg, bg_lims, mfile, a, b, l


def read_node123(pvhapath, node):
    """
    """

    # config = ConfigParser.RawConfigParser()
    config = configparser.RawConfigParser()
    filecfg = os.path.join(pvhapath,"pybet.cfg")
    config.read(filecfg)
    p = config.getfloat(node, "Prior probability")
    l = config.getint(node, "Equivalent N. Data (Lambda)")
    pds = config.getint(node, "Past Data (Successes)")
    pdt = config.getint(node, "Past Data (Total)")

    return p, l, pds, pdt
  

def read_node4(pvhapath, node):
    """
    """

    # config = ConfigParser.RawConfigParser()
    config = configparser.RawConfigParser()
    filecfg = os.path.join(pvhapath,"pybet.cfg")
    config.read(filecfg)
    f = config.get(node, "File Name")
    l = config.getint(node, "Equivalent N. Data (Lambda)")
    m = config.get(node, "File Name Monitoring")

    return f, l, m
  

def read_node5(pvhapath):
    """
    """

    # config = ConfigParser.RawConfigParser()
    config = configparser.RawConfigParser()
    filecfg = os.path.join(pvhapath,"pybet.cfg")
    config.read(filecfg)
    d45 = config.getboolean("Node Magmatic Style", "Node 4-5 Dependence")
    nsizes = config.getint("Node Magmatic Style", "N. Sizes")
    f = config.get("Node Magmatic Style", "File Name")

    return d45, nsizes, f
  

def read_node6(pvhapath):
    """
    """

    # config = ConfigParser.RawConfigParser()
    config = configparser.RawConfigParser()
    filecfg = os.path.join(pvhapath,"pybet.cfg")
    config.read(filecfg)
    nout = config.getint("Node 6", "N. Outcomes")
    outcomes = config.get("Node 6", "Outcomes")
    units = config.get("Node 6", "Units")
    na = config.get("Node 6", "N. Areas")
    f1 = config.get("Node 6", "File Name")
    f2 = config.get("Node 6", "File Intensities")
    f3 = config.get("Node 6", "File Points-Areas")

    return nout, outcomes, units, na, f1, f2, f3
  

def read_node78(pvhapath):
    """
    """

    # config = ConfigParser.RawConfigParser()
    config = configparser.RawConfigParser()
    filecfg = os.path.join(pvhapath,"pybet.cfg")
    config.read(filecfg)
    f1 = config.get("Node 78", "File Name Prior")
    f2 = config.get("Node 78", "File Name Past Data")

    return f1, f2


def read_monitoring(pvhapath):
    """
    """

    # config = ConfigParser.RawConfigParser()
    config = configparser.RawConfigParser()
    filecfg = os.path.join(pvhapath)
    config.read(filecfg)
    sections = config.sections()

    monitoringPars = {}
    name = {}
    val = {}
    th1 = {}
    th2 = {}
    rel = {}
    wei = {}

    ic = 0
    for sec in sections:
        tmp = sec.split(" - ")
        if (int(sec[-2:]) == 1):
            name[tmp[0]] = []
            val[tmp[0]] = []
            th1[tmp[0]] = []
            th2[tmp[0]] = []
            rel[tmp[0]] = []
            wei[tmp[0]] = []

        name[tmp[0]].append(config.get(sec, "Name"))
        val[tmp[0]].append( np.nan_to_num(config.getfloat(sec, "Value")) )
        th1[tmp[0]].append(config.getfloat(sec, "Threshold 1"))

        th2tmp = config.get(sec, "Threshold 2")
        if (th2tmp == "None" or th2tmp == "saturated"):
            th2[tmp[0]].append(th2tmp)
        else:
            th2[tmp[0]].append(float(th2tmp))

        rel[tmp[0]].append(config.get(sec, "Relation"))
        wei[tmp[0]].append(config.getfloat(sec, "Weight"))

    return name, val, th1, th2, rel, wei  


def sel_dir(self, event):
    """
    Open a dialog to select a directory path
    """
    dfl_dir = os.path.expanduser("~")
    dlg = wx.DirDialog(self, "Select a directory:", defaultPath=dfl_dir,
                     style=wx.DD_DEFAULT_STYLE
                     #| wx.DD_DIR_MUST_EXIST
                     #| wx.DD_CHANGE_DIR
                     )
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()
    else:
        msg = "WARNING\nYou have NOT selected any directory"
        show_warning_message(self, msg, "WARNING")
        path = ""

    dlg.Destroy()
    return path


def sel_file(self, event, *kargs):
    """
    upload_file
    It opens a file dialog, it opens the selected file and
    it returns the corresponding path  
    """

    dfl_dir = os.path.expanduser("~")
    dlg = wx.FileDialog(self, message="Upload File", defaultDir=dfl_dir, 
                      defaultFile="", wildcard="*.*", 
                      style=wx.FD_OPEN|wx.FD_CHANGE_DIR)

    if (dlg.ShowModal() == wx.ID_OK):
        path = dlg.GetPath()
    else:
        msg = "WARNING\nYou have NOT selected any file"
        show_warning_message(self, msg, "WARNING")
        path = ""

    dlg.Destroy()
    return path
  

def verify_internet_conn():
    try:
        #response = urllib2.urlopen("http://maps.google.com/maps", timeout=3)
        response = urllib.request.urlopen("http://maps.google.com/maps", timeout=3)
        return True
    # except urllib2.URLError as err: pass
    except urllib.error.URLError as err: pass
    return False 


def show_warning_message(self, *kargs):
    """
    It opens a pop-up dialog showing a warning message.
    """

    dlg = wx.MessageDialog(self, kargs[0], kargs[1], wx.OK|wx.ICON_WARNING)
    dlg.ShowModal()
    dlg.Destroy()


def show_error_message(self, *kargs):
    """
    It opens a pop-up dialog showing an error message.
    """

    dlg = wx.MessageDialog(self, kargs[0], kargs[1], wx.OK|wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy()





def check_mods():
    """
    """
    
  
    wxMissingMsg = """
      ERROR! wxPython module is not installed!
      
      Installation:
      
      Linux
      Most of distributions have their pre-compiled package, so you can 
      easily install it from your preferred package manager. The package 
      name is usually python-wxgtk2.8 (debian-based) or wxpython (redhat-
      based). 
      
      Windows and Mac OSX
      Binaries can be downloaded from http://www.wxpython.org/ in the 
      download area (stable version).
      
      Source code
      In case you need to build it from source code you can follow this 
      http://www.wxpython.org/BUILD-2.8.html
      
      """
    
    npMissingMsg = """
      ERROR! numPy module is not installed!
      
      Installation:
      
      Linux
      Most of distributions have their pre-compiled package, so you can 
      easily install it from your preferred package manager. The package 
      name is usually python-numpy or just numpy. 
      
      Windows and Mac OSX
      Binaries can be downloaded from http://sourceforge.net/projects/numpy/ 
      
      """
    
    mplotMissingMsg = """
      ERROR! Matplotlib module is not installed!
      
      Installation:
      
      Linux
      Most of distributions have their pre-compiled package, so you can 
      easily install it from your preferred package manager. The package 
      name is usually python-matplotlib or just matplotlib. 
      
      Windows and Mac OSX
      Binaries can be downloaded from 
      http://sourceforge.net/projects/matplotlib/files/matplotlib/ 
      """
      
    sciMissingMsg = """
      ERROR! SciPy module is not installed!
      
      Installation:
      
      Linux
      Most of distributions have their pre-compiled package, so you can 
      easily install it from your preferred package manager. The package 
      name is usually python-scipy or just scipy. 
      
      Windows and Mac OSX
      Binaries can be downloaded from 
      http://sourceforge.net/projects/scipy/files/ 
      """
    
    try:
        import numpy
    except ImportError:
        sys.exit(npMissingMsg)
    
    try:
        import wx
    except ImportError:
        sys.exit(wxMissingMsg)
    
    try:
        import matplotlib
    except ImportError:
        sys.exit(mplotMissingMsg)
    
    try:
        import scipy
    except ImportError:
        sys.exit(sciMissingMsg)
    
    return True
