import numpy as np
from numpy import genfromtxt
import math
import matplotlib.pyplot as plt
import os.path
import csv

def __init__(self):
    pass


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return np.array([rho,phi])
def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return np.array([x,y])
def scan2map(measurement, selfPosition = np.array([0,0,0])):
    r = measurement[0,:]
    t = np.radians(measurement[1,:])
    r.shape = (r.size,1)
    t.shape = (t.size,1)
    heading=selfPosition[2]
    heading=math.radians(heading)
    #print(heading)
    t = t-heading*np.ones((t.size,1))+ (math.pi)/2
    self_x= selfPosition[0]*np.ones((t.size,1))
    self_y= selfPosition[1]*np.ones((t.size,1))
    self_x.shape = (t.size,1)
    self_y.shape = (t.size,1)
    selfPosition = np.concatenate((self_x,self_y),axis=1)
    #print(selfPosition)
    a =pol2cart(r,t)
    a.shape = (2,t.size)
    selfPosition = selfPosition.T
    x = selfPosition+a
    return x

def interPolation(PD):
    
    t= np.linspace(40,120,num=4000, endpoint=True)
    R_interpolated= np.interp(t,PD[1,:],PD[0,:])
    PDinter= np.zeros([2,R_interpolated.size])
    #print()
    PDinter[1,:]= t.T
    PDinter[0,:]= R_interpolated.T 
   # print(PDinter)
    #plt.plot(PDinter)
    return PDinter
    
def data2map(coordinateMeas,selfLocalization):
    positionData = genfromtxt(coordinateMeas,delimiter=',')
    print(positionData.shape)
    
    selfLocalizationData = genfromtxt(selfLocalization,delimiter=',')
    print(selfLocalizationData.shape)
    #headingData = genfromtxt(headingMeas, delimiter=',')
    #headingData = math.radians(headingData)
    #polarData = np.zeros((positionData.shape))
    #for i in range (0,positionData.shape[1]):
        #polarData[:,i]= cart2pol(positionData[0,i],positionData[1,i])
    
#    polar_Data= interPolation(positionData)
    #print (polar_Data.shape)
    #print (polarData.shape)
    #print(selfLocalizationData)
    #xy_data = scan2map(positionData,selfLocalizationData)
    xy_data = scan2map(positionData,selfLocalizationData)
    return xy_data

