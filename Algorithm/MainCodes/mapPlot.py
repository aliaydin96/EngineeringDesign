import os
from numpy import genfromtxt
import math
import matplotlib.pyplot as plt
import os.path
import csv
from math import pi
import numpy as np
from scipy.spatial import ConvexHull

def wallDetection(obje):
    Wall=np.zeros((1,2))
#    plt.figure()
    for i in range(2):
        try:
            cwd = os.getcwd()
            src=cwd+'/'+"data"+str(i)+"Wall"+'.csv'
            b=np.genfromtxt(src,delimiter = ',')
            a=b.T
            Wall= np.concatenate((Wall,a),axis=0)
            
        except OSError:
            continue
    hull  =ConvexHull(Wall) 
    for simplex in hull.simplices:
        plt.plot(Wall[simplex,0],Wall[simplex,1],'b')
    
    for i in range(obje.shape[0]):
        if obje[i][4]==0:
            teX=np.zeros((4,1))
            teY=np.zeros((4,1))
            deltaX=obje[i][2]-obje[i][0]
            deltaY=obje[i][3]-obje[i][1]
            teX[0]=obje[i][2]
            teY[0]=obje[i][3]
            teX[1]= obje[i][0]+deltaX*np.cos(2*pi/3)-deltaY*np.sin(2*pi/3)
            teY[1]=obje[i][1] +deltaX*np.sin(2*pi/3)+deltaY*np.cos(2*pi/3)
            teX[2]= obje[i][0]+deltaX*np.cos(-2*pi/3)-deltaY*np.sin(-2*pi/3)
            teY[2]=obje[i][1] +deltaX*np.sin(-2*pi/3)+deltaY*np.cos(-2*pi/3)
            teX[3]=teX[0]
            teY[3]=teY[0]
            plt.plot(teX,teY)
            x_c=(teX[0]+teX[1]+teX[2])/3
            y_c=(teY[0]+teY[1]+teY[2])/3
            plt.text(x_c,y_c,str(int(x_c))+','+str(int(y_c)))
        if obje[i][4]==1:
            teX=np.zeros((5,1))
            teY=np.zeros((5,1))
            deltaX=obje[i][2]-obje[i][0]
            deltaY=obje[i][3]-obje[i][1]
            teX[0]=obje[i][2]
            teY[0]=obje[i][3]
            teX[1]= obje[i][0]+deltaX*np.cos(pi/2)-deltaY*np.sin(pi/2)
            teY[1]=obje[i][1] +deltaX*np.sin(pi/2)+deltaY*np.cos(pi/2)
            teX[2]= obje[i][0]+deltaX*np.cos(pi)-deltaY*np.sin(pi)
            teY[2]=obje[i][1] +deltaX*np.sin(pi)+deltaY*np.cos(pi)
            teX[3]= obje[i][0]+deltaX*np.cos(-pi/2)-deltaY*np.sin(-pi/2)
            teY[3]=obje[i][1] +deltaX*np.sin(-pi/2)+deltaY*np.cos(-pi/2)
            teX[4]=teX[0]
            teY[4]=teY[0]
            plt.plot(teX,teY)
            x_c=(teX[0]+teX[1]+teX[2]+teY[3])/4
            y_c=(teY[0]+teY[1]+teY[2]+teY[3])/4
            plt.text(x_c,y_c,str(int(x_c))+','+str(int(y_c)))
        if obje[i][4]==3:
            teX=np.zeros((4,1))
            teY=np.zeros((4,1))
            deltaX=obje[i][2]-obje[i][0]
            deltaY=obje[i][3]-obje[i][1]
            teX[0]=obje[i][0]
            teY[0]=obje[i][1]
            teX[1]= obje[i][0]+deltaX*np.cos(-pi/3)-deltaY*np.sin(-pi/3)
            teY[1]=obje[i][1] +deltaX*np.sin(-pi/3)+deltaY*np.cos(-pi/3)
            teX[2]=obje[i][2]
            teY[2]=obje[i][3]
            teX[3]=teX[0]
            teY[3]=teY[0]
            plt.plot(teX,teY)
            x_c=(teX[0]+teX[1]+teX[2])/3
            y_c=(teY[0]+teY[1]+teY[2])/3
            plt.text(x_c,y_c,str(int(x_c))+','+str(int(y_c)))
        if obje[i][4]==2:
            teX=np.zeros((5,1))
            teY=np.zeros((5,1))
            deltaX=obje[i][2]-obje[i][0]
            deltaY=obje[i][3]-obje[i][1]
            teX[0]=obje[i][0]
            teY[0]=obje[i][1]
            teX[1]= obje[i][0]+deltaX*np.cos(-pi/2)-deltaY*np.sin(-pi/2)
            teY[1]=obje[i][1] +deltaX*np.sin(-pi/2)+deltaY*np.cos(-pi/2)
            teX[2]= teX[1]+(teX[0]-teX[1])*np.cos(-pi/2)-(teY[0]-teY[1])*np.sin(-pi/2)
            teY[2]=teY[1] +(teX[0]-teX[1])*np.sin(-pi/2)+(teY[0]-teY[1])*np.cos(-pi/2)
            teX[3]=obje[i][2]
            teY[3]=obje[i][3]
            teX[4]=teX[0]
            teY[4]=teY[0]
            
            plt.plot(teX,teY)
            x_c=(teX[0]+teX[1]+teX[2]+teY[3])/4
            y_c=(teY[0]+teY[1]+teY[2]+teY[3])/4
            plt.text(x_c,y_c,str(int(x_c))+','+str(int(y_c)))
            
        if obje[i][4]==6:
            te= np.linspace(0,2*pi,360)
            x_5=np.zeros((360,1))
            y_5=np.zeros((360,1))
            for j in range(360):
                x_5[j][0]=obje[i][0]+25*np.cos(te[j])
                y_5[j][0]=obje[i][1]+25*np.sin(te[j])
            plt.plot(x_5,y_5)
            x_c=obje[i][0]
            y_c=obje[i][1]
            plt.text(x_c,y_c,str(int(x_c))+','+str(int(y_c)))
            
        if obje[i][4]==7:
            te= np.linspace(0,2*pi,360)
            x_10=np.zeros((360,1))
            y_10=np.zeros((360,1))
            for j in range(360):
                x_10[j][0]=obje[i][0]+50*np.cos(te[j])
                y_10[j][0]=obje[i][1]+50*np.sin(te[j])
            plt.plot(x_10,y_10)
            x_c=obje[i][0]
            y_c=obje[i][1]
            plt.text(x_c,y_c,str(int(x_c))+','+str(int(y_c)))
            
            
            
        else:
            pass
    plt.axis('equal')    
    plt.show()
        


