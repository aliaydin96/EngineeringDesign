import numpy as np
import math
data = np.genfromtxt('data6.csv',delimiter=',')
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

r_compare_max = 2704
r_compare_min = 1764
variation = round(math.atan(50/(50+rmin))*200/math.pi)-1
lower_index = rmin_ind-variation
upper_index = rmin_ind+variation
prob1 = 0
for i in range(lower_index,upper_index+1):
    r_next = math.pow((rmin+50),2)+math.pow(data[i],2)-2*data[i]*(rmin+50)*math.cos(math.pi*(i-rmin_ind)/200)
    if(r_compare_max >= r_next) & (r_compare_min <= r_next):
        prob1 = prob1 +1
prob1 = prob1/(upper_index-lower_index+1)

r_compare = 900
index_variation = round(math.atan(25/(25+rmin))*200/math.pi)-1
lower_index_small = rmin_ind-index_variation
upper_index_small = rmin_ind+index_variation

prob2 = 0
for i in range(lower_index_small,upper_index_small+1):
    r_next =  math.pow((rmin+25),2)+math.pow(data[i],2)-2*data[i]*(rmin+25)*math.cos(math.pi*(i-rmin_ind)/200)
    if(r_compare >= r_next):
        prob2 = prob2 +1

prob2 = prob2/(upper_index_small-lower_index_small+1)
if(prob1 >= 0.6):
    print("100 mm with center\n")
    #printing radius and theta in mm and radians
    print((rmin+50),(rmin_set*math.pi/200))
if((prob1 <= 0.6)&(prob2 >= 0.6)):
    print("50 mm with center\n")
    print((rmin+25),(rmin_set*math.pi/200))
