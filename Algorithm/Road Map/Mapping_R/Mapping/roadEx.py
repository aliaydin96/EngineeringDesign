# %%
# %% 
import numpy as np
import os
from roadHelperX import *
import matplotlib.pyplot as plt

# %% 
var = np.array([1]); # measurement
cwd = os.getcwd()

a = np.zeros([5,1])
np.savetxt("totalData", a, delimiter=",")

#%%

 # data (radius(mm), theta(degree))
 # SL (x,y, heading(degree))
overflowIndex=np.array(0)
cruisePoint= []
for v in var:
    meas = np.genfromtxt(cwd+'\\'+'data'+'.csv',delimiter = ',')
#   sl = np.genfromtxt(cwd+'\\'+'SL_'+str(v)+'.csv',delimiter = ',')
    
    measLen=meas.shape[1]
    Theta=np.linspace(0,358.2,measLen)
    Theta.shape=(1,measLen)
    meas=(meas[0]+meas[1])/2
    meas.shape=(1,measLen)
    meas=np.concatenate((meas, Theta), axis=0)
    
    for i in range(measLen):
        if meas[0,i]>1100:
            overflowIndex=np.append(overflowIndex,i)
      
    
    
    
    meas=np.delete(meas,overflowIndex,axis=1)
    
    measLen=meas.shape[1] 
        
    sl_2=np.ones([3,measLen])
#    sl_2[0]*=sl[0]
#    sl_2[1]*=sl[1]
#    sl_2[2]*=sl[2]
    
    sl_2[0]*=0
    sl_2[1]*=0
    sl_2[2]*=0
    
        
    
#    sl_2=np.zeros([3,measLen])
    
    totalDataPerMeas= np.concatenate((meas, sl_2), axis=0)
    
    maxIndex=np.argmax(totalDataPerMeas[0],axis=0)
    
    destinationPoint= DestinationPoint(totalDataPerMeas[:,maxIndex])
    
    
    for i in range(totalDataPerMeas.shape[1]):
        a=totalDataPerMeas[1][maxIndex]-totalDataPerMeas[1][i]
        if -45<a<45 and totalDataPerMeas[0][i]*np.sin(np.deg2rad(abs(a)))<100:
            cruisePoint= np.append(cruisePoint,i)
 
    


    print(destinationPoint)
    print(cruisePoint.shape)
    print(cruisePoint)
    
    minPoint= totalDataPerMeas[0][maxIndex]
    
    for i in cruisePoint:
    
        if totalDataPerMeas[0][int(i)]<minPoint:
            max_Index=i
            
    destinationPoint= DestinationPoint(totalDataPerMeas[:,maxIndex])    
    print(destinationPoint)      

    
# %% 
x= [sl_2[0][0],destinationPoint[0]]
y=[sl_2[1][0],destinationPoint[1]]  

# Calculate the coefficients. This line answers the initial question. 
coefficients = np.polyfit(x, y, 1)

x_slide=100/np.sin(np.arctan(coefficients[0]))
y_slide=100/np.cos(np.arctan(coefficients[0]))

# Let's compute the values of the line...
polynomial = np.poly1d(coefficients)
x_axis = np.linspace(sl_2[0][0],destinationPoint[0],100)
y_axis = polynomial(x_axis)

coefficients[1]+=x_slide
polynomial = np.poly1d(coefficients)
x_axisL = np.linspace(sl_2[0][0]-x_slide,destinationPoint[0]-x_slide,100)
y_axisL = polynomial(x_axisL)+y_slide
L_line=np.concatenate(( [x_axisL],[y_axisL]), axis=0)


coefficients[1]-=2*x_slide
polynomial = np.poly1d(coefficients)
x_axisR = np.linspace(sl_2[0][0]+x_slide,destinationPoint[0]+x_slide,100)
y_axisR = polynomial(x_axisR)-y_slide
R_line=np.concatenate(([x_axisR],[y_axisR]), axis=0)


# ...and plot the points and the line
plt.plot(x_axis, y_axis)
plt.plot( x[0], y[0], 'go' )
plt.plot( x[1], y[1], 'go' )
plt.grid('on')

plt.plot(x_axisR, y_axisR)
plt.plot( x[0]-x_slide, y[0]+y_slide, 'go' )
plt.plot( x[1]-x_slide, y[1]+y_slide, 'go' )
plt.grid('on')

plt.plot(x_axisL, y_axisL)
plt.plot( x[0]+x_slide, y[0]-y_slide, 'go' )
plt.plot( x[1]+x_slide, y[1]-y_slide, 'go' )
plt.grid('on')
plt.show()
  
    
    
# %% 
#Map=scan2map(totalDataPerMeas)
#plt.figure() 
#plt.scatter(Map[0,:],Map[1,:])
#
## %% 
#plt.polar(totalDataPerMeas[0,:],totalDataPerMeas[1,:])


