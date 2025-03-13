#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 

This file is part of pyBetVH.

"""

import math
import random
import sys
import wx
import numpy as np
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCv
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavTb
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
mpl.rcParams["font.family"]="serif"
mpl.rcParams["font.sans-serif"]="Times"

class pn1Canvas(wx.Panel):
    """
    
    """
    
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
  
        vbox = wx.BoxSizer(orient=wx.VERTICAL)
        #hbox_top = wx.BoxSizer(orient=wx.HORIZONTAL)
  
        self.fig = plt.figure()
        self.canvas = FigCv(self, -1, self.fig)
        self.toolbar = NavTb(self.canvas)
        #self.toolbar.Disable()
  
        self.fig.clf()
        #self.axes = self.fig.add_axes([0.1,0.1,0.85,0.85])
  
  
        self.fig.subplots_adjust(left=None, bottom=None, right=None, top=None, 
                                 wspace=None, hspace=0.3)
        # self.fig.hold(True)
  
        self.canvas.SetSize(self.GetSize())
        self.canvas.draw()
        
        #self.chpoints = wx.CheckBox(self, -1, "Show Points", (-1, -1))
        #wx.EVT_CHECKBOX(self, self.chpoints.GetId(), self.show_points)
        #self.chareas = wx.CheckBox(self, -1, "Show Areas", (-1, -1))
        #wx.EVT_CHECKBOX(self, self.chareas.GetId(), self.show_areas)
        #self.chpoints.Disable()
        #self.chareas.Disable()
        #hbox_top.Add(self.chpoints, 0, wx.ALL, 5)
        #hbox_top.Add(self.chareas, 0, wx.ALL, 5)
  
        #vbox.Add(hbox_top, 0, wx.EXPAND|wx.ALL, 0)
        vbox.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 0)
        vbox.Add(self.toolbar, 0, wx.EXPAND|wx.ALL, 0)
  
        self.SetSizer(vbox)
  
   
    def hazard_map(self, *kargs):
        """
        Loading map ...
        """
        
        hc = kargs[0]             # volcanic hazard
        self.xx = kargs[1]        # x coord of each point
        self.yy = kargs[2]        # y coord of each point
        ida = kargs[3]            # id area for each point
        na = kargs[4]             # nareas
        npt = kargs[5]            # n. point
        ptsel = kargs[6]          # selected area
        stsel = kargs[7]          # selected statistic
        pth = kargs[8]            # probability threshold
        ith = kargs[9]            # intensity threshold
        imgfile = kargs[10]
        xmap1, xmap2, ymap1, ymap2 = kargs[11]
        iml = kargs[12]
        imt = kargs[13]
        
        nx = 100
        ny = 100
        self.xmin = min(self.xx)
        self.xmax = max(self.xx)
        self.ymin = min(self.yy)
        self.ymax = max(self.yy)
        
        z = [0]*npt
        
        if (stsel == 0):
            hcsel = np.mean(hc, axis=2)
        else:
            hcsel = np.percentile(hc, stsel, axis=2)
        
        for i in range(npt):
            curve = hcsel[i,:]
            # finding intensity value corresponding to probability threshold (pth)
            if (pth < curve[0] and pth > curve[-1] ):
                for j in range(len(curve)):
                    if (curve[j] < pth):
                        interp = (iml[j]-iml[j-1]) * (pth-curve[j-1]) / (curve[j]-curve[j-1])
                        z[i] = iml[j-1] + interp 
                        break
            elif (pth >= curve[0]):
                z[i] = 0
            elif (pth <= curve[-1]):
                z[i] = iml[-1]
            else:
                pass
        
  
        xv = np.linspace(self.xmin, self.xmax, nx)
        yv = np.linspace(self.ymin, self.ymax, ny)
        xg, yg = np.meshgrid(xv, yv)
        zg = mlab.griddata(self.xx, self.yy, z, xg, yg)  
  
        cmap = plt.cm.RdYlGn_r
        cmaplist = [cmap(i) for i in range(cmap.N)]
        dcmap = cmap.from_list("Custom cmap", cmaplist, cmap.N)
  
  #      bounds = np.linspace(gf.floatFloor(min(z)), gf.floatCeil(max(z)), 11)
        bounds = np.linspace(np.amin(zg), np.amax(zg), 9)
        bounds = bounds[1:]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
  
        self.fig.clf()
        # self.fig.hold(True)
        self.ax1 = self.fig.add_subplot(1, 1, 1)
  
        img = plt.imread(imgfile)
        self.ax1.imshow(img, origin="upper", extent=(xmap1, xmap2, ymap1, ymap2))
        
        self.map1 = self.ax1.contourf(xg, yg, zg, bounds, origin="lower",
                                      cmap=plt.cm.RdYlGn_r, alpha=0.8)
        #self.map1 = self.ax1.imshow(zg, origin="lower", aspect="equal", vmin=bounds[0], 
                                    #vmax=bounds[-1], cmap=plt.cm.RdYlGn_r, alpha=0.7, 
                                    #extent=(self.xmin, self.xmax, self.ymin, self.ymax),
                                    #interpolation="nearest")
        self.map2 = self.ax1.contour(xg, yg, zg, bounds, origin="lower",
                                     aspect="equal", cmap=plt.cm.RdYlGn_r, linewidths=2,
                                     alpha=1.0)
        plt.clabel(self.map2, inline=1, fontsize=10, fmt="%.2E", colors="#000000")
        self.ax1.plot(self.xx[ptsel], self.yy[ptsel], linewidth=0, marker="o", 
                      markerfacecolor="magenta")                        
  
        #self.cb1 = self.fig.colorbar(self.map1, shrink=0.8, norm=norm, ticks=bounds, 
                                     #boundaries=bounds, format="%.3f")
        self.cb1 = self.fig.colorbar(self.map1, shrink=0.8, orientation="vertical", format="%.2E")
        self.cb1.set_alpha(1)
        self.cb1.set_label(imt)
        self.cb1.draw_all()
  
        self.ax1.set_title("Hazard Map\n", fontsize=9)
        self.ax1.set_xlabel("Easting (km)")
        self.ax1.set_ylabel("Northing (km)")
        self.ax1.axis([xmap1, xmap2, ymap1, ymap2])
  
        self.canvas.draw()
        self.canvas.mpl_connect("motion_notify_event", self.update_mouse_sel)
        self.Layout()
  
        return z
  
  
    def update_mouse_sel(self, event):
  
        if (event.inaxes != self.ax1): 
            return
        else:
            xsel, ysel = event.xdata, event.ydata
            if ( xsel >= self.xmin and xsel <= self.xmax and 
                 ysel >= self.ymin and ysel <= self.ymax ):

                dist = np.sqrt( (self.xx-xsel)**2 + (self.yy-ysel)**2 )
                i = np.argmin(dist) + 1
                x = self.xx[i]
                y = self.yy[i]
                tt = "Hazard Map\nPoint n. %s, Lon = %8.3f km, Lat = %8.3f km" %(i, x, y)
                # tt = "Point n. {:}, Lon = {:f8.3} km,  Lat = {:f8.3} km".format(i,x,y)
                # self.ax1.set_title(tt, fontsize=9)
                self.canvas.draw()
            else:
                tt = "Hazard Map\nOut of data points bounds"
                # self.ax1.set_title(tt, fontsize=9)
                self.canvas.draw()



class pn2Canvas(wx.Panel):
    """
    
    """
    
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
  
        vbox = wx.BoxSizer(orient=wx.VERTICAL)
        self.fig = plt.figure()
        self.canvas = FigCv(self, -1, self.fig)
        self.toolbar = NavTb(self.canvas)
        #self.toolbar.Disable()
  
        self.fig.clf()
        self.fig.subplots_adjust(left=None, bottom=None, right=None, top=None, 
                                 wspace=None, hspace=0.3)
        # self.fig.hold(True)
        self.canvas.SetSize(self.GetSize())
        self.canvas.draw()
        vbox.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 0)
        vbox.Add(self.toolbar, 0, wx.EXPAND|wx.ALL, 0)
        self.SetSizer(vbox)
  
   
    def probability_map(self, *kargs):
        """
        Loading Probability Map ...
        """
        
        hc = kargs[0]             # volcanic hazard
        self.xx = kargs[1]        # x coord of each point
        self.yy = kargs[2]        # y coord of each point
        aa = kargs[3]             # id area for each point
        na = kargs[4]             # nareas
        npt = kargs[5]            # n. point
        ptsel = kargs[6]          # selected area
        stsel = kargs[7]          # selected statistic
        pth = kargs[8]            # probability threshold
        ith = kargs[9]            # intensity threshold
        imgfile = kargs[10]
        xmap1, xmap2, ymap1, ymap2 = kargs[11]
        iml = kargs[12]
        imt = kargs[13]
        
        nx = 100
        ny = 100
        self.xmin = min(self.xx)
        self.xmax = max(self.xx)
        self.ymin = min(self.yy)
        self.ymax = max(self.yy)
        
        zp = [0]*npt
  
        if (stsel == 0):
            hcsel = np.mean(hc, axis=2)
        else:
            hcsel = np.percentile(hc, stsel, axis=2)
  
        for i in range(npt):
            curve = hcsel[i,:]
            # finding probability value corresponding to intensity threshold (ith)
            if (ith < iml[-1] and ith > iml[0] ):
                zp[i] = np.interp(ith, iml, curve)
            elif (ith >= iml[-1]):
                zp[i] = curve[-1]
            elif (ith <= iml[0]):
                zp[i] = curve[0]
            else:
                pass
  
  
        xv = np.linspace(self.xmin, self.xmax, nx)
        yv = np.linspace(self.ymin, self.ymax, ny)
        xg, yg = np.meshgrid(xv, yv)
        zgp = mlab.griddata(self.xx, self.yy, zp, xg, yg)  
  
        cmap = plt.cm.RdYlGn_r
        cmaplist = [cmap(i) for i in range(cmap.N)]
        dcmap = cmap.from_list("Custom cmap", cmaplist, cmap.N)
  
        #bounds = np.linspace(gf.floatFloor(np.amin(zgp)), gf.floatCeil(np.amax(zgp)), 11)
        bounds = np.linspace(np.amin(zgp), np.amax(zgp), 9)
        bounds = bounds[1:]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
  
        self.fig.clf()
        # self.fig.hold(True)
  
        img = plt.imread(imgfile)
        self.ax2 = self.fig.add_subplot(1, 1, 1)
        self.ax2.imshow(img, origin="upper", extent=(xmap1, xmap2, ymap1, ymap2))
  
        self.map3 = self.ax2.contourf(xg, yg, zgp, bounds, origin="lower",
                                      cmap=plt.cm.RdYlGn_r, alpha=0.8)
        #self.map3 = self.ax2.imshow(zgp, origin="lower", aspect="equal", vmin=bounds[0], 
                                    #vmax=bounds[-1], cmap=plt.cm.RdYlGn_r, alpha=0.7, 
                                    #extent=(self.xmin, self.xmax, self.ymin, self.ymax),
                                    #interpolation="nearest")
        self.map4 = self.ax2.contour(xg, yg, zgp, bounds, origin="lower",
                                     aspect="equal", cmap=plt.cm.RdYlGn_r, linewidths=2,
                                     alpha=1)
        plt.clabel(self.map4, inline=1, fontsize=10, fmt="%.2E", colors="#000000")
                                
        self.ax2.plot(self.xx[ptsel], self.yy[ptsel], linewidth=0, marker="o", 
                      markerfacecolor="magenta")                        
  
        self.cb2 = self.fig.colorbar(self.map3, shrink=0.8, orientation="vertical", format="%.2E")
  
        self.cb2.set_label("P", rotation=90)
        self.cb2.set_alpha(1)
        self.cb2.draw_all()
        self.ax2.axis([xmap1, xmap2, ymap1, ymap2])
  
        self.ax2.set_title("Probability Map\n", fontsize=9)
        self.ax2.set_xlabel("Easting (km)")
        self.ax2.set_ylabel("Northing (km)")
  
        self.canvas.draw()
        self.Layout()
  
        return zp



class pn3Canvas(wx.Panel):
    """
    It plots hazard curves ...   
    """
    
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
  
        vbox = wx.BoxSizer(orient=wx.VERTICAL)
        hbox_top = wx.BoxSizer(orient=wx.HORIZONTAL)
  
        self.fig = plt.figure()
        self.canvas = FigCv(self, -1, self.fig)
        self.toolbar = NavTb(self.canvas)
        #self.toolbar.Disable()
  
        self.fig.clf()
        #cid = self.fig.canvas.mpl_connect("button_press_event", self.onclick)
  
        self.fig.subplots_adjust(left=None, bottom=None, right=None, top=None, 
                                 wspace=None, hspace=0.3)
        # self.fig.hold(True)
  
        self.canvas.SetSize(self.GetSize())
        self.canvas.draw()
        
        vbox.Add(hbox_top, 0, wx.EXPAND|wx.ALL, 0)
        vbox.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 0)
        vbox.Add(self.toolbar, 0, wx.EXPAND|wx.ALL, 0)
   
        self.SetSizer(vbox)
  
  
    def hazard_curve(self, *kargs):
        """
        It plots hazard curves.
      
        """
        
        hc = kargs[0]            # hazard curves
        ptsel = kargs[1]         # selected point
        iml = kargs[2]           # intensity
        imt = kargs[3]           # intensity unit
        pth = kargs[4]           # threshold hazard map
        ith = kargs[5]           # intensity threshold
        dtw = kargs[6]           # time window
  
  
        ave = np.mean(hc[ptsel,:,:], axis=1)
        p10 = np.percentile(hc[ptsel,:,:], 10, axis=1)
        p50 = np.percentile(hc[ptsel,:,:], 50, axis=1)
        p90 = np.percentile(hc[ptsel,:,:], 90, axis=1)
  
        self.fig.clf()
        self.axes = self.fig.add_axes([0.15,0.15,0.75,0.75])
        self.fig.subplots_adjust(left=None, bottom=None, right=None, 
                                  top=None, wspace=None, hspace=0.3)
        # self.fig.hold(True)
        self.axes.grid(True)
        
        self.pt, = self.axes.plot(iml, p10, color="#00ff00", linewidth=1,
                                  alpha=1, label="10th Percentile")
  
        self.pt, = self.axes.plot(iml, p50, color="#ff0000", linewidth=1, 
                                  alpha=1, label="50th Percentile")
  
        self.pt, = self.axes.plot(iml, p90, color="#0000ff", linewidth=1, 
                                  alpha=1, label="90th Percentile")
  
        self.pt, = self.axes.plot(iml, ave, color="#000000", linewidth=1,
                                  alpha=1, label="Average")
  
        self.axes.axhline(y=pth, linestyle="--", color="#000000", linewidth=1,
                          alpha=1, label="Threshold in Probability")
  
        self.axes.axvline(x=ith, linestyle="-", color="#000000", linewidth=1,
                          alpha=1, label="Threshold in Intensity")
  
  
        self.axes.legend()
        tt = ("Point n." + str(ptsel+1) + " - Time window = " + str(dtw) + " years")
        
        self.axes.set_title(tt, fontsize=10)  
        self.axes.set_xlabel(imt)
        self.axes.set_xlim(iml[0],iml[-1])
        self.axes.set_ylabel("Probability of Exceedance")
        self.axes.set_yscale("log")
        self.canvas.draw()
        self.Layout()
        return p10, p50, p90, ave



class pn4Canvas(wx.Panel):
    """
    
    """
    
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
  
        vbox = wx.BoxSizer(orient=wx.VERTICAL)
        self.fig = plt.figure()
        self.canvas = FigCv(self, -1, self.fig)
        self.toolbar = NavTb(self.canvas)
        #self.toolbar.Disable()
  
        self.fig.clf()
        self.fig.subplots_adjust(left=None, bottom=None, right=None, top=None, 
                                 wspace=None, hspace=0.3)
        # self.fig.hold(True)
        self.canvas.SetSize(self.GetSize())
        self.canvas.draw()
        vbox.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 0)
        vbox.Add(self.toolbar, 0, wx.EXPAND|wx.ALL, 0)
        self.SetSizer(vbox)
  
  
    def plot_absolute_prob(self, event, *kargs): 
        """ 
            It plots the two following graphics:
              - empirical cumulative distribution function 
              - probability density function 
        """
  
        pabs = kargs[0]
        ave = kargs[1]
        nx = len(pabs)
        p = np.sort(pabs)
        y = np.arange(1,nx+1)
        y = y/float(nx)
        #ave = np.mean(p)
        perc10 = np.percentile(p, 10)
        perc50 = np.percentile(p, 50)
        perc90 = np.percentile(p, 90)
        
        avetxt = "{:.3e}".format(ave)
                
        self.fig.clf()
        self.fig.subplots_adjust(left=None, bottom=None, right=None, 
                                 top=None, wspace=None, hspace=0.3)
  
        ax1 = self.fig.add_subplot(2, 1, 1)
        # ax1.hold(True)
        ax1.grid(color="#aaaaaa", linestyle="dashed", linewidth=1, alpha=0.75)
        ax1.fill([perc10, perc90, perc90, perc10], [0,0,1,1], fill=True, 
                 color="#00ff00", alpha=0.25, 
                 label=r"10$^{th}$-90$^{th}$ Percentiles")
        
        ax1.plot(p,y)
        xmin, xmax = ax1.get_xlim()
        xmin = np.amin(p)
        if (xmin < 1e-10):
            xmin = 1e-10
        elif (xmin > 1e-5):
            xmin = 1e-5
        else:
            xmin = 1e-10
  
        ax1.axvline(x=perc10, color="#00ff00", linewidth=2, linestyle="solid")#, 
                    #label="10th Percentile")
        ax1.axvline(x=perc50, color="#000000", linewidth=2, linestyle="solid", 
                    label="50th Percentile")
        ax1.axvline(x=perc90, color="#00ff00", linewidth=2, linestyle="solid")#, 
                    #label="90th Percentile")
        ax1.axvline(x=ave, color="#ff0000", linestyle="solid", linewidth=2,
                    label="Average")
        ax1.text(ave, 0.5, r"$\bar{P}$ = " + avetxt, color="#ff0000", 
                 fontsize=12, bbox=dict(facecolor="#ffffff", 
                 edgecolor="#aaaaaa", linewidth=0.5))
                 
        ax1.set_title("Empirical Cumulative Distribution Function")
        ax1.legend(loc="upper left")
        #if np.any(p > 0.0):
        ax1.set_xscale("log")
          
        ax1.set_xlim(xmin,1e0)
        ax1.set_ylim(0,1)
        ax1.set_xlabel("P")
        ax1.set_ylabel("")
  
        ax2 = self.fig.add_subplot(2, 1, 2)
        # ax2.hold(True)
        ax2.grid(color="#aaaaaa", linestyle="dashed", linewidth=1, alpha=0.7)
        #bins = np.array([1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1e0])
        min_exp = 1+np.abs(np.floor(np.log10(np.abs(xmin)))).astype(int)
        bins = 1./np.power(10,range(min_exp))[::-1]
        ax2.hist(p, bins=bins, density=False, cumulative=False, alpha=0)
        ymin, ymax = ax2.get_ylim()
        ax2.fill([perc10, perc90, perc90, perc10], [0,0,ymax,ymax], fill=True, 
                 color="#00ff00", alpha=0.25, 
                 label=r"10$^{th}$-90$^{th}$ Percentiles")
        
        ax2.hist(p, bins=bins, density=False, cumulative=False, alpha=0.75, 
                 color="#0099ff")
        ax2.axvline(x=perc10, color="#00ff00", linewidth=2, linestyle="solid")#, 
                    #label="10th Percentile")
        ax2.axvline(x=perc50, color="#000000", linewidth=2, linestyle="solid", 
                    label="50th Percentile")
        ax2.axvline(x=perc90, color="#00ff00", linewidth=2, linestyle="solid")#, 
                    #label="90th Percentile")
        ax2.axvline(x=ave, color="#ff0000", linestyle="solid", linewidth=2,
                    label="Average")
        ax2.set_title("Probability Density Function")
        ax2.legend(loc="upper left")
        ax2.set_xscale("log")
  
        ax2.set_xlim(xmin,1e0)
        #ax2.set_xlim(1e-9,1e0)
        ax2.set_ylim(0,ymax)
        ax2.set_xlabel("P")
        ax2.set_ylabel("")
        self.canvas.draw()
  
  
    def plot_conditional_prob(self, event, *kargs): 
        """ 
           Plot  
        """
  
        self.fig.clf()
        #self.fig.clf(keep_observers=False)
        pcon = kargs[0]
        nodes = kargs[1]
        nodes_flag = kargs[2]
        
        # label correction inverting P for binary cases
        if nodes == 0:
            pass
        elif nodes == 1:
            #pcon = 1.0-pcon
            pass
        else:
            cond1 = (nodes < 4)
            cond2 = (nodes_flag[1] == 1 and nodes < 5)
            if (cond1 or cond2):
                if (nodes_flag[nodes-1] == 1):
                    pcon = 1.0-pcon
        
        labels = list()
        if (nodes == 1):
            tmp = np.mean(pcon, axis=0)
            values = np.array([tmp, 1.0-tmp])
            nwedges = np.shape(values)
            labels.append("Unrest")
            labels.append("No Unrest")
  
        elif (nodes == 2):
            tmp = np.mean(pcon, axis=0)
            values = np.array([tmp, 1.0-tmp])
            nwedges = np.shape(values)
            labels.append("Magmatic \nUnrest")
            labels.append("No Magmatic \nUnrest")
  
        elif (nodes == 3):
            if (nodes_flag[1] == 0):
                tmp = np.mean(pcon, axis=0)
                values = np.array([tmp, 1.0-tmp])
                nwedges = np.shape(values)
                labels.append("Magmatic \nEruption")
                labels.append("No Magmatic \nEruption")
            else:
                tmp = np.mean(pcon, axis=0)
                values = np.array([tmp, 1.0-tmp])
                nwedges = np.shape(values)
                labels.append("Hydrothermal \nUnrest")
                labels.append("Tectonic \nUnrest")
  
        elif (nodes == 4):
            if (nodes_flag[1] == 0):
                values = np.mean(pcon, axis=0)
                nwedges = np.shape(values)[0]
                for i in range(nwedges):
                    labels.append("Vent" + " " + str(i + 1))
            else:
                tmp = np.mean(pcon, axis=0)
                values = np.array([tmp, 1.0-tmp])
                nwedges = np.shape(values)
                labels.append("Hydrothermal \nEruption")
                labels.append("No Hydrothermal \nEruption")
  
        elif (nodes == 5):
            if (nodes_flag[1] == 0):
                values = np.mean(pcon, axis=0)
                nwedges = np.shape(values)[0]
                for i in range(nwedges):
                    labels.append("Size" + " " + str(i + 1))
            else:
                values = np.mean(pcon, axis=0)
                nwedges = np.shape(values)[0]
                for i in range(nwedges):
                    labels.append("Vent" + " " + str(i + 1))
  
        elif (nodes == 6):
            tmp = np.mean(pcon, axis=0)
            values = np.array([tmp, 1.0-tmp])
            nwedges = np.shape(values)
            labels.append("Hydrothermal \nEffusive \nEruption")
            labels.append("Hydrothermal \nExplosive \nEruption")
  
        else:
            msg = "ERROR:\n wrong value in var num_sel_list, function plot_pie"
            gf.show_error_message(self, msg, "ERROR") 
            return
            
        ax1 = self.fig.add_subplot(1, 1, 1)
        ax1.pie(values, explode=None, labels=labels, autopct="%1.1f%%", shadow=True)
        ax1.set_title("Average Probability")
  
        self.canvas.draw()


class pn5Canvas(wx.Panel):
    """
    
    """
    
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
  
        vbox = wx.BoxSizer(orient=wx.VERTICAL)
        self.fig = plt.figure()
        self.canvas = FigCv(self, -1, self.fig)
        self.toolbar = NavTb(self.canvas)
        #self.toolbar.Disable()
  
        self.fig.clf()
        self.fig.subplots_adjust(left=None, bottom=None, right=None, top=None, 
                                 wspace=None, hspace=0.3)
        # self.fig.hold(True)
        self.canvas.SetSize(self.GetSize())
        self.canvas.draw()
        vbox.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 0)
        vbox.Add(self.toolbar, 0, wx.EXPAND|wx.ALL, 0)
        self.SetSizer(vbox)
  
  
    def custom_div_cmap(self, numcolors=11, name="custom_div_cmap",
                          mincol="green", midcol="yellow", maxcol="red"):
        """ Create a custom diverging colormap with three colors
        
        Default is blue to white to red with 11 colors.  Colors can be specified
        in any way understandable by matplotlib.colors.ColorConverter.to_rgb()
        """
  
        from matplotlib.colors import LinearSegmentedColormap 
        
        cmap = LinearSegmentedColormap.from_list(name=name, 
                                                 colors =[mincol, midcol, maxcol],
                                                 N=numcolors)
        return cmap
  
  
    def show_map(self, *kargs):
        """ 
           Vent Map
            
        """ 
        
        #z = np.mean(kargs[0], axis=0)
        z = kargs[0]
        zlim = np.linspace(np.min(z), np.max(z), 11)
  
        xmin_map, xmax_map, ymin_map, ymax_map = kargs[1]
        par1, par2, par3, par4, par5 = kargs[2]
        vcx = kargs[3]
        vcy = kargs[4]
        imgpath = kargs[5]
        
        self.fig.clf()
        self.fig.subplots_adjust(left=None, bottom=None, right=None, 
                                 top=None, wspace=None, hspace=0.3)
        # self.fig.hold(True)
        self.ax = self.fig.add_subplot(1, 1, 1)
        
  
        cmap = self.custom_div_cmap(9)    # 
        #majorFormatter = FormatStrFormatter("%d")
        xlab = "Easting (km)"
        ylab = "Northing (km)"
        #majorFormatter = FormatStrFormatter("%5.2f")
        #xlab = "Longitude"
        #ylab = "Latitude"
  
        #z = A[:,kargs[1]]
        
        #imgfile = ""
        #tmp_dir = os.path.join(vol_dir, string.lower(volname))
        #for item in os.listdir(tmp_dir):
          #if (item[-7:-3] == "map."):
            #imgfile = str(os.path.join(tmp_dir, item))
            
        #if (imgfile == ""):
          #msg = ("WARNING\nImage map file "
                 #"in" + vol_dir + string.lower(volname)  + " does not "
                 #"exist. You can continue but no background map will "
                 #"be plotted.")
          #gf.show_warningMessage(self, msg, "WARNING")
        #else:  
          #if (imgfile[-3:] == "png"):
            #img = plt.imread(imgfile)
            #plt.imshow(img, origin="upper", 
                       #extent=(xmin_map, xmax_map, ymin_map, ymax_map))
          ##elif (imgfile[-3:] == "jpg"):
            ##img = plt.imread(imgfile)
            ##plt.imshow(img, origin="lower", 
                       ##extent=(xmin_map, xmax_map, ymin_map, ymax_map))
          #else:
            #msg = ("ERROR\nImage extension format "
                   #"in " + vol_dir + string.lower(volname)  + " must "
                   #"be .png only.")
            #gf.show_error_message(self, msg, "ERROR")
            #return
          
        
        img = plt.imread(imgpath)
        self.ax.imshow(img, origin="upper", extent=(xmin_map, xmax_map, ymin_map, ymax_map))
  
        patches = []
           
        if (par4 == -9999):
            in_rad = par1/1000
            ou_rad = par2/1000
            strike = par3
            r1 = ou_rad
            r2 = in_rad
            ww = ou_rad - in_rad
            st = int(strike) * -1
            c = Circle((vcx, vcy), r2)
            patches.append(c)
            c = Wedge((vcx, vcy), r1, st, st+90, ww)
            patches.append(c)
            c = Wedge((vcx, vcy), r1, st+90, st+180, ww)
            patches.append(c)
            c = Wedge((vcx, vcy), r1, st+180, st+270, ww)
            patches.append(c)
            c = Wedge((vcx, vcy), r1, st+270, st+360, ww)
            patches.append(c)
          
            self.im = PatchCollection(patches, cmap=cmap, 
                                 color="#cccccc", linewidth=1.5, alpha=0.6)
  
        else:
            wt = par1/1000
            ht = par2/1000
            nw = par3
            nh = par4
            ww = wt / nw
            hh = ht / nh
            xin = vcx - 0.5 * wt
            yin = vcy - 0.5 * ht
            st = math.radians(par5)
            for j in range(nh):
                for i in range(nw): 
                    xp = (xin+i*ww)
                    yp = (yin+j*hh)
                    xc = xp - vcx
                    yc = yp - vcy
                    xc = (xp-vcx)*math.cos(st)-(yp-vcy)*math.sin(st)
                    yc = (xp-vcx)*math.sin(st)+(yp-vcy)*math.cos(st)
                    xc = xc + vcx
                    yc = yc + vcy
  
                    c = matplotlib.patches.Rectangle(xy=(xc, yc), width=ww, 
                                                     height=hh, angle=par5)
                    patches.append(c)
  
            
            self.im = PatchCollection(patches, cmap=cmap, alpha=0.6, 
                                 color="#cccccc", linewidth=0.1)
                               
       
        self.im.set_array(np.array(z))
        self.ax.add_collection(self.im)
  
        self.c1 = self.fig.colorbar(self.im, format="%.3e", shrink=0.9,
                                    ticks=np.linspace(zlim[0], zlim[-1],10))
        self.im.set_clim([zlim[0], zlim[-1]])
        self.c1.set_alpha(1)
        self.c1.draw_all()
        #self.im.set_clim([zlim[0], 0.1])
        
        #self.ax.set_title(args[2])
        self.ax.set_xlabel(xlab)
        self.ax.set_ylabel(ylab)
        #self.ax.xaxis.set_major_formatter(majorFormatter)
        #self.ax.yaxis.set_major_formatter(majorFormatter)
  
        #nticks = 6
        #dx = (xmax_map-xmin_map)/nticks
        #dy = (ymax_map-ymin_map)/nticks
        #xt = []
        #yt = []
  
        #for i in range(nticks):
          #xt.append(xmin_map+i*dx)
          #yt.append(ymin_map+i*dy)
  
        #self.ax.set_xticks(xt)
        #self.ax.set_yticks(yt)
  
        self.canvas.draw()




class pn6Canvas(wx.Panel):
    """
    
    """
    
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
  
        vbox = wx.BoxSizer(orient=wx.VERTICAL)
        self.fig = plt.figure()
        self.canvas = FigCv(self, -1, self.fig)
        self.toolbar = NavTb(self.canvas)
        #self.toolbar.Disable()
  
        self.fig.clf()
        self.fig.subplots_adjust(left=None, bottom=None, right=None, top=None, 
                                 wspace=None, hspace=0.3)
        # self.fig.hold(True)
        self.canvas.SetSize(self.GetSize())
        self.canvas.draw()
        vbox.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 0)
        vbox.Add(self.toolbar, 0, wx.EXPAND|wx.ALL, 0)
        self.SetSizer(vbox)
  
  
    def show_map(self, *kargs):
        """ 
         Vent Map
            
        """ 

