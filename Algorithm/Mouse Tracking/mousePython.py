import serial
#import RPi.GPIO as GPIO
import time
import math 
from motor import *
GPIO.setwarnings(False)

Kp = 0.5
Kd = 0.1
desired_angle = 30
baseSpeed = 5
maxMotorSpeed = 10
minMotorSpeed = 0
ser = serial.Serial("/dev/ttyUSB0", 115200)

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
constant_pos = 38
constant_neg = 38
counter = 0
angle_error = 0
last_angle_error = 0
#in1, in2, PWM, Stanby, (polarity of motors)
motor1 = Motor(40,36,32,38,False)
motor2 = Motor(35,37,33,38,False)
def PD_controller(angle):
    global counter
    global last_angle_error
    global desired_angle
    global counter1
    angle_error = desired_angle - angle
    motor_speed = Kp * angle_error + Kd * (angle_error - last_angle_error)
    last_angle_error = angle_error
    dutycycle_1 = baseSpeed + motor_speed
    dutycycle_2 = baseSpeed - motor_speed
    
    if(dutycycle_1 > maxMotorSpeed):
        dutycycle_1 = maxMotorSpeed
    if(dutycycle_2 > maxMotorSpeed):
        dutycycle_2 = maxMotorSpeed
    if(dutycycle_1 < minMotorSpeed):
        dutycycle_1 = minMotorSpeed
    if(dutycycle_2 < minMotorSpeed):
        dutycycle_2 = minMotorSpeed    
        
    motor1.drive(dutycycle_1)
    motor2.drive(dutycycle_2)


    if((angle_error > -3) & (angle_error < 3)):
        counter += 1
    if(counter >= 2000):
#        desired_angle = 0
#        counter = 0
#        counter1 += 1
#    if(counter1 == 2):
        motor1.brake() #Short brake
        motor2.brake()
try:        
    while True:
    #    time_begin = time.time()


        dx1 = int(ser.readline())
        if(dx1 > 0):
            dx1 = dx1 * constant_pos / 255
        else:
            dx1 = dx1 * constant_neg / 255
        dy1 = -int(ser.readline())
        if(dy1 > 0):
            dy1 = dy1 * constant_pos / 255
        else:
            dy1 = dy1 * constant_neg / 255
        dx2 = int(ser.readline())
        if(dx2 > 0):
            dx2 = dx2 * constant_pos / 255
        else:
            dx2 = dx2 * constant_neg / 255
        dy2 = -int(ser.readline())
        if(dy2 > 0):
            dy2 = dy2 * constant_pos / 255
        else:
            dy2 = dy2 * constant_neg / 255
            
            
        length1 = math.sqrt(math.pow(dx1,2) + math.pow(dy1,2))
        length2 = math.sqrt(math.pow(dx2,2) + math.pow(dy2,2))
        middlePoint = (length1 + length2) / 2
        x_avg = (dx1 + dx2) / 2
        y_avg = (dy1 + dy2) / 2
        if(dx1 >= 0):
            angle = anglesum - (length1 - length2) / 1

        else:
            angle = anglesum + (length1 - length2) / 1
     #       x_position = x_avg * math.cos(anglesum * math.pi / 180) - y_avg * math.sin(anglesum * math.pi / 180) + x_position_initial
     #       y_position = x_avg * math.sin(anglesum * math.pi / 180) - y_avg * math.cos(anglesum * math.pi / 180) + y_position_initial
        x_position = x_avg * math.cos(anglesum * math.pi / 180) - y_avg * math.sin(anglesum * math.pi / 180) + x_position_initial
        y_position = x_avg * math.sin(anglesum * math.pi / 180) + y_avg * math.cos(anglesum * math.pi / 180) + y_position_initial
    #    print("dx1: ", dx1, "dy1: ", dy1, "dx2: ", dx2, "dy2: ",dy2)
        print("angle ", angle,"x position ", x_position,"y position ", y_position, "counter: ",counter)
        PD_controller(angle)
    #    motor1.drive(counter) #Backwards 100% dutycycle
    #    motor2.drive(counter)
    #        
    #    if(counter == 7):
    #        counter = 7
    #    else:
    #        counter = counter + 1   
    #    if((x_position >= 100) | (y_position >= 100)):
    #        motor1.brake() #Short brake
    #        motor2.brake()
    #        motor1.standby(True) #Enable standby
    #        motor1.standby(False) #Disable standby
        anglesum = angle
        x_position_initial = x_position
        y_position_initial = y_position

    #    time_end = time.time()
    #    duration = time_end - time_begin
    #    print(duration)
    #    print("===========")
except KeyboardInterrupt:
    GPIO.cleanup()
