import RPi.GPIO as GPIO
import time
import numpy as np
import math
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#variable definition
rpmcount = 0
rpmcount2 = 0
rpmMotor1 = 0
rpmMotor2 = 0
x_position = 0
y_position = 0
x_pos_initial = 0
y_pos_initial = 0
angle = 0
anglesum = 0
rpmMotor1_initial = 0
rpmMotor2_initial = 0
motor1_rpm_change = 0
motor2_rpm_change = 0
#input definition
GPIO.setup(16, GPIO.IN)  
GPIO.setup(18, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(24, GPIO.IN)

def encoderDataMotor_1(A):
    global rpmcount
    encoderA = GPIO.input(16)
    encoderB = GPIO.input(18)
    if(encoderA == 1):
        if(encoderB == 1):
            rpmcount = rpmcount + 1
        else:
            rpmcount = rpmcount - 1
    else:
        if(encoderB == 0):
            rpmcount = rpmcount - 1
        else:
            rpmcount = rpmcount + 1
    return
            
def encoderDataMotor_2(A):
    global rpmcount2
    encoderA = GPIO.input(22)
    encoderB = GPIO.input(24)
    if(encoderA == 1):
        if(encoderB == 1):
            rpmcount2 = rpmcount2 + 1
        else:
            rpmcount2 = rpmcount2 - 1
    else:
        if(encoderB == 0):
            rpmcount2 = rpmcount2 - 1
        else:
            rpmcount2 = rpmcount2 + 1
    return
GPIO.add_event_detect(16, GPIO.RISING, callback = encoderDataMotor_1)
GPIO.add_event_detect(22, GPIO.RISING, callback = encoderDataMotor_2)
#GPIO.add_event_detect(18, GPIO.BOTH, callback = rpmmotor)
try:
    while True:
        rpmMotor1 = np.divide(rpmcount, 18.0)
        rpmMotor2 = np.divide(rpmcount2, 18.0)
        #print("rpm1: ",rpmMotor1,"rpm2: ",rpmMotor2)
        motor1_rpm_change = rpmMotor1 - rpmMotor1_initial
        motor2_rpm_change = rpmMotor2 - rpmMotor2_initial
        middlePoint = (motor1_rpm_change + motor2_rpm_change) / 2
        if((motor1_rpm_change >= 0) | (motor2_rpm_change >= 0)):
            angle = anglesum + (motor1_rpm_change - motor2_rpm_change) / 0.26
        else:
            angle = anglesum - (motor1_rpm_change - motor2_rpm_change) / 0.26
        
        x_position = middlePoint * np.cos(anglesum * np.pi /180) + x_pos_initial
        y_position = middlePoint * np.sin(anglesum * np.pi /180) + y_pos_initial

        anglesum = angle
        x_pos_initial = x_position
        y_pos_initial = y_position
        rpmMotor1_initial = rpmMotor1
        rpmMotor2_initial = rpmMotor2
    
        print("x pos:", x_position, "y pos: ", y_position, "heading: ", angle)
        
except KeyboardInterrupt:
    GPIO.cleanup()
#    rpmcount = 0
            



