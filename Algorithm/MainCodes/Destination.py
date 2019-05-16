import numpy as np
import math
from matplotlib import pyplot as plt
# B is self_localization
def destinationPoint(objeCordinates, destinationPoints, b,finishCounter,pastObje):
    dist=np.array([])
    index=np.array([])
    p=0
    k=0

    for j in range(objeCordinates.shape[0]):
        deltX= objeCordinates[j][0]-b[0][0]
        deltY=objeCordinates[j][1]-b[1][0]
        fiOb= np.arctan2(deltY,deltX)
        rOb= np.sqrt(deltX*deltX+deltY*deltY)
        rOb=((rOb*rOb*rOb*1.24)/1000000) - (0.002286*rOb*rOb) + (1.904*rOb) -111
        objeCordinates[j][0]= b[0][0]+ rOb*np.cos(fiOb)
        objeCordinates[j][1]= b[1][0]+rOb*np.sin(fiOb)



    for i in range(pastObje.shape[1]):
          for j in range(objeCordinates.shape[0]):
              distance=np.sqrt((pastObje[0][i]-objeCordinates[j][0])**2 + (pastObje[1][i]-objeCordinates[j][1])**2) 
              if distance<400:
                  index=np.append(index,j)

    try:
        index=np.asarray(index)
        index= index.astype(int)
        objeCordinates=np.delete(objeCordinates,index,axis=0)
    except ValueError:
        print('No past Object')


    for i in range(objeCordinates.shape[0]):
        dist = np.append(dist,np.sqrt((objeCordinates[i][0] - b[0][0])**2+(objeCordinates[i][1] - b[1][0])**2))

    try:
        close=np.where(dist<200)
        close=np.asarray(close)
        close= close.astype(int)
        closeObje=np.argmin(objeCordinates[close])
        plt.scatter(objeCordinates[close][0],objeCordinates[close][0],s=40, c='b')
        print("Obje Detection")
        k=1
    except ValueError:
        print('No close object')

    try:
        index= np.where(dist>1200)
        index=np.asarray(index)
        index= index.astype(int)
        objeCordinates=np.delete(objeCordinates,index,axis=0)
    except ValueError:
        print ('No far object')

    dist=np.array([])
    for i in range(objeCordinates.shape[0]):
        dist = np.append(dist,np.sqrt((objeCordinates[i][0] - b[0][0])**2+(objeCordinates[i][1] - b[1][0])**2))


    try:
        minimum=np.argmin(dist)
        print(objeCordinates)
        D= objeCordinates[minimum]
        D.shape=(1,2)
        print("Yes")
        
#        plt.scatter(D[0][0],D[0][1],s=60,c='r')
#        plt.text(D[0][0],D[0][1],"Obje"+str(forCounter+1))
        p=1
        if D[0][0] ==0 and D[0][1]==0:
            D= destinationPoints
            D.shape=(1,2)
            print("bug2")
            finishCounter+=1

    except ValueError:
        D= destinationPoints
        D.shape=(1,2)
        print("bug")
        finishCounter+=1
#    pastObje1=D.T
#    pastObje=np.concatenate((pastObje,pastObje1),axis=1)

    return D,p,k,finishCounter
