import os
from numpy import genfromtxt
import math
import matplotlib.pyplot as plt
import os.path
import csv
from math import pi
import numpy as np
from scipy.spatial import ConvexHull

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
def routeRunner(ADPMx,pastSL,alfa=pi/10,scale=2/4):
    iteration=4*pi/alfa # it creates the center point of route
    ADPMlen= ADPMx.shape[1]
    
    for i in range(ADPMlen):
        if int(ADPMx[0][i])==0 :
            ADPMx[0][i]=ADPMx[0][i-1]
    
    ADPMlen=int(ADPMlen/iteration)
    average=np.zeros((3,int(iteration)))
    for i in range(int(iteration)):
        
        if i<int(iteration)-1:
            average[1][i]=sum(ADPMx[0][int(i*ADPMlen):int((i+2)*ADPMlen)])
            average[0][i]=(i+1)*alfa/2
            try:
                average[1][i]/=len(np.nonzero(ADPMx[0][int(i*ADPMlen):int((i+2)*ADPMlen)]))
            except ZeroDivisionError:
                average[1][0]=0
            a=ADPMx[0][int(i*ADPMlen):int((i+2)*ADPMlen)]
            try:
                average[2][i]= np.min(a[np.nonzero(a)])*scale
            except ValueError:
                average[2][i]= 1000
                average[1][i]=15000
            
        else:
            average[1][i]= sum(ADPMx[0][-1*ADPMlen:1*ADPMlen])
            average[0][i]=(i+1)*alfa/2
            try :
                average[1][i]/=len(np.nonzero(ADPMx[0][int(i*ADPMlen):int((i+2)*ADPMlen)]))
            except ZeroDivisionError:
                average[1][0]=0
            a=ADPMx[0][int(i*ADPMlen):int((i+2)*ADPMlen)]
            try:
                average[2][i]= np.min(a[np.nonzero(a)])*scale
            except ValueError:
                average[2][i]= 1000
                average[1][i]=15000
                
    maximum=np.argmax(average[1],axis=0)    
    
    destinationPoints=pol2cart(average[2][maximum],(average[0][maximum]+ADPMx[4][0]))
    destinationPoints[0]+=ADPMx[2][0]
    destinationPoints[1]+=ADPMx[3][0]
    lenSL=pastSL.shape[1]
    plt.figure()
    
    for i in range(lenSL):
        if pastSL[0][i]-500 > destinationPoints[0] and  destinationPoints[0] < pastSL[0][i]+500 and pastSL[1][i]-500 > destinationPoints[0] and  destinationPoints[0] < pastSL[1][i]+500 :
            continue
        else:
#            plt.text(destinationPoints[0],destinationPoints[1],'Past Destinations')
            plt.scatter(destinationPoints[0],destinationPoints[1], s=100)
            average[1][maximum]=0
            maximum=np.argmax(average[1],axis=0)    
            destinationPoints=pol2cart(average[2][maximum],(average[0][maximum]+ADPMx[4][0]))
            destinationPoints[0]+=ADPMx[2][0]
            destinationPoints[1]+=ADPMx[3][0]
#            plt.text(destinationPoints[0],destinationPoints[1],'Real Destination')
#            plt.scatter(destinationPoints[0],destinationPoints[1], s=100)
            
    
    return destinationPoints

#%%
    
def ADPMcreater(measurement,SelfLocalization):
    
#%% measurement and selfLocalization are 'strings' that indicate data csv files name
    
    dataName=measurement
    cwd = os.getcwd()
    src=cwd+'/'+dataName+'.csv'
    
    meas = np.genfromtxt(src,delimiter = ',')
    measLen=meas.shape[0]
    meas.shape=(1,measLen)

#%%
    sL=SelfLocalization
    src=cwd+'/'+sL+'.txt'
    sL=np.genfromtxt(src,delimiter = ',')
    
    selfX= sL[0]
    selfY= sL[1]
    heading=sL[2] # if it is degrre, it must be converted to radian
    heading=np.radians(heading)
       
#%%
    measDummy=meas
    index=np.array([])
    distance=(measDummy[0][0:measLen-1]- measDummy[0][1:measLen]);
    average=  np.sum(abs(distance))/ (measLen-1);
    discardFactor=0.6;
    
    for i in range(measLen-1):
        if measDummy[0][i]>=2500:
            measDummy[0][i]=0
        if measDummy[0][i+1]>=2500:
            measDummy[0][i+1]=0
        if abs(measDummy[0][i+1]-measDummy[0][i])> discardFactor*average:
            index=np.append(index,i)
        if measDummy[0][i] <10:
            index=np.append(index,i)
    
    index= index.astype(int)
    meas=measDummy

#%%
    
    # define a theta angle 0-358.2 with data length
    theta=np.linspace(0,359.1,measLen)
    theta=np.radians(theta)
    theta.shape=(1,measLen)
    
    # concetanete the 2 distance matrices and theta matrices
    
    meas=np.concatenate((meas, theta), axis=0)

#%%
# Define Self Position and Self Localization
    selfX= selfX* np.ones([1,measLen]);
    selfY= selfY* np.ones([1,measLen]);
    heading= heading*np.ones([1,measLen])-(pi/2);
    
    ADPM=np.concatenate((meas, selfX,selfY,heading), axis=0) # all data per each measurement
    
    ADPMlen=ADPM.shape[1]
    
    
    return ADPM, index,selfX,selfY,heading

#%%
    
def dataMeas(dataName,pastSL=np.zeros((2,1))):
    
    ADPM, index ,selfX,selfY,heading=ADPMcreater(dataName,dataName)
    
    destinationPoints=routeRunner(ADPM,pastSL,pi/24)
    
#    print(destinationPoints[0],destinationPoints[1])
    
    
    ADPM, index,selfX,selfY,heading =ADPMcreater(dataName,dataName)
    
    #%%
    ADPM= np.delete(ADPM,index,axis=1)
    
    
    #%%
    ADPMlen=ADPM.shape[1]
    startingPoint=np.array([])
    endingPoint=np.array([])
    k=0
    distance=(ADPM[0][0:ADPMlen-1]- ADPM[0][1:ADPMlen]);
    average=np.sum(abs(distance))/ (ADPMlen-1);
    discardFactor=2
    # a=ADPMlen-1
    
    for i in range(ADPMlen-1):
        if ADPM[0][i+1]-ADPM[0][i]<0 and abs(ADPM[0][i+1]-ADPM[0][i])>average*discardFactor and k==0:
            startingPoint=np.append(startingPoint,i+2)
            k=1
               
        if ADPM[0][i+1]-ADPM[0][i]>0 and abs(ADPM[0][i+1]-ADPM[0][i])> average*discardFactor and k==1:
            endingPoint=np.append(endingPoint,i+1)
            k=0
            
    if startingPoint.shape[0] != endingPoint.shape[0]:
        endingPoint=np.append(endingPoint,ADPMlen-1)
        
    #%%
        
    startingPoint.shape=(startingPoint.shape[0],1)
    endingPoint.shape=(endingPoint.shape[0],1)
    k=np.array([])
    for i in range(startingPoint.shape[0]):
        if abs(endingPoint[i][0]-startingPoint[i][0])>20:
            k=np.append(k,i)
    
    k=k.astype(int)    
    obje=np.concatenate((startingPoint,endingPoint),axis=1)
    obje=obje.astype(int)
    obje=np.delete(obje,k,axis=0)
    obje.shape=(obje.shape[0],2)
    numberObject=obje.shape[0]
    MinimumPoints= np.zeros([numberObject,1])
    #plt.figure()
    objeCordinates=np.zeros([numberObject,2])
    for i in range(numberObject):
        coordinates=pol2cart(ADPM[0][obje[i][0]:obje[i][1]],(ADPM[1][obje[i][0]:obje[i][1]])+ADPM[4][obje[i][0]:obje[i][1]])
        coordinates[0]+=ADPM[2][0]
        coordinates[1]+=ADPM[3][0]
        try:
            MinimumPoints[i,0]=obje[i][0]+np.argmin(ADPM[0][obje[i][0]:obje[i][1]])
        except ValueError:
            continue
        MinimumPoints= MinimumPoints.astype(int)
        x,y=pol2cart(ADPM[0][MinimumPoints[i,0]],ADPM[1][MinimumPoints[i,0]]+ADPM[4][0])
        objeCordinates[i][0]=x+ADPM[2][0]
        objeCordinates[i][1]=y+ADPM[3][0]
        objeCSV= dataName+"obje"+str(i)+".csv"
#        np.savetxt(objeCSV, coordinates,delimiter=",")
        plt.scatter(coordinates[0],coordinates[1])
        plt.scatter(ADPM[2][0],ADPM[3][0],s=60, c='r')
        plt.xlabel('X')
        plt.ylabel('Y')
#    print(numberObject)
#    print(MinimumPoints)
#    print(objeCordinates)
    
    #%%
    coordinates=pol2cart(ADPM[0],np.mod((ADPM[1]+ADPM[4]),2*pi))
    coordinates[0]=coordinates[0]+ADPM[2]
    coordinates[1]=coordinates[1]+ADPM[3]
    name= dataName+"XY"+".csv"
#    np.savetxt(name, coordinates,delimiter=",")
    plt.scatter(coordinates[0],coordinates[1],s=5)
    plt.scatter(ADPM[2][0],ADPM[3][0],s=60, c='r')
    plt.xlabel('X')
    plt.ylabel('Y')  
    
    #%%
    wallIndex=np.array([])
    for i in range(endingPoint.shape[0]):
        for j in range(int(endingPoint[i][0]-startingPoint[i][0])):
            wallIndex=np.append(wallIndex, startingPoint[i][0]+j)
            
            
    wallCordinates= np.delete(coordinates, wallIndex, axis=1)
    
#    plt.scatter(wallCordinates[0],wallCordinates[1],s=5, c='r')
    
    name=dataName+"Wall"+".csv"
    np.savetxt(name, coordinates,delimiter=",")
    hull=ConvexHull(wallCordinates.T)
#    for simplex in hull.simplices:
#        plt.plot(wallCordinates.T[simplex,0],wallCordinates.T[simplex,1])
        
    return objeCordinates, destinationPoints


