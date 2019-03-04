import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os.path
import math
from math import pi
from helper import *
import cv2

# %%

mappingNumber = 1
while mappingNumber<5:
    coordinateMeas= 'Coordinate_Meas_'+ str(mappingNumber)
    selfLocalization='Self_Localization_Meas_'+ str(mappingNumber)
    headingMeas = 'Heading_Meas_' + str (mappingNumber)
    if os.path.isfile(coordinateMeas):
        if mappingNumber == 1:
            Map=data2map(coordinateMeas,selfLocalization,headingMeas)
        else:
            Map2 = data2map(coordinateMeas,selfLocalization,headingMeas)
            Map= np.concatenate((Map,Map2),axis=1)
        mappingNumber = mappingNumber + 1
    else:
        continue
# %%
Map.shape
plt.figure(1)
plt.scatter(Map[0,:],Map[1,:])
plt.axis('equal')

plt.savefig('Map.png')
# %%

np.savetxt("Map.csv", Map, delimiter=",")

