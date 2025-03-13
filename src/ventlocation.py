#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 

This file is part of PyBetUnrest.

'''

import sys
import wx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCv
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavTb
from matplotlib.patches import Circle, Wedge, Rectangle
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


class VentLocation(wx.Frame):
    def __init__(self, parent, id, title, *kargs):
        wx.Frame.__init__(self, parent, id, title, size=(-1, -1))
  
        ''' 
            It opens a new frame showing the vent location.
            Parameters:
              - args[0] --> map file name and path
              - args[1] --> list vloc_par[]
                    if len(vloc_par) == 3 --> circular geometry 
                      vloc_par[0] = internal radius in km
                      vloc_par[1] = strike
                      vloc_par[2] = external radius in km)
                    if len(vloc_par) == 4 --> grid geometry 
                      vloc_par[0] = width in km 
                      vloc_par[1] = heigth in km 
                      vloc_par[2] = n. points along width
                      vloc_par[3] = n. points along height
              - args[2] --> list vloc_map_corners[]
              - args[3] --> list vol_center
  
        '''
   
        par1, par2, par3, self.par4, par5 = kargs[1]
           
        xmin_map = kargs[2][0]/1000.
        xmax_map = kargs[2][1]/1000.
        ymin_map = kargs[2][2]/1000.
        ymax_map = kargs[2][3]/1000.
  
        #print(kargs[0], kargs[3])
        self.vcx = kargs[3][0]/1000.
        self.vcy = kargs[3][1]/1000.
        vcx = self.vcx
        vcy = self.vcy
  
        majorFormatter = FormatStrFormatter('%d')
        #majorFormatter = FormatStrFormatter('%5.2f')
  
        patches = []
         
        if (self.par4 == -9999):
            in_rad = par1/1000
            ou_rad = par2/1000
            strike = par3
            self.r1 = ou_rad
            self.r2 = in_rad
            self.ww = ou_rad - in_rad
            self.st = int(strike) * -1 # clockwise
            r1 = self.r1
            r2 = self.r2
            ww = self.ww
            st = self.st
            
            xmin_fig = xmin_map
            xmax_fig = xmax_map
            ymin_fig = ymin_map
            ymax_fig = ymax_map
  
            c = Circle(xy=(vcx, vcy), radius=r2, facecolor='#330000', 
                       alpha=0.5, picker=5)
            patches.append(c)
            c = Wedge(center=(vcx, vcy), r=r1, theta1=st, theta2=st+90, 
                      width=ww, facecolor='#ffff00', alpha=0.5)
            patches.append(c)
            c = Wedge(center=(vcx, vcy), r=r1, theta1=st+90, theta2=st+180, 
                      width=ww, facecolor='#990000', alpha=0.5)
            patches.append(c)
            c = Wedge(center=(vcx, vcy), r=r1, theta1=st+180, theta2=st+270, 
                      width=ww, facecolor='#ff0000', alpha=0.5)
            patches.append(c)
            c = Wedge(center=(vcx, vcy), r=r1, theta1=st+270, theta2=st+360, 
                              width=ww, facecolor='#ff9900', alpha=0.5)
            patches.append(c)
          
        else:
            self.wt = par1/1000.
            self.ht = par2/1000.
            self.nw = par3
            self.nh = self.par4
            self.ww = float(wt/nw)
            self.hh = float(ht/nh)
            self.xin = vcx-0.5*wt
            self.yin = vcy-0.5*ht
            self.st = math.radians(par5)
  
            st = self.st
            xin = self.xin
            yin = self.yin
            ww = self.ww
            hh = self.hh
            wt = self.wt
            ht = self.ht
            nw = self.nw
            nh = self.nh
            
            #xmin_fig = xin-0.25*wt
            #xmax_fig = xin+1.25*wt
            #ymin_fig = yin-0.25*ht
            #ymax_fig = yin+1.25*ht
            xmin_fig = xmin_map
            xmax_fig = xmax_map
            ymin_fig = ymin_map
            ymax_fig = ymax_map
            #print(xmin_map, xmax_map, ymin_map, ymax_map)
            #print(xin, yin)
            for i in range(nw):
                for j in range(nh):
                    xp = (xin+i*ww)
                    yp = (yin+j*hh)
                    xc = xp - vcx
                    yc = yp - vcy
                    #xc = (xp-vcx)*math.cos(st)-(yp-vcy)*math.sin(st)
                    #yc = (xp-vcx)*math.sin(st)+(yp-vcy)*math.cos(st)
                    xc = (xp-vcx)*np.cos(st)-(yp-vcy)*np.sin(st)
                    yc = (xp-vcx)*np.sin(st)+(yp-vcy)*np.cos(st)
                    xc = xc + vcx
                    yc = yc + vcy
                    
                    # for vhub only (no rotation)
                    c = Rectangle(xy=(xc, yc), width=ww, height=hh, 
                                  linewidth=1, edgecolor="#ff0000",
                                  facecolor="#aaaaaa", alpha=0.5, fill=True)
  
                    #c = Rectangle(xy=(xc, yc), width=ww, height=hh, 
                                 #angle=par5, linewidth=1, edgecolor="#ff0000",
                                 #facecolor="#aaaaaa", alpha=0.5, fill=True)
                    #c.set_facecolor(np.random.rand(3))
                    #c.set_facecolor('none')
                    patches.append(c)
  
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        self.fig = plt.figure()
        self.canvas = FigCv(self, -1, self.fig)
        #print(wx.Platform)
        
        if (wx.Platform != '__WXMAC__'):
            self.toolbar = NavTb(self.canvas)
        
        self.fig.clf()
        self.fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.3)
        # self.fig.hold(True)
        self.ax = self.fig.add_subplot(1, 1, 1, aspect='equal')
        
        imgfile = str(kargs[0])
        if (imgfile[-4:] != ".png" ):
            pass
        else:
            img = plt.imread(imgfile)
            self.ax.imshow(img, origin="upper", extent=(xmin_map, xmax_map, ymin_map, ymax_map))
        
        #img = plt.imread(imgfile)
        #self.ax.imshow(img, origin="upper", extent=(xmin_map, xmax_map, ymin_map, ymax_map))
        
        for item in patches:
            self.ax.add_artist(item)
        
        self.ax.set_xlim(xmin_fig, xmax_fig)
        self.ax.set_ylim(ymin_fig, ymax_fig)
        self.ax.set_xlabel("Easting (km)")
        self.ax.set_ylabel("Northing (km)")
  
        self.ax.set_title("")
        self.ax.xaxis.set_major_formatter(majorFormatter)
        self.ax.yaxis.set_major_formatter(majorFormatter)
  
        self.canvas.draw()
        self.canvas.mpl_connect('motion_notify_event', self.update_cur_pos)
        vbox1.Add(self.canvas, 1, wx.EXPAND)
        if (wx.Platform != '__WXMAC__'):
            vbox1.Add(self.toolbar, 0, wx.EXPAND)
        self.SetSizer(vbox1)
        self.Fit()
        self.Show(True)
  
    def change_cursor(self, event):
        pass
  
    def update_cur_pos(self, event):
  
        vcx = self.vcx
        vcy = self.vcy
        st = self.st
  
        if (event.inaxes != self.ax): 
            return
        else:
            x, y = event.xdata, event.ydata
            
            if (self.par4 == -9999):
                r1 = self.r1
                r2 = self.r2 
                dist = np.sqrt( np.power(x-vcx,2) + np.power(y-vcy,2) )
                if (dist <= r2 ):
                    self.ax.set_title("Vent 1, x = %8.3f km, y = %8.3f km" %(x, y))
      
                elif (dist > r2 and dist <= r1):
      
                    angle = (np.arctan2( y-vcy, x-vcx ) * 180 / np.pi)
                    if (angle < 0):
                        angle = angle + 360
      
                    if (angle >= 0 and angle < st+90 or angle > st+360 and angle <= 360):
                        vent = "2" 
                    elif (angle >= st+90 and angle < st+180):
                        vent = "5" 
                    elif (angle >= st+180 and angle < st+270):
                        vent = "4" 
                    else:
                        vent = "3" 
      
                    #self.ax.set_title("Vent %s, x = %8.3f km, y = %8.3f km | %5.1f " %(vent, x, y, angle))
                    self.ax.set_title("Vent %s, x = %8.3f km, y = %8.3f km" %(vent, x, y))
                else:
                    self.ax.set_title("x = %8.3f km, y = %8.3f km" %(x, y))
  
            else:
                xin = self.xin
                yin = self.yin
                ww = self.ww
                hh = self.hh
                wt = self.wt
                ht = self.ht
                if (x > xin and x < xin+wt and y > yin and y < yin+ht):
                    ii = int((x - xin)/ww) + 1
                    jj = int((y - yin)/hh)
                    vent = ii + jj * nw
                    self.ax.set_title("Vent %s, x = %8.3f km, y = %8.3f km" %(vent, x, y))
                else:
                    self.ax.set_title("x = %8.3f km, y = %8.3f km" %(x, y))
              
  
            # self.ax.set_title("x = {:f8.3} km,  y = {:f8.3} km".format(x,y))
            self.canvas.draw()
  
    def onpick(self, event):
        # ev = event.artist
        # xdata, ydata = ev.get_data()
        # xdata = ev.get_facecolor()
        # ydata = thisline.get_ydata()
        # ind = event.ind
        # print('onpick points:', zip(xdata[ind], ydata[ind]))
        print(event.x)


