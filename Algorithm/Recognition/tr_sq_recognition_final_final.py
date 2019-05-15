import numpy as np
import math

def recognit(forCounter,x_in,y_in,heading):
    data = np.genfromtxt('data'+str(forCounter)+'.csv',delimiter=',')
    pos_flag = 0
    heading-=math.pi/2
    global min_ind,max_ind
    theta = []
    for i in range(400):
      theta.append(i*math.pi/200)
    for i in range(400):
        if (data[i]==0):
            data[i] = 500
    rmin=min(data)
    rmin_ind=np.argmin(data)
    if(rmin_ind>370)|(rmin_ind<30):
      pos_flag = 1
      data = np.concatenate ((data[100:400], data[0:100]),axis=0)
      rmin=min(data)
      rmin_ind=np.argmin(data)
    for i in range(30):
      if(data[(rmin_ind+i)] < 240):
        max_ind = rmin_ind+i+1
      if(data[(rmin_ind-i)] < 240):
        min_ind = rmin_ind-i
    sel_r = data[min_ind:(max_ind+1)]
    sel_th = theta[min_ind:(max_ind+1)]
    rm_ind=np.argmin(sel_r)
    sel_x = np.multiply(sel_r,np.cos(sel_th))
    sel_y = np.multiply(sel_r,np.sin(sel_th))
    der = sel_r[1:len(sel_r)]-sel_r[0:(len(sel_r)-1)]
    filt_der = np.convolve(der,[1/3, 1/3, 1/3])
    filt_der = filt_der[1:(len(filt_der)-1)]
    xmin = sel_x[rm_ind]
    ymin = sel_y[rm_ind]
    p1x = sel_x[0]
    p1y = sel_y[0]
    p4x = sel_x[(len(sel_x)-1)]
    p4y = sel_y[(len(sel_y)-1)]
    rms = math.sqrt(sum(np.multiply(der,der))/len(der))
    rms = math.sqrt(rms)
    
    for i in range(1,len(der)):
      if(filt_der[i]>=-rms):
        p2x = sel_x[i]
        p2y = sel_y[i]
        break
    for i in range(1,len(der)):
      if(filt_der[(len(filt_der)-i)] <= rms):
        p3x = sel_x[(len(sel_r)-i)]
        p3y = sel_y[(len(sel_th)-i)]    
        break
    
    de1 = np.power((p1x-p2x),2)+np.power((p1y-p2y),2);
    de2 = np.power((p3x-p2x),2)+np.power((p3y-p2y),2);
    de3 = np.power((p4x-p3x),2)+np.power((p3y-p4y),2);
    dq1 = np.power((p1x-p3x),2)+np.power((p1y-p3y),2);
    dq2 = np.power((p2x-p4x),2)+np.power((p2y-p4y),2);
    a1 = (de1+de2-dq1)/(2*math.sqrt(de1*de2));
    a2 = (de3+de2-dq2)/(2*math.sqrt(de3*de2));
    a1 = math.acos(a1)*180/math.pi
    a2 = math.acos(a2)*180/math.pi
    orian = (p3x-p2x)*(p2x+p3x)+(p3y-p2y)*(p2y+p3y)
    orian = orian/(math.sqrt(de2*(np.power((p2x+p3x),2)+np.power((p2y+p3y),2))))
    orian = math.acos(orian)*180/math.pi
    d1 = np.power((ymin-p1y),2)+np.power((xmin-p1x),2)
    d2 = np.power((ymin-p4y),2)+np.power((xmin-p4x),2)
    corner_angle = np.power((p1x-p4x),2)+np.power((p1y-p4y),2);
    corner_angle = math.acos((d1+d2-corner_angle)/(2*math.sqrt(d1*d2)))
    corner_angle = corner_angle*180/math.pi;
  
    #classification
    if(de2 < 1300):
      if(corner_angle < 75):
          print("T cor.an= ",corner_angle)
          r_center = rmin+ 49.0748
          x_center = x_in+r_center*np.cos(math.pi*rmin_ind/200+heading+pos_flag*math.pi/2)
          y_center = y_in+r_center*np.sin(math.pi*rmin_ind/200+heading+pos_flag*math.pi/2)
          x_corner = x_in+rmin*np.cos(math.pi*rmin_ind/200+heading+pos_flag*math.pi/2)
          y_corner = y_in+rmin*np.sin(math.pi*rmin_ind/200+heading+pos_flag*math.pi/2)
          return x_center,y_center,x_corner,y_corner,0,rmin
          
      if(corner_angle > 75):
          print("S cor.an= ",corner_angle)
          r_center = rmin+49.5
          x_center = x_in+r_center*np.cos(math.pi*rmin_ind/200+heading+pos_flag*math.pi/2)
          y_center = y_in+r_center*np.sin(math.pi*rmin_ind/200+heading+pos_flag*math.pi/2)
          x_corner = x_in+rmin*np.cos(math.pi*rmin_ind/200+heading+pos_flag*math.pi/2)
          y_corner = y_in+rmin*np.sin(math.pi*rmin_ind/200+heading+pos_flag*math.pi/2)
          return x_center,y_center,x_corner,y_corner,1,rmin
          
    if((a1 >= 130)&(de1 > 400)):
      if(a2 < 80):
        print("T ed.an= ",a2)
        xc1 = p2x
        yc1 = p2y
        xc2 = p3x
        yc2 = p3y
        leng = math.sqrt(np.power((xc1-xc2),2)+np.power((yc1-yc2),2))
        unit_vectorx = 85*(xc1-xc2)/leng
        unit_vectory = 85*(yc1-yc2)/leng
        x_corner1 = xc2 + unit_vectorx
        y_corner1 = yc2 + unit_vectory
        x_corner2 = xc2
        y_corner2 = yc2
        r1 = math.sqrt(np.power(x_corner1,2)+np.power(y_corner1,2))
        t1 = np.arctan2(y_corner1,x_corner1)
        r2 = math.sqrt(np.power(x_corner2,2)+np.power(y_corner2,2))
        t2 = np.arctan2(y_corner2,x_corner2)
        x_corner1 = x_in+r1*np.cos(t1+heading+pos_flag*math.pi/2)
        y_corner1 = y_in+r1*np.sin(t1+heading+pos_flag*math.pi/2)
        x_corner2 = x_in+r2*np.cos(t2+heading+pos_flag*math.pi/2)
        y_corner2 = y_in+r2*np.sin(t2+heading+pos_flag*math.pi/2)
        return x_corner1,y_corner1,x_corner2,y_corner2,3,rmin
        
    if((a2 >= 130)&(de3 > 400)):
      if(a1 < 80):
        print("T ed.an= ",a1)
        xc1 = p2x
        yc1 = p2y
        xc2 = p3x
        yc2 = p3y
        leng = math.sqrt(np.power((xc1-xc2),2)+np.power((yc1-yc2),2))
        unit_vectorx = 85*(xc2-xc1)/leng
        unit_vectory = 85*(yc2-yc1)/leng
        x_corner2 = xc1 + unit_vectorx
        y_corner2 = yc1 + unit_vectory
        x_corner1 = xc1
        y_corner1 = yc1
        r1 = math.sqrt(np.power(x_corner1,2)+np.power(y_corner1,2))
        t1 = np.arctan2(y_corner1,x_corner1)
        r2 = math.sqrt(np.power(x_corner2,2)+np.power(y_corner2,2))
        t2 = np.arctan2(y_corner2,x_corner2)
        x_corner1 = x_in+r1*np.cos(t1+heading+pos_flag*math.pi/2)
        y_corner1 = y_in+r1*np.sin(t1+heading+pos_flag*math.pi/2)
        x_corner2 = x_in+r2*np.cos(t2+heading+pos_flag*math.pi/2)
        y_corner2 = y_in+r2*np.sin(t2+heading+pos_flag*math.pi/2)
        return x_corner1,y_corner1,x_corner2,y_corner2,3,rmin
        
    if(orian<90):
      rotation = 90-orian
      a = a1
      if((rotation >= 30)&(a <= 85)):
        print("T1 ")
        xc1 = p2x
        yc1 = p2y
        xc2 = p3x
        yc2 = p3y
        leng = math.sqrt(np.power((xc1-xc2),2)+np.power((yc1-yc2),2))
        unit_vectorx = 85*(xc2-xc1)/leng
        unit_vectory = 85*(yc2-yc1)/leng
        x_corner2 = xc1 + unit_vectorx
        y_corner2 = yc1 + unit_vectory
        x_corner1 = xc1
        y_corner1 = yc1
        r1 = math.sqrt(np.power(x_corner1,2)+np.power(y_corner1,2))
        t1 = np.arctan2(y_corner1,x_corner1)
        r2 = math.sqrt(np.power(x_corner2,2)+np.power(y_corner2,2))
        t2 = np.arctan2(y_corner2,x_corner2)
        x_corner1 = x_in+r1*np.cos(t1+heading+pos_flag*math.pi/2)
        y_corner1 = y_in+r1*np.sin(t1+heading+pos_flag*math.pi/2)
        x_corner2 = x_in+r2*np.cos(t2+heading+pos_flag*math.pi/2)
        y_corner2 = y_in+r2*np.sin(t2+heading+pos_flag*math.pi/2)
        return x_corner1,y_corner1,x_corner2,y_corner2,3,rmin
    
    if(orian>90):
      rotation = orian-90
      a = a2
      if((rotation >= 30)&(a <= 85)):
        print("T1 ")
        xc1 = p2x
        yc1 = p2y
        xc2 = p3x
        yc2 = p3y
        leng = math.sqrt(np.power((xc1-xc2),2)+np.power((yc1-yc2),2))
        unit_vectorx = 85*(xc1-xc2)/leng
        unit_vectory = 85*(yc1-yc2)/leng
        x_corner1 = xc2 + unit_vectorx
        y_corner1 = yc2 + unit_vectory
        x_corner2 = xc2
        y_corner2 = yc2
        r1 = math.sqrt(np.power(x_corner1,2)+np.power(y_corner1,2))
        t1 = np.arctan2(y_corner1,x_corner1)
        r2 = math.sqrt(np.power(x_corner2,2)+np.power(y_corner2,2))
        t2 = np.arctan2(y_corner2,x_corner2)
        x_corner1 = x_in+r1*np.cos(t1+heading+pos_flag*math.pi/2)
        y_corner1 = y_in+r1*np.sin(t1+heading+pos_flag*math.pi/2)
        x_corner2 = x_in+r2*np.cos(t2+heading+pos_flag*math.pi/2)
        y_corner2 = y_in+r2*np.sin(t2+heading+pos_flag*math.pi/2)
        return x_corner1,y_corner1,x_corner2,y_corner2,3,rmin
        
    ax1 = np.power((p2x-xmin),2)+np.power((p2y-ymin),2)
    ay1 = np.power((p1x-xmin),2)+np.power((p1y-ymin),2)
    ay1 = (ax1+de1-ay1)/(2*math.sqrt(ax1*de1))
    ay1 = math.acos(ay1)*180/math.pi
    ax2 = np.power((p3x-xmin),2)+np.power((p3y-ymin),2)
    ay2 = np.power((p4x-xmin),2)+np.power((p4y-ymin),2)
    ay2 = (ax2+de3-ay2)/(2*math.sqrt(ax2*de3))
    ay2 = math.acos(ay2)*180/math.pi
    
    if((ay1>155)&(ay2>155)):
      if(corner_angle <= 75):
        print("SX")
        r_center = rmin+49.5
        x_center = x_in+r_center*np.cos(math.pi*rmin_ind/200+heading+pos_flag*math.pi/2)
        y_center = y_in+r_center*np.sin(math.pi*rmin_ind/200+heading+pos_flag*math.pi/2)
        x_corner = x_in+rmin*np.cos(math.pi*rmin_ind/200+heading+pos_flag*math.pi/2)
        y_corner = y_in+rmin*np.sin(math.pi*rmin_ind/200+heading+pos_flag*math.pi/2)
        return x_center,y_center,x_corner,y_corner,1,rmin
        
    if(math.sqrt(de2) >= 69):
      print("T2 ")
      xc1 = p2x
      yc1 = p2y
      xc2 = p3x
      yc2 = p3y
      leng = math.sqrt(np.power((xc1-xc2),2)+np.power((yc1-yc2),2))
      unit_vectorx = 85*(xc1-xc2)/leng
      unit_vectory = 85*(yc1-yc2)/leng
      x_corner1 = xc2 + unit_vectorx
      y_corner1 = yc2 + unit_vectory
      x_corner2 = xc2
      y_corner2 = yc2
      r1 = math.sqrt(np.power(x_corner1,2)+np.power(y_corner1,2))
      t1 = np.arctan2(y_corner1,x_corner1)
      r2 = math.sqrt(np.power(x_corner2,2)+np.power(y_corner2,2))
      t2 = np.arctan2(y_corner2,x_corner2)
      x_corner1 = x_in+r1*np.cos(t1+heading+pos_flag*math.pi/2)
      y_corner1 = y_in+r1*np.sin(t1+heading+pos_flag*math.pi/2)
      x_corner2 = x_in+r2*np.cos(t2+heading+pos_flag*math.pi/2)
      y_corner2 = y_in+r2*np.sin(t2+heading+pos_flag*math.pi/2)
      return x_corner1,y_corner1,x_corner2,y_corner2,3,rmin
    print("left, rigth")
    if(orian<90):
        return  8, 8, 8, 8, 8,rmin
    if(orian>90):
        return  9, 9, 9, 9, 9,rmin
