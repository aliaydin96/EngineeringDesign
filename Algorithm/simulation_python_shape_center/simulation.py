import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils



#%%
import scipy.io
mat = scipy.io.loadmat('MapX1.mat')
temp = []
dictlist = []

for key, value in mat.items():
    temp = [key,value]
    dictlist.append(temp)
dictlist = dictlist[3]
dictlist = dictlist[1][0]

mat2 = scipy.io.loadmat('MapY1.mat')
temp2 = []
dictlist2 = []

for key2, value2 in mat2.items():
    temp2 = [key2,value2]
    dictlist2.append(temp2)
dictlist2 = dictlist2[3]
dictlist2 = dictlist2[1][0]
dictlist2 = list(filter(lambda a: a != 0, dictlist2))
dictlist = list(filter(lambda a: a != 0, dictlist))

#%%
A = np.zeros((400,400))
for i in range (0,len(dictlist)):
    for j in range(0,len(dictlist)):
        if(i==j and dictlist[i]!=0 and dictlist2[j]!=0):
            A[dictlist[i]][dictlist2[j]]=1
        else:
            A[i][j]=0
plt.imshow(A,cmap = 'gray')
import scipy
scipy.misc.imsave('outfile.jpg', A)

#%%
img = cv2.imread('outfile.jpg',1)
#img = imutils.rotate(img,90)
#img = io.imread('cember.png')
small = cv2.resize(img, (0,0), fx=2.1, fy=2.1)
gray_dst = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
blurred = cv2.medianBlur(gray_dst,3)

edged = cv2.Canny(blurred, 60, 80)
edged = cv2.dilate(edged, None, iterations=65)
k = cv2.erode(edged, None, iterations=65)
k = cv2.morphologyEx(k, cv2.MORPH_OPEN, kernel)
k = cv2.morphologyEx(k, cv2.MORPH_CLOSE, kernel)

plt.imshow(k, cmap = 'gray')




#%%
im2, contours, hierarchy = cv2.findContours(k, cv2.RETR_LIST , cv2.CHAIN_APPROX_TC89_KCOS )

liste = []
font = cv2.FONT_HERSHEY_COMPLEX
#print(len(contours))

area_max= 0
font = cv2.FONT_HERSHEY_SIMPLEX  
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
#    print(len(approx))
#    print(approx)
    if(len(approx)<10):
        
        if(cv2.contourArea(cnt)>600):
    
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(small,(x,y),(x+w,y+h),(0,255,0),3)
            cv2.putText(small, "Circle", (x, y), font, 1, (0))
            M = cv2.moments(cnt)
#            cX = int(M["m10"] / M["m00"])-20
#            cY = int(M["m01"] / M["m00"])-20
            cX = int((x+w/2))
            cY = int((y+h/2))
            cv2.circle(small, (cX, cY), 5, (255, 255, 255), -1)
            cv2.putText(small, 'rectangle', (cX, cY), font, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(small, str(cX), (cX-45, cY-20), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(small, ',', (cX-15, cY-20), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)            
            cv2.putText(small, str(cY), (cX-10, cY-20), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            
            print(cX,cY)
            
    elif(len(approx)>10 and len(approx)<14 and cv2.contourArea(cnt)>600):
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(small,center,radius,(0,255,0),2)
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(small, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(small, 'circle', (cX, cY), font, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(small, str(cX), (cX-45, cY-20), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(small, ',', (cX-15, cY-20), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)            
        cv2.putText(small, str(cY), (cX-10, cY-20), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        
        print(cX,cY)
    elif(len(approx)<3):
        pass
    else:
#        rect = cv2.minAreaRect(cnt)
#        box = cv2.boxPoints(rect)
##        box = np.int0(box)
#        M = cv2.moments(cnt)
#        cX = int(M["m10"] / M["m00"])
#        cY = int(M["m01"] / M["m00"])
        
        approx2 = cv2.approxPolyDP(cnt, 0.15*cv2.arcLength(cnt, True), True)
        point1 = approx2[0]
        point2 = approx2[1]
        point3 = approx2[2]
        x1 = point1[0][0]
        y1 = point1[0][1]
        x2 = point2[0][0]
        y2 = point2[0][1]
        x3 = point3[0][0]
        y3 = point3[0][1]
              
                
        cX = int(x1-0.66*(x1-0.5*(x2+x3)))
        cY = int(y1-0.66*(y1-0.5*(y2+y3)))
        
        cv2.circle(small, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(small, 'triangle', (cX, cY), font, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(small, str(cX), (cX-45, cY-20), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(small, ',', (cX-15, cY-20), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)            
        cv2.putText(small, str(cY), (cX-10, cY-20), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
#        box_arr = np.array([box[1],box[2],box[3]])
#        cv2.drawContours(small, [box_arr], -1, (0,255,0), 5)
        cv2.drawContours(small, [approx2], -1, (0,255,0), 5)
        print(cX,cY)
        

cv2.imshow("shapes", small)
cv2.imshow("Threshold", k)
scipy.misc.imsave('resultant_map1.jpg', small)
cv2.waitKey(0)
cv2.destroyAllWindows()

