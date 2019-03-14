import serial
#import RPi.GPIO as GPIO
import time
import math 

ser = serial.Serial("/dev/ttyUSB0", 9600)
ser.baudrate = 9600

dy1 = 0
dx2 = 0
dy2 = 0
angle = 0
anglesum = 0
x_position = 0
y_position = 0
middlePoint = 0
x_position_initial = 0
y_position_initial = 0
constant_pos = 39
constant_neg = 30
while True:
#    time_begin = time.time()


    dx1 = int(ser.readline())
    if(dx1 > 0):
        dx1 = dx1 * constant_pos / 255
    else:
        dx1 = dx1 * constant_neg / 255
    dy1 = int(ser.readline())
    if(dy1 > 0):
        dy1 = dy1 * constant_pos / 255
    else:
        dy1 = dy1 * constant_neg / 255
    dx2 = int(ser.readline())
    if(dx2 > 0):
        dx2 = dx2 * constant_pos / 255
    else:
        dx2 = dx2 * constant_neg / 255
    dy2 = int(ser.readline())
    if(dy2 > 0):
        dy2 = dy2 * constant_pos / 255
    else:
        dy2 = dy2 * constant_neg / 255
        
        
    length1 = math.sqrt(math.pow(dx1,2) + math.pow(dy1,2))
    length2 = math.sqrt(math.pow(dx2,2) + math.pow(dy2,2))
    middlePoint = (length1 + length2) / 2
    x_avg = (dx1 + dx2) / 2
    y_avg = (dy1 + dy2) / 2
    if(dy1 >= 0):
        angle = anglesum - (length1 - length2) / 1.1

    else:
        angle = anglesum + (length1 - length2) / 1.1
 #       x_position = x_avg * math.cos(anglesum * math.pi / 180) - y_avg * math.sin(anglesum * math.pi / 180) + x_position_initial
 #       y_position = x_avg * math.sin(anglesum * math.pi / 180) - y_avg * math.cos(anglesum * math.pi / 180) + y_position_initial
    x_position = x_avg * math.cos(anglesum * math.pi / 180) - y_avg * math.sin(anglesum * math.pi / 180) + x_position_initial
    y_position = x_avg * math.sin(anglesum * math.pi / 180) + y_avg * math.cos(anglesum * math.pi / 180) + y_position_initial
    
    print("angle ", angle)
    print("x position ", x_position)
    print("y position ", y_position)
    anglesum = angle
    x_position_initial = x_position
    y_position_initial = y_position




#    time_end = time.time()
#    duration = time_end - time_begin
#    print(duration)
#    print("===========")