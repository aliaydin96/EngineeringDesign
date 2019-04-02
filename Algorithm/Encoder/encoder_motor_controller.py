import RPi.GPIO as GPIO
import time
import numpy as np
from motor import *
import csv
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
Kp = 1.3
Kd = 0.8
desired_angle = 180
baseSpeed = 4
maxMotorSpeed = 8
minMotorSpeed = 0
#variable definition
headingArray = []
x_pos_array = []
y_pos_array = []
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
angle_error = 0
last_angle_error = 0
rpmMotor1_initial = 0
rpmMotor2_initial = 0
motor1_rpm_change = 0
motor2_rpm_change = 0
motor_speed = 0
dutycycle_1 = 0
dutycycle_2 = 0
xdata = []
ydata = []
headingdata = []
counter = 0
counter1 = 0
#input definition
GPIO.setup(24, GPIO.IN)  #encoder A (yellow)
GPIO.setup(26, GPIO.IN)  #encoder B (green)
GPIO.setup(29, GPIO.IN)  #encoder A (yellow)
GPIO.setup(31, GPIO.IN)  #encoder B (green)
#in1, in2, PWM, Stanby, (polarity of motors)
motor1 = Motor(40,36,32,38,True)
motor2 = Motor(35,37,33,38,False)
def PD_controller(angle):
    global counter
    global last_angle_error
    global desired_angle
    global counter1
    global angle_error
    angle_error = desired_angle - angle
    motor_speed = Kp * angle_error + Kd * (angle_error - last_angle_error)
    last_angle_error = angle_error
    dutycycle_1 = baseSpeed - motor_speed
    dutycycle_2 = baseSpeed + motor_speed
    
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

    

def encoderDataMotor_1(A):
    global rpmcount
    encoderA = GPIO.input(26)
    encoderB = GPIO.input(24)
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
    encoderA = GPIO.input(29)
    encoderB = GPIO.input(31)
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


GPIO.add_event_detect(26, GPIO.RISING, callback = encoderDataMotor_1)
GPIO.add_event_detect(29, GPIO.RISING, callback = encoderDataMotor_2)
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
        
        PD_controller(angle)
        
        headingArray.append(angle)
        x_pos_array.append(x_position)
        y_pos_array.append(y_position)
        if((angle_error > -1) & (angle_error < 1)):
            counter += 1
            
        if(counter >= 2000):
#        if(x_position >= 30):
#        desired_angle = 0
#        counter = 0
#        counter1 += 1
#    if(counter1 == 2):
            motor1.brake() #Short brake
            motor2.brake()
            np.asarray(headingArray)
            np.asarray(x_pos_array)
            np.asarray(y_pos_array)
            np.savetxt("headingAngle.csv", headingArray, delimiter = ",")
            np.savetxt("x_position.csv", x_pos_array, delimiter = ",")
            np.savetxt("y_position.csv", y_pos_array, delimiter = ",")
            break
        anglesum = angle
        x_pos_initial = x_position
        y_pos_initial = y_position
        rpmMotor1_initial = rpmMotor1
        rpmMotor2_initial = rpmMotor2
    
        print("x pos:", x_position, "y pos: ", y_position, "heading: ", angle, "counter: ", counter)
        
except KeyboardInterrupt:
    GPIO.cleanup()

            




