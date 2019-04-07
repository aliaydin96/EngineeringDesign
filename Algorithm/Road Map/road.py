import numpy as np
var = (1,2,3)
'''
data types of csv files
measurement(radius,theta(degree))
'''
for v in var:
    meas=np.genfromtxt('data-'+str(v)+'.csv',delimiter=',')
    sl=np.genfromtxt('SL_'+str(v)+'.csv',delimiter=',')


np.genfromtxt('data-'+'1'+'.csv',delimiter=',')
