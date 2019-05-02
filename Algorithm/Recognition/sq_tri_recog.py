import numpy as np
import math

data = np.genfromtxt('data25.csv',delimiter=',')
theta = []
for i in range(400):
  theta.append(i*math.pi/200)
flag = 0
#data = np.concatenate ((data[357:400], data[0:357]),axis=0)
for i in range(400):
    if (data[i]==0):
        data[i] = 500


rmin=min(data)
rmin_ind=np.argmin(data)
rmin_set = rmin_ind

#rmin_ind=np.asarray(rmin_ind)
#rmin_ind=rmin_ind.astype(int)

if(rmin_ind>375)|(rmin_ind<20):
  flag = 1
  data = np.concatenate ((data[100:400], data[0:99]),axis=0)
  rmin=min(data)
  rmin_ind=np.argmin(data)
  #rmin_ind=np.asarray(rmin_ind)
  #rmin_ind=rmin_ind.astype(int)

for i in range(30):
  if(data[(rmin_ind+i)] < 250):
    max_ind = rmin_ind+i
  if(data[(rmin_ind-i)] < 250):
    min_ind = rmin_ind-i

sel_r = data[min_ind:(max_ind+1)]
sel_th = theta[min_ind:(max_ind+1)]
der = sel_r[1:(max_ind-min_ind+1)]-sel_r[0:(max_ind-min_ind)]
filt_der = np.convolve(der,[1/3, 1/3, 1/3])
filt_der = filt_der[1:(len(filt_der)-1)]
print("filt_der",len(filt_der))
turning_point = np.zeros((2,4))
turning_point[:,0] = [sel_r[0],sel_th[0]]
turning_point[:,3] = [sel_r[(len(sel_r)-1)],sel_th[(len(sel_th)-1)]]


for i in range(len(der)-1):
  if(filt_der[i]>=-1):
    turning_point[0,1] = sel_r[i-1]
    turning_point[1,1] = sel_th[i-1]
    break

for i in range(len(der)-1):
  if(filt_der[(len(filt_der)-i-1)] <= 1):
    turning_point[0,2] = sel_r[(len(sel_r)-i)]
    turning_point[1,2] = sel_th[(len(sel_th)-i)]
    break

print("turning_point",turning_point)

x_tur = np.multiply(turning_point[0,:],np.cos(turning_point[1,:]))
y_tur = np.multiply(turning_point[0,:],np.sin(turning_point[1,:]))


dis_tur1 = x_tur[1:4]-x_tur[0:3]
dis_tur1 = np.power(dis_tur1,2)
dis_tur2 = y_tur[1:4]-y_tur[0:3]
dis_tur2 = np.power(dis_tur2,2)
dise = dis_tur1+dis_tur2

dis1 = np.asarray([(x_tur[2]-x_tur[0])*(x_tur[2]-x_tur[0]), (x_tur[3]-x_tur[1])*(x_tur[3]-x_tur[1])])
dis2 = np.asarray([(y_tur[2]-y_tur[0])*(y_tur[2]-y_tur[0]), (y_tur[3]-y_tur[1])*(y_tur[3]-y_tur[1])])
disq = dis1+dis2

an_tur1 = (dise[0]+dise[1]-disq[0])/(2*math.sqrt(dise[0]*dise[1]))
an_tur2 = (dise[2]+dise[1]-disq[1])/(2*math.sqrt(dise[2]*dise[1]))

an_tur1 = np.degrees(abs(np.arccos(an_tur1)))
an_tur2 = np.degrees(abs(np.arccos(an_tur2)))
print("atur1",an_tur1,"an_tur2",an_tur2)

dummy_an = an_tur1+an_tur2-180

if(dise[1]<2209):
    if((dummy_an <= 75) & (dummy_an >= 50)):
        print("triangular w/ angle= ", dummy_an)
  
    if((dummy_an <= 105) & (dummy_an >= 80)):
        print("square w/ angle= ", dummy_an)

if(dise[1]>=2209): 
    if ((an_tur1 >= 95)&(an_tur2 >= 95)):
        if((dise(1,2) < 4900)&((dise(1,2) >= 2209))):
            print('sqare w/ edge = ', math.sqrt(dise[1]))
        
        if((dise(1,2) >= 4900)&(dise(1,2) <= 8100)):
            print('triangular w/ edge = ', math.sqrt(dise[1]))        
