#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import numpy as np
import matplotlib.pyplot as plt

""" 

This file is part of PyBetEF.

"""

def calc_monitoring_prob(par_th1, par_th2, par_rel, 
                         par_val, par_wei, sample, nmix, anomaly_pars):
    """
    """
    a = anomaly_pars[0]
    b = anomaly_pars[1]
    l = anomaly_pars[2]
    tmp = calc_anomaly_degree(par_th1, par_th2, par_rel, par_val)
    anDegTot = np.sum(np.array(tmp)*np.array(par_wei))
    probM, aveM = sampling_monitoring(anDegTot, sample, nmix, a, b, l)
    #probM, aveM = sampling_monitoring_OLD(anDegTot, sample, nmix)
    return probM, aveM   
   

def mixing(postBG, postM, sample, nmix):
    """
    Statistical mixing of long-term and monitoring for binomial
    distribution (yes/no)
    """
    tmp, nbranches = np.shape(postM)
    pp = np.zeros((sample,nbranches))
    for i in range(nbranches):
        sample1 = postM[:,i]
        sample2 = postBG[i,:sample-nmix]
        pp[:,i] = np.random.permutation(np.concatenate([sample1,sample2]))
    
    return pp
  

def sampling_monitoring(anDegTot, sample, nmix, a, b, l):
    """
    Sampling the monitored parameter with a given degree of anomaly
     
    """
    aveM = 1 - a*np.exp(-b*anDegTot)
    alpha = aveM*(l+1)
    beta = (l+1)-alpha
    probM = np.random.dirichlet([alpha,beta], nmix)
    return probM, aveM




def sampling_monitoring_OLD(anDegTot, sample, nmix):
    """
    Sampling the monitored parameter with a given degree of anomaly
     
    """
    pars = [0.5,1.0,0.0,2.0]
    #pars = [0.99,1.0,0.0,2.0]
    l = 1
    a = np.random.uniform(pars[0], pars[1], sample)
    b = np.random.uniform(pars[2], pars[3], sample)
    
    alpha = (1-a*np.exp(-b*anDegTot))*(l+1)
    beta = l+a*np.exp(-b*anDegTot)
    
    probM = np.zeros((nmix,2))
    for i in range(nmix):
        probM[i,:] = np.random.dirichlet([alpha[i],beta[i]], 1)
  
    aveM = np.mean(alpha)
    return probM, aveM


 
def calc_anomaly_degree(th1, th2, rel, v):  
    """
    Calculation of the Degree of Anomaly
    """
    npars = len(v)
    anDeg = []
    
    for i in range(npars):
      
        if (th2[i] == "None" or th2[i] == "saturated"):
            if (rel[i] == "<"):
                if (v[i] <= th1[i]):  
                    anDeg.append(1.0)
                else:
                    anDeg.append(0.0)
                
            elif (rel[i] == ">"):
                if (v[i] >= th1[i]):
                    anDeg.append(1.0)
                else:  
                    anDeg.append(0.0)
                
            else:
                print("Error in rel")
  
        else:
            tmp1 = (v[i]-th1[i])/(th2[i]-th1[i])
            if (rel[i]=="<"):
                if (v[i] >= th2[i]):
                    anDeg.append(0.0)
                elif (v[i] <= th1[i]):  
                    anDeg.append(1.0)
                else:  
                    anDeg.append(0.5*(np.sin(np.pi*tmp1+0.5*np.pi)+1) )
            elif (rel[i]==">"):
                if (v[i] >= th2[i]):
                    anDeg.append(1.0)
                elif (v[i] <= th1[i]):  
                    anDeg.append(0.0)
                else:  
                    anDeg.append(0.5*(np.sin(np.pi*tmp1-0.5*np.pi)+1) )
       
            else:
                print("Error in rel")
          
    return anDeg
  


def make_alpha16(n, p, l, pd):
    """
    Calculate alpha values for nodes 1 to 6
    
    Variables:
    
    n: n. branches
    a: alpha
    p: prior probability
    l: equivalent number of data
    pd: past data
  
    """
    a = [0]*n
    a0 = l + n - 1
    for i in range(n):
        a[i] = (p[i] * a0) + pd[i]
    
    return a
  


def theoretical_average(a):
    """
    """
    if (np.size(a) <= 2):
        ave = a[0]/np.sum(a)
    else:
        ave = a/np.sum(a)
  
    return ave

def mixing_average(ave_longterm, ave_monitoring, weight):
    """
    """
    
    ave_mix = (1-weight)*ave_longterm + weight*ave_monitoring
    return ave_mix
  
