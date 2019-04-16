# %% 
import numpy as np
import os
from numpy import genfromtxt
import math
import matplotlib.pyplot as plt
import os.path
import csv
from math import pi

#%% 
#cartesian and polar conversion 
#send cartesian and polar coordinate as 


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return np.array([rho,phi])


def pol2cart(rho, phi):
    
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return np.array([x,y])
    



#%%
# Collecting Data
# Data is 2 dimension distance matrices, measurement gives (2,200) matrices
cwd = os.getcwd()
src=cwd+'\\'+'data1'+'.csv'

measR = np.genfromtxt(src,delimiter = ',')
measLen=measR.shape[1]

meas=(measR[0]+measR[1])/2
meas.shape=(1,measLen)

#%% Eliminating meas
index=np.array([])
distance=(meas[0][0:measLen-1]- meas[0][1:measLen]);
average=  np.sum(abs(distance))/ (measLen-1);
discardFactor=0.65;

for i in range(measLen-1):
    if meas[0][i]>=2500:
        meas[0][i]=0
    if meas[0][i+1]>=2500:
        meas[0][i+1]=0
    if abs(meas[0][i+1]-meas[0][i])> discardFactor*average:
        index=np.append(index,i)

index= index.astype(int)
    
#%%

#%%

# define a theta angle 0-358.2 with data length
Theta=np.linspace(0,358.2,measLen)
Theta=np.radians(Theta)
Theta.shape=(1,measLen)

# concetanete the 2 distance matrices and theta matrices

meas=np.concatenate((meas, Theta), axis=0)
    
#%%
# Define Self Position and Self Localization
selfX= 0;
selfY= 0;
heading=0; #radian

selfX= selfX* np.ones([1,measLen]);
selfY= selfY* np.ones([1,measLen]);
heading= heading*np.ones([1,measLen]);

ADPM=np.concatenate((meas, selfX,selfY,heading), axis=0) # all data per each measurement


# %%  Drawing the measurement
coordinates=pol2cart(ADPM[0],(ADPM[1]+ADPM[4]))
coordinates[0]=coordinates[0]+ADPM[2]
coordinates[1]=coordinates[1]+ADPM[3]

plt.figure();
plt.scatter(coordinates[0],coordinates[1])
#b=-1000;
#t=1000;
#l=-1000;
#r=1000;
#plt.ylim((b,t))
#plt.xlim((l,r))
plt.scatter(ADPM[2][0],ADPM[3][0],s=60, c='r')
plt.text(ADPM[2][0],ADPM[3][0],'heading='+str(ADPM[4][0]))
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Data1( Purely Measurement) with Self Position of Robot')

plt.savefig('Data1( Purely Measurement)')


#%% delete the undesired measurement
ADPM= np.delete(ADPM,index,axis=1)

#%%

coordinates=pol2cart(ADPM[0],(ADPM[1]+ADPM[4]))
coordinates[0]=coordinates[0]+ADPM[2]
coordinates[1]=coordinates[1]+ADPM[3]

plt.figure();
plt.scatter(coordinates[0],coordinates[1])
#b=-1000;
#t=1000;
#l=-1000;
#r=1000;
#plt.ylim((b,t))
#plt.xlim((l,r))
plt.scatter(ADPM[2][0],ADPM[3][0],s=60, c='r')
plt.text(ADPM[2][0],ADPM[3][0],'heading='+str(ADPM[4][0]))
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Data1(Cleaning with average filter)')
plt.savefig('Data1(Cleaning with average filter)')


#%% finding the outermost point from robot self position
maxIndex=np.argmax(ADPM[0],axis=0) # it returns an integer

#%% control that th robot is moving at this point in straight line
cruisePoint=np.array([maxIndex]) # it is array if the destination point is not reachable point
for i in range(ADPM.shape[1]):
    thetaDif=ADPM[1][maxIndex]-ADPM[1][i]
    if -pi/2<thetaDif<pi/2 and ADPM[0][i]*abs(np.sin(thetaDif))<100 and ADPM[0][i] < ADPM[0][maxIndex]:
        cruisePoint= np.append(cruisePoint,i)
 
#%%
plt.figure();
plt.scatter(coordinates[0],coordinates[1])
#b=-1000;
#t=1000;
#l=-1000;
#r=1000;
#plt.ylim((b,t))
#plt.xlim((l,r))
plt.scatter(ADPM[2][0],ADPM[3][0],s=60, c='g')
plt.text(ADPM[2][0],ADPM[3][0],'heading='+str(ADPM[4][0]))
plt.scatter(coordinates[0][maxIndex],coordinates[1][maxIndex],s=60,c='r')
plt.text(coordinates[0][maxIndex],coordinates[1][maxIndex],'Destination Aim')
for c in cruisePoint :
    plt.scatter(coordinates[0][c],coordinates[1][c],s=10,c='g')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Decision of Destination Point')
plt.savefig('Destination Point Finding')

# %% numpy sorting R to find maximum
sortedRho=np.sort(ADPM[0])

for i in range(sortedRho.shape[0]-1):
    maxIndex=np.where(ADPM==sortedRho[-(i+1)])
    maxIndex=np.asarray(maxIndex)
    maxIndex=maxIndex[-1][-1]
    k=0;
    for j in range(ADPM.shape[1]):
        thetaDif=ADPM[1][maxIndex]-ADPM[1][j]
        if -pi/2<thetaDif<pi/2 and ADPM[0][j]*abs(np.sin(thetaDif))<100 and ADPM[0][j] < ADPM[0][maxIndex] and k==0:
            k=1;
    if k==0:
        maxIndice=maxIndex
        break


#%%
DestinationPoint=pol2cart(ADPM[0][maxIndice]-200,(ADPM[1][maxIndice]+ADPM[4][maxIndice]))
DestinationPoint[0]+=ADPM[2][maxIndice]
DestinationPoint[1]+=ADPM[3][maxIndice]     
        
plt.figure();
plt.scatter(coordinates[0],coordinates[1])
#b=-1000;
#t=1000;
#l=-1000;
#r=1000;
#plt.ylim((b,t))
#plt.xlim((l,r))
plt.scatter(ADPM[2][0],ADPM[3][0],s=60, c='g')
plt.text(ADPM[2][0],ADPM[3][0],'heading='+str(ADPM[4][0]))
plt.scatter(DestinationPoint[0],DestinationPoint[1],s=60,c='r')
plt.text(DestinationPoint[0],DestinationPoint[1],'Destination Final')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Final Destination Point')
plt.savefig('Destination Point Final')


