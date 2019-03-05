import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.axes as ma
import os.path
import math
from math import pi
from helper import *
import cv2

# %%

mappingNumber = 1
while mappingNumber<4:
    coordinateMeas= 'data-'+ str(mappingNumber) +'.csv'
    selfLocalization='SL_'+ str(mappingNumber) +'.csv'
    #headingMeas = 'H_' + str (mappingNumber)
    if os.path.isfile(coordinateMeas):
        if mappingNumber == 1:
            Map=data2map(coordinateMeas,selfLocalization)
            mappingNumber = mappingNumber + 1
            color='red'
            plt.figure(mappingNumber)
            plt.scatter(Map[0,:],Map[1,:], c=color)
            plt.ylim(top=600)
            plt.ylim(bottom=200)
            plt.xlim(left=-600)
            plt.xlim(right=600)
   
        else:
            Map2 = data2map(coordinateMeas,selfLocalization)
            Map= np.concatenate((Map,Map2),axis=1)
            mappingNumber = mappingNumber + 1
            color='blue'
            plt.figure(mappingNumber)
            plt.scatter(Map[0,:],Map[1,:], c=color)
            plt.ylim(top=600)
            plt.ylim(bottom=200)
            plt.xlim(left=-600)
            plt.xlim(right=600)
    else:
        continue
         
 
   
# %%
Map.shape
#plt.figure(1)
#plt.scatter(Map[0,:],Map[1,:])
#plt.ylim(top=600)
#plt.ylim(bottom=200)
#plt.xlim(left=-600)
#plt.xlim(right=600)


plt.savefig('Map.png')
# %%

np.savetxt("Map.csv", Map, delimiter=",")

