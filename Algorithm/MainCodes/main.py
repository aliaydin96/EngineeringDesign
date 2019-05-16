from Self_Localization import *
from Environment_Sensing_Unit import *
from motor import *
from Destination import *
from RoadMap import *
import numpy as np
from mapPlot import *
from tr_sq_recognition import *
import math
from detection import *
from Destination import *
import os

for i in range(20):
    try:
        os.remove("data"+str(i)+".csv")
        os.remove("data"+str(i)+".txt")
        os.remove("data"+str(i)+"Wall.csv")
    except OSError:
        pass

x_position_initial = 0
y_position_initial =0
angle_initial=90
desired_x_position = 0
desired_y_position = 0
finishCounter=0
p=0
k=0
pastSL=np.zeros((2,1))
pastObje=np.zeros((2,1))
objeM=4*np.ones((1,5))
pastObjeCoordinateY = []
pastObjeCoordinateX = []
np.asarray(pastObjeCoordinateX)
np.asarray(pastObjeCoordinateY)
for forCounter in range(2):
    
#    self_localization_part(x_position,y_position,angle,desired_x_position,desired_y_position,forCounter)
    [x_position,y_position ,angle] = self_localization_part(x_position_initial,y_position_initial,angle_initial,desired_x_position,desired_y_position,forCounter)
    print("x_pos ",x_position,"y_pos ",y_position,"angle ",angle)
    x_position_initial = x_position
    y_position_initial = y_position
    angle_initial = angle
    ESU(forCounter)
    dataName="data"+str(forCounter)
    b=np.ones((2,1))
    b[0][0]=x_position_initial
    b[1][0]=y_position_initial
    pastSL=np.concatenate((pastSL,b),axis=1)
    
    objeCordinates, destinationPoints =dataMeas(dataName,pastSL)
    print("obje Cordinates ADPM",objeCordinates)
#    for j in range(objeCordinates.shape[0]):
#        pastObjeCoordinateX = np.append(pastObjeCoordinateX,objeCordinates[j][0])
#        pastObjeCoordinateY = np.append(pastObjeCoordinateY,objeCordinates[j][1])
        
    if p==1:
        xc1,yc1,xc2,yc2,modeC,rmin=detection(forCounter,x_position_initial,y_position_initial,angle*math.pi/180)
        print(xc1,yc1,xc2,yc2,modeC)
        if(rmin<120):
            desired_x_position = x_position_initial + (280 - rmin)*math.cos(angle*math.pi/180 - math.pi)
            desired_y_position = y_position_initial + (280 - rmin)*math.sin(angle*math.pi/180 - math.pi)
            [x_position,y_position ,angle] = self_localization_part(x_position_initial,y_position_initial,angle_initial,desired_x_position,desired_y_position,forCounter)
            print("x_pos ",x_position,"y_pos ",y_position,"angle ",angle)
            x_position_initial = x_position
            y_position_initial = y_position
            angle_initial = angle
            xc1,yc1,xc2,yc2,modeC,rmin=detection(forCounter,x_position_initial,y_position_initial,angle*math.pi/180)
            print(xc1,yc1,xc2,yc2,modeC)            
        elif(rmin>180):
            desired_x_position = x_position_initial + (rmin)*math.cos(angle*math.pi/180)
            desired_y_position = y_position_initial + (rmin)*math.sin(angle*math.pi/180)
            [x_position,y_position ,angle] = self_localization_part(x_position_initial,y_position_initial,angle_initial,desired_x_position,desired_y_position,forCounter)
            print("x_pos ",x_position,"y_pos ",y_position,"angle ",angle)
            x_position_initial = x_position
            y_position_initial = y_position
            angle_initial = angle
            xc1,yc1,xc2,yc2,modeC,rmin=detection(forCounter,x_position_initial,y_position_initial,angle*math.pi/180)
            print(xc1,yc1,xc2,yc2,modeC)             
        dummy=np.array([xc1,yc1,xc2,yc2,modeC]).T
        dummy.shape=(1,5)
        objeM=np.concatenate((objeM,dummy),axis=0)
        if modeC==5:
            pastObje=np.delete(pastObje,-1,axis=1)
        p=0
    
    objeCordinates,p,k,finishCounter = destinationPoint(objeCordinates, destinationPoints, b,finishCounter,pastObje)
    print("obje Cordinates destination",objeCordinates)
    desired_x_position=objeCordinates[0][0]
    desired_y_position=objeCordinates[0][1]  
    if p==1:
        pastObje1=objeCordinates.T
        pastObje=np.concatenate((pastObje,pastObje1),axis=1)
    print("pastObje ",pastObje)
    
#    if k==1:
#        xc1,yc1,xc2,yc2,modeC=detection(forCounter,x_position_initial,y_position_initial,angle*math.pi/180)
#        print(xc1,yc1,xc2,yc2,modeC)
#        dummy=np.array([xc1,yc1,xc2,yc2,modeC]).T
#        dummy.shape=(1,5)
#        objeM=np.concatenate((objeM,dummy),axis=0)
#        k=0
    
    distance = math.sqrt((desired_x_position - x_position)**2 + (desired_y_position-y_position)**2)
    desired_angle = math.atan2((desired_y_position-y_position),(desired_x_position - x_position))
    
    if(distance > 500):
        desired_x_position = x_position + 300*math.cos(desired_angle)
        desired_y_position = y_position + 300*math.sin(desired_angle)
        if p==1:
            pastObje=np.delete(pastObje,-1,axis=1)
            p = 0
    print("desx: ",desired_x_position,"desy: ",desired_y_position )    
    plt.show()

    if finishCounter==2:
        break
    

print(objeM)
wallDetection(objeM) 
    

