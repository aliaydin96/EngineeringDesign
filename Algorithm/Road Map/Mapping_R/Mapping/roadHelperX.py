import numpy as np
from numpy import genfromtxt
import math
import matplotlib.pyplot as plt
import os.path
import csv



def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return np.array([rho,phi])


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return np.array([x,y])
    
    
def DestinationPoint(maxPoint,coninin_siqinin_qeyfi=0):
    
    r = maxPoint[0]
    t = maxPoint[1]
    heading=maxPoint[4]
    t = t-heading+coninin_siqinin_qeyfi;
    a =pol2cart(r,t)
    
    DP= [maxPoint[2]+a[0], maxPoint[3]+a[1]]
    
    return  DP


def scan2map(Data,coninin_siqinin_qeyfi=90):
    r = Data[0]
    t = Data[1]
    r.shape=(1,r.size)
    t.shape=(1,t.size)
    heading=Data[4]
    heading.shape=(1,heading.size)
    
    t = t-heading+coninin_siqinin_qeyfi*np.ones((1,t.size))
    
    
    a =pol2cart(r,t)
    a.shape = (2,t.size)
  
    x = np.array([a[0]+Data[2], a[1]+Data[3]])
    return x
