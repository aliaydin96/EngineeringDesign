# -*- coding: utf-8 -*-
"""
Created on Mon May  6 17:54:16 2019
@author: Nail
"""
import numpy as np
import math
import os 
import matplotlib.pyplot as plt
from helper import * 
import statistics as s

from scipy.stats import kurtosis
from scipy.stats import skew
from numpy  import array
from tr_sq_recognition import *
cwd = os.getcwd()

def detection(forCounter,x_in,y_in,heading):
    data = np.genfromtxt('data'+str(forCounter)+'.csv',delimiter=',')
    dataLen=data.shape[0]
    data.shape=(1,dataLen)
    theta = []
    for i in range(400):
      theta.append(i*math.pi/200)
    theta = array(theta)
    theta.shape=(1,dataLen)
    meas = np.concatenate((data,theta),axis = 0)
    zoomedR,zoomed_t = zoomPolar(meas)
    meas=zoom(meas)
    print("len ",len(meas[0]))
    flag = 0
    dis = np.zeros((len(meas[0]),1))
    for f in range(len(meas[0])-1):
        dis[f]=distance(meas[0][f],meas[0][f+1],meas[1][f],meas[1][f+1])
        if dis[f] < 10 and flag == 0:
            flag = 1
            min_index = f+1
        if dis[f] < 10 and flag == 1:
            max_index = f+1
    
    before_filter = cart2pol(meas[0][min_index:max_index],meas[1][min_index:max_index])
    zoomed_r = before_filter[0]
    zoomed_t = before_filter[1]
    radiusT= np.transpose(zoomed_r)
    thetaT = np.transpose(zoomed_t)
    radiusTf = smooth(radiusT,window_len=5)
    thetaTf =smooth(thetaT,window_len=5)
    radiusTf1 = radiusTf [2:-2]
    thetaTf1 = thetaTf [2:-2]
    
    minIndex=np.argmin(radiusTf1)
    center = pol2cart(radiusTf1[minIndex]+50,thetaTf1[minIndex])
    print("rmin ",radiusTf1[minIndex],"tet ",thetaTf1[minIndex]," ", x_in," ",y_in," ",heading)
    dis2 = np.zeros((len(radiusTf1),1))
    for r in range(len(radiusTf1)):
        dis2[r]=distance(pol2cart(radiusTf1[r],thetaTf1[r])[0],center[0],pol2cart(radiusTf1[r],thetaTf1[r])[1],center[1])
    filtered=pol2cart(radiusTf1,thetaTf1)
    fitness = []
    if ((np.std(dis2) >= 0.59) & (np.std(dis2) <= 6.8417)) and  ((np.mean(dis2)>=48.77 ) & (np.mean(dis2) <= 51.3)):
        center=pol2cart((radiusTf1[minIndex]+50),(thetaTf1[minIndex]+heading-np.pi/2))
        print("10 cm circle")
        return (center[0]+x_in),(center[1]+y_in),0,0,7,radiusTf1[minIndex]
    elif ((np.std(dis2) >= 2.7835) & (np.std(dis2) <= 6.2517)) and  ((np.mean(dis2)>= 42.814) & (np.mean(dis2) <= 47.425)):
        angle = []
        for t in range(len(filtered[0])-5):
            angle.append(math.atan2(filtered[0][t]-filtered[0][t+5],filtered[1][t]-filtered[1][t+5])*180)
        a,b = linefit(0,angle[0],len(angle)-1,angle[-1])
        fitness = []
        for n in range(len(angle)):
            fitness.append(line2pointDistance(a,b,n,angle[n]))
        if np.mean(fitness) <= 0.09:
            center=pol2cart(radiusTf1[minIndex]+25,thetaTf1[minIndex]+heading-np.pi/2)
            print("5 cm circle")
            return center[0]+x_in,center[1]+y_in,0,0,6,radiusTf1[minIndex]
        if len(angle)<=17:
            center=pol2cart(radiusTf1[minIndex]+25,thetaTf1[minIndex]+heading-np.pi/2)
            print("5 cm circle")
            return center[0]+x_in,center[1]+y_in,0,0,6,radiusTf1[minIndex]
        else:
            try:
                a,b,c,d,e = recognit(forCounter,x_in,y_in,heading)
                return a,b,c,d,e
            except TypeError:
                print('Patlak')
    else:
        try:
            a,b,c,d,e = recognit(forCounter,x_in,y_in,heading)
            return a,b,c,d,e
        except TypeError:
            print('Patlak')
            pass
    
#