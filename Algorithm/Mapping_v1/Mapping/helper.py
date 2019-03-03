import numpy as np
from numpy import genfromtxt
import math
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
def scan2map(measurement, heading=0, selfPosition = np.array([0,0])):
    r = measurement[0,:]
    t = measurement[1,:]
    r.shape = (r.size,1)
    t.shape = (t.size,1)
    t = t-heading*np.ones((t.size,1))
    self_x= selfPosition[0]*np.ones((t.size,1))
    self_y= selfPosition[1]*np.ones((t.size,1))
    self_x.shape = (t.size,1)
    self_y.shape = (t.size,1)
    selfPosition = np.concatenate((self_x,self_y),axis=1)
    a =pol2cart(r,t)
    a.shape = (2,70)
    selfPosition = selfPosition.T
    x = selfPosition+a
    return x

def data2map(coordinateMeas,selfLocalization,headingMeas):
    positionData = genfromtxt(coordinateMeas,delimiter=',')
    selfLocalizationData = genfromtxt(selfLocalization,delimiter=',')
    headingData = genfromtxt(headingMeas, delimiter=',')
    headingData = math.radians(headingData)
    polarData = np.zeros((positionData.shape))
    for i in range (0,positionData.shape[1]):
        polarData[:,i]= cart2pol(positionData[0,i],positionData[1,i])
    xy_data = scan2map(polarData,headingData,selfLocalizationData)
    return xy_data
