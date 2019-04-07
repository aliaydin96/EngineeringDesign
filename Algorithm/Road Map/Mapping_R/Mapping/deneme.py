
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os.path
import math
from math import pi
from helper import *
#%%

position_data = genfromtxt('Coordinate_Meas_1',delimiter=',')
polar_data = np.zeros((position_data.shape))
for i in range (0,position_data.shape[1]):
     polar_data[:,i]= cart2pol(position_data[0,i],position_data[1,i])
# %% Polar data



np.radian(2)

heading = pi
import numpy as np

a = np.ones(10)
selfPosition = np.array((0,0))
r = polar_data[0,:]
t = polar_data[1,:]
r.shape = (r.size,1)
t.shape = (t.size,1)
type(heading)
t = t+heading*np.ones((t.size,1))
self_x= selfPosition[0]*np.ones((t.size,1))
self_y= selfPosition[1]*np.ones((t.size,1))
self_x.shape = (t.size,1)
self_y.shape = (t.size,1)
selfPosition = np.concatenate((self_x,self_y),axis=1)
a =pol2cart(r,t)
a.shape = (2,70)
selfPosition = selfPosition.T
x = a+selfPosition
x.shape
# %%
mappingNumber=1;
coordinateMeas= 'Coordinate_Meas_'+ str(mappingNumber)
selfLocalization='Self_Localization_Meas_'+ str(mappingNumber)
headingMeas = 'Heading_Meas_' + str (mappingNumber)

positionData = genfromtxt(coordinateMeas,delimiter=',')
coordinateMeas

selfLocalizationData = genfromtxt(selfLocalization,delimiter=',')
type(selfLocalizationData)

selfLocalizationData

headingData = genfromtxt(headingMeas, delimiter=',')
headingData
