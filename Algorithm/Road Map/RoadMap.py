
# %%
clear
# %% 
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.axes as ma
import os.path
import math
from math import pi
import cv2
from skimage.exposure import rescale_intensity
import argparse
import scipy.signal as ss

# %% 

# %% 
# Load an color image in grayscale
img = cv2.imread('line1.PNG',0);
# %% 

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# %% 
print(img.shape)
shape=img.shape

# %% 
for i in range(shape[0]):
    for j in range(shape[1]):
        if img[i][j]>125:
            img[i][j]=255
        else:
            img[i][j]=0
            
# %%     

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# %% 
for i in range(shape[0]):
    for j in range(shape[1]):
        if img[i][j]>125:
            img[i][j]=1
        else:
            img[i][j]=0


# %% 
print(img)
# %% 
k=np.ones((20,20));

# %% 
centre= ss.convolve2d(img,k);
#%%
for i in range(centre.shape[0]):
    for j in range(centre.shape[1]):
        if centre[i][j]==1:
            centre[i][j]=1
            print(i,j)
        else:
            centre[i][j]=0
        
            

# %% 
img_2=centre*255;
cv2.imshow('image',img_2)
cv2.waitKey(0)
cv2.destroyAllWindows()

# %% 

