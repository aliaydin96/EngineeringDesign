# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 13:54:50 2019

@author: Nail
"""
import numpy as np
import os
import math 
def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return np.array([rho,phi])

def linefit(x1,y1,x2,y2):
    a=(y2-y1)/(x2-x1)
    b=y1
    return a,b

def line2pointDistance(a,b,x1,y1):
    return (abs( a*x1 - 1*y1 + b )) / (np.sqrt( a*a + b*b))
def pol2cart(rho, phi):
    
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return np.array([x,y])

def reading(folder,fileName,discardFactor=0.32):
    cwd = os.getcwd()
    src=cwd+folder+fileName+'.csv'
    meas = np.genfromtxt(src,delimiter = ',')
    measLen=meas.shape[0]
    meas.shape=(1,measLen)
    index=np.array([])
    distance=(meas[0][0:measLen-1]- meas[0][1:measLen]);
    average=  np.sum(abs(distance))/ (measLen-1);
    for i in range(measLen-1):
        if meas[0][i]>=2500:
            meas[0][i]=0
        if meas[0][i+1]>=2500:
            meas[0][i+1]=0
        if abs(meas[0][i+1]-meas[0][i])> discardFactor*average:
            index=np.append(index,i)
        if meas[0][i]<50:
            index=np.append(index,i)
    index= index.astype(int)
    np.delete(meas,index)
    theta=np.linspace(0,359.1,measLen) 
    theta=np.radians(theta)
    theta.shape=(1,measLen)
    meas=np.concatenate((meas, theta), axis=0)
    return meas

def zoom(meas,selfLocalization=np.zeros((1,2))):
    zoomed_r,zoomed_theta=meas[0][np.where(meas[0]<300)],meas[1][np.where(meas[0]<300)]
    zoomed_r,zoomed_theta=zoomed_r[np.where(zoomed_r != 0)],zoomed_theta[np.where(zoomed_r != 0)]
    zoomedData=pol2cart(zoomed_r,zoomed_theta)
    return zoomedData
def zoomPolar(meas):
    zoomed_r,zoomed_theta=meas[0][np.where(meas[0]<300)],meas[1][np.where(meas[0]<300)]
    zoomed_r,zoomed_theta=zoomed_r[np.where(zoomed_r != 0)],zoomed_theta[np.where(zoomed_r != 0)]
    return zoomed_r,zoomed_theta
import numpy
def distance(x1,x2,y1,y2):
    return math.hypot(x2 - x1, y2 - y1)

def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.
    """

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError( "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")


    s=numpy.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y