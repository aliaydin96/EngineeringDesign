import serial
import RPi.GPIO as GPIO
import time
import math 
from motor import *
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

ser = serial.Serial("/dev/ttyUSB0", 115200)
dx1 = 0
dy1 = 0
dx2 = 0
dy2 = 0
x_avg = 0
y_avg = 0
x_avg_initial = 0
y_avg_initial = 0
x_avg_change = 0
y_avg_change = 0
length1 = 0
length2 = 0
length1_initial = 0
length2_initial = 0
length1_change = 0
length2_change = 0

xsum = 0
ysum = 0
xsum2 = 0
ysum2 = 0

angle = 0
anglesum = 90
x_position = 0
y_position = 0
middlePoint = 0
x_position_initial = 0
y_position_initial = 0
constant_divider_forMouse = 34.0
counter = 0

motor1 = Motor(40,36,32,38,True)
motor2 = Motor(35,37,33,38,False)
try:        
    while True:
    #    time_begin = time.time()
        dx1 = int(ser.readline())
        dy1 = -int(ser.readline())
        dx2 = int(ser.readline())
        dy2 = -int(ser.readline())
        dx1 = dx1 * constant_divider_forMouse / 255 
        dy1 = dy1 * constant_divider_forMouse / 255 
        dx2 = dx2 * constant_divider_forMouse / 255 
        dy2 = dy2 * constant_divider_forMouse / 255 
          
        length1 = math.sqrt(math.pow(dx1,2) + math.pow(dy1,2))
        length2 = math.sqrt(math.pow(dx2,2) + math.pow(dy2,2))
        
        dangle1 = 0.05
        dangle2 = 0.05
        dx1 = dx1 * math.cos(dangle1) - dy1 * math.sin(dangle1)
        dy1 = dx1 * math.sin(dangle1) + dy1 * math.cos(dangle1)
        dx2 = dx2 * math.cos(dangle2) + dy2 * math.sin(dangle2)
        dy2 = dx2 * math.sin(dangle2) + dy2 * math.cos(dangle2)
        x_avg = (dx1 + dx2) / 2
        y_avg = (dy1 + dy2) / 2 
       
        if((length1 >= 0) | (length2 >= 0)):
            angle = anglesum - (length1- length2) / 0.875

        else:
            angle = anglesum + (length1 - length2) / 0.875

        x_position = x_avg * math.cos(anglesum * math.pi / 180) - y_avg * math.sin(anglesum * math.pi / 180) + x_position_initial
        y_position = x_avg * math.sin(anglesum * math.pi / 180) + y_avg * math.cos(anglesum * math.pi / 180) + y_position_initial
        xsum = dx1 + xsum
        ysum = dy1 + ysum
        xsum2 = dx2 + xsum2
        ysum2 = dy2 + ysum2
        print("dx1: ", xsum, "dy1: ", ysum, "dx2: ", xsum2, "dy2: ",ysum2)
#        print("angle ", angle,"x position ", x_position,"y position ", y_position, "counter: ",counter)
#        inp = GPIO.input(18)
#        print(inp)
#        motor1.drive(counter)
#        motor2.drive(counter)
#        counter += 1
#        if(counter >= 5):
#            counter = 5
#        if(xsum > 100):
#            motor1.brake()
#            motor2.brake()
        anglesum = angle
        x_position_initial = x_position
        y_position_initial = y_position

    #    time_end = time.time()
    #    duration = time_end - time_begin
    #    print(duration)
    #    print("===========")
except KeyboardInterrupt:
    GPIO.cleanup()


