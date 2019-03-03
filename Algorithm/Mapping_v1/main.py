import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os.path
import math
from math import pi
# %%
# adding the cartesian and polar coordinate converter
# these functions take or give 'radians'
def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)
# %%
Mapping_Number = 1
Coordinate_Meas= 'Coordinate_Meas_'+ str(Mapping_Number)
Self_Localization='Self_Localization_Meas_'+ str(Mapping_Number)
Heading_Meas = 'Heading_Meas_' + str (Mapping_Number)

if os.path.isfile(Coordinate_Meas):
    #control the scanning data is there while
    my_scan = genfromtxt(Coordinate_Meas, delimiter=',')
    Self_Position = genfromtxt(Self_Localization, delimiter=',')
    Heading = genfromtxt(Heading_Meas, delimiter=',')

    OverAll_Map(my_scan,Self_Position, Heading)
    #print(Mapping_Number)
    Mapping_Number= Mapping_Number+1
else :
    pass
