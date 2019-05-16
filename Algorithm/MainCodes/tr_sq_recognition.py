import numpy as np
import math

def recognit(forCounter,x_in,y_in,heading):
    flag = 0
    heading-=math.pi/2
    global min_ind,max_ind
    data = np.genfromtxt('data'+str(forCounter)+'.csv',delimiter=',')
    theta = []
    for i in range(400):
      theta.append(i*math.pi/200)
 
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
      print(rmin)

    for i in range(30):
      if(data[(rmin_ind+i)] < 400):
        max_ind = rmin_ind+i
        
#      else: return 4,4,4,4,4
      if(data[(rmin_ind-i)] < 400):
        min_ind = rmin_ind-i
#      else:  return 4,4,4,4,4

    sel_r = data[min_ind:(max_ind+1)]
    sel_th = theta[min_ind:(max_ind+1)]
    der = sel_r[1:(max_ind-min_ind+1)]-sel_r[0:(max_ind-min_ind)]
    filt_der = np.convolve(der,[1/3, 1/3, 1/3])
    filt_der = filt_der[1:(len(filt_der)-1)]
    turning_point = np.zeros((2,4))
    turning_point[:,0] = [sel_r[0],sel_th[0]]
    turning_point[:,3] = [sel_r[(len(sel_r)-1)],sel_th[(len(sel_th)-1)]]


    for i in range(1,len(der)):
      if(filt_der[i]>=-1):
        turning_point[0,1] = sel_r[i-1]
        turning_point[1,1] = sel_th[i-1]
        r_turn1=sel_r[i-1]
        t_turn1= sel_th[i-1]*(flag == 0)+(flag==1)*theta[i-1+300]
        break

    for i in range(1,len(der)):
      if(filt_der[(len(filt_der)-i-1)] <= 1):
        turning_point[0,2] = sel_r[(len(sel_r)-i)]
        turning_point[1,2] = sel_th[(len(sel_th)-i)]
        r_turn2=sel_r[(len(sel_r)-i)]
        t_turn2= sel_th[(len(sel_r)-i)]*(flag == 0)+(flag==1)*theta[(len(sel_r)-i)+300]
        
        break

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
    print(dise)

    dummy_an = an_tur1+an_tur2-180
    print("dummy = ", dummy_an)
    if(dise[1]<2209):
        if((dummy_an <= 52) & (dummy_an >= 30)):
            print("triangular w/ angle= ", dummy_an)
            r_center = rmin+46.1
            x_center = x_in+r_center*np.cos(theta[rmin_set]+heading)
            y_center = y_in+r_center*np.sin(theta[rmin_set]+heading)
            x_corner = x_in+rmin*np.cos(theta[rmin_set]+heading)
            y_corner = y_in+rmin*np.sin(theta[rmin_set]+heading)
            return x_center,y_center,x_corner,y_corner,0,rmin
      
        if((dummy_an <= 115) & (dummy_an >= 52.5)):
            print("square w/ angle= ", dummy_an)
            r_center = rmin+49.5
            x_center = x_in+r_center*np.cos(theta[rmin_set]+heading)
            y_center = y_in+r_center*np.sin(theta[rmin_set]+heading)
            x_corner = x_in+rmin*np.cos(theta[rmin_set]+heading)
            y_corner = y_in+rmin*np.sin(theta[rmin_set]+heading)
            return x_center,y_center,x_corner,y_corner,1,rmin
            print("distance = ", math.sqrt(dise[1]))
    if(dise[1]>=2209): 
        if ((an_tur1 >= 95)&(an_tur2 >= 95)):
            if((dise[1] < 4900)&((dise[1] >= 2209))):
                print('sqare w/ edge = ', math.sqrt(dise[1]))
                x_corner1=  x_in+r_turn1*np.cos(t_turn1+heading)
                y_corner1 = y_in+r_turn1*np.sin(t_turn1+heading)
                x_corner2 = x_in+r_turn2*np.cos(t_turn2+heading)
                y_corner2 = y_in+r_turn2*np.sin(t_turn2+heading)
                return x_corner1,y_corner1,x_corner2,y_corner2,2,rmin
            
            if((dise[1] >= 4900)&(dise[1] <= 9000)):
                print('triangular w/ edge = ', math.sqrt(dise[1]))
                x_corner1=  x_in+r_turn1*np.cos(t_turn1+heading)
                y_corner1 = y_in+r_turn1*np.sin(t_turn1+heading)
                x_corner2 = x_in+r_turn2*np.cos(t_turn2+heading)
                y_corner2 = y_in+r_turn2*np.sin(t_turn2+heading)
                return x_corner1,y_corner1,x_corner2,y_corner2,3,rmin
            
    return 4,4,4,4,5
        
