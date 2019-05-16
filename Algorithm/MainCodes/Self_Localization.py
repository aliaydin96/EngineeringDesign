import RPi.GPIO as GPIO
import time
import numpy as np
from motor import *
import csv
import math
import serial
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
baseSpeed = 0
maxMotorSpeed = 7
minMotorSpeed = -7
desired_length_initial = 0
#in1, in2, PWM, Stanby, (polarity of motors)
motor1 = Motor(40,36,32,38,True)
motor2 = Motor(35,37,33,38,False)
def PI_Heading_Controller(PI_desired_angle,PI_Angle):
    global counter, dutycycle_1_initial, dutycycle_2_initial
    global angle_error,past_angle_errors
    global baseSpeed,maxMotorSpeed,minMotorSpeed,motor_speed
    Kp = 0.5
    Ki = 0.05
    angle_error = PI_desired_angle - PI_Angle
    if (angle_error > 0): 
        if (abs(PI_desired_angle - PI_Angle) < abs(-360 + PI_desired_angle - PI_Angle)): angle_error = PI_desired_angle - PI_Angle
        else:  angle_error = -360 + PI_desired_angle - PI_Angle
    else:
        if(abs(PI_desired_angle - PI_Angle)< abs(360 + PI_desired_angle - PI_Angle)): angle_error = PI_desired_angle - PI_Angle
        else:  angle_error = 360 - (PI_desired_angle - PI_Angle)
   
    motor_speed = Kp * angle_error + Ki * np.sum(past_angle_errors) 
    dutycycle_1 = baseSpeed - motor_speed
    dutycycle_2 = baseSpeed + motor_speed
    if(dutycycle_1 >= maxMotorSpeed):         dutycycle_1 = maxMotorSpeed
    if(dutycycle_2 >= maxMotorSpeed):         dutycycle_2 = maxMotorSpeed
    if(dutycycle_1 <= minMotorSpeed):         dutycycle_1 = minMotorSpeed
    if(dutycycle_2 <= minMotorSpeed):         dutycycle_2 = minMotorSpeed    
    if(dutycycle_1 > dutycycle_1_initial):    dutycycle_1_initial += 1
    if(dutycycle_1 < dutycycle_1_initial):    dutycycle_1_initial -= 1
    if(dutycycle_2 > dutycycle_2_initial):    dutycycle_2_initial += 1
    if(dutycycle_2 < dutycycle_2_initial):    dutycycle_2_initial -= 1
    motor1.drive(dutycycle_1_initial)
    motor2.drive(dutycycle_2_initial)
    if((abs(angle_error)<20) &(counter<100)):
        minMotorSpeed = -3
        maxMotorSpeed = 3
        baseSpeed = 0 
    if((angle_error > -3) & (angle_error < 3)): counter += 1
    if((counter >= 100) & (counter <= 110)):
        baseSpeed = 10
        maxMotorSpeed = 20
        minMotorSpeed = 0
    
    past_angle_errors[5] = angle_error
    a =past_angle_errors[4]
    past_angle_errors[4] =  past_angle_errors[5]
    b=past_angle_errors[3]
    past_angle_errors[3] =  a
    a= past_angle_errors[2]
    past_angle_errors[2] =  b
    b=past_angle_errors[1]
    past_angle_errors[1] =  a
    past_angle_errors[0] =  b

def self_localization_part(x_position,y_position,anglesum,desired_x_position,desired_y_position,dataCounter):
    global counter, dutycycle_1_initial, dutycycle_2_initial
    global desired_length_initial
    global angle_error,past_angle_errors
    global baseSpeed,maxMotorSpeed,minMotorSpeed,motor_speed
    desired_angle = 0    
    #variable definition
    EncoderData = serial.Serial("/dev/ttyUSB0", 9600)
    EncoderData.write(b'3')
    rpmcount = 0
    rpmcount2 = 0
    rpmMotor1 = 0
    rpmMotor2 = 0
#    x_pos_initial = 0
#    y_pos_initial = 0
    angle = 0
    past_angle_errors = np.zeros(6)
    angle_error = 0
    rpmMotor1_initial = 0
    rpmMotor2_initial = 0
    motor1_rpm_change = 0
    motor2_rpm_change = 0
    motor_speed = 0
    dutycycle_1 = 0
    dutycycle_2 = 0
    dutycycle_1_initial=0
    dutycycle_2_initial  =0
    counter = 0
    encoderCounter = 0
    desired_angle = (math.atan2((desired_y_position - y_position) , (desired_x_position - x_position))) * 180 / math.pi
    if(desired_angle < 0):
        desired_angle += 360
    K = []
    K = np.asarray(K)
    time.sleep(3)
    try:
        while True:            
            desired_length = math.sqrt(math.pow((x_position - desired_x_position),2)+math.pow((y_position - desired_y_position),2))
#            if((counter >= 50) & (counter <= 60)|(20 >= desired_length)): 
            if(150 >= desired_length):  
                motor1.brake() #Short brake
                motor2.brake()                
                dutycycle_1_initial = 0
                dutycycle_2_initial = 0
                past_angle_errors = np.zeros(6)
                counter = 0
                baseSpeed = 0
                maxMotorSpeed = 7
                minMotorSpeed = -7
                position = [x_position,y_position ,anglesum]
                position = np.asarray(position)
                np.savetxt('data'+str(dataCounter)+'.txt', position, delimiter=',')
                return x_position,y_position ,anglesum                             
            if(encoderCounter == 10):
                try:
                    EncoderData.write(b'1')
                    rpmcount = int(EncoderData.readline())
                    EncoderData.write(b'2')
                    rpmcount2 = int(EncoderData.readline())
                except ValueError:
                    continue
                encoderCounter = 0
            else: encoderCounter += 1
            rpmMotor1 = rpmcount / 1.8432
            rpmMotor2 = rpmcount2 / 1.6750
            motor1_rpm_change = rpmMotor1 - rpmMotor1_initial
            motor2_rpm_change = rpmMotor2 - rpmMotor2_initial        
            middlePoint = (motor1_rpm_change + motor2_rpm_change) / 2
            if((motor1_rpm_change >= 0) | (motor2_rpm_change >= 0)):
                angle = (anglesum + (motor1_rpm_change - motor2_rpm_change) / 2.63)%360
            else:
                angle = (anglesum - (motor1_rpm_change - motor2_rpm_change) / 2.63)%360            
            x_position = (middlePoint) * math.cos(anglesum * math.pi /180) + x_position
            y_position = (middlePoint) * math.sin(anglesum * math.pi /180) + y_position              
            PI_Heading_Controller(desired_angle, angle)
           
            anglesum = angle
#            x_pos_initial = x_position
#            y_pos_initial = y_position
            rpmMotor1_initial = rpmMotor1
            rpmMotor2_initial = rpmMotor2
#            print("desired_angle",desired_angle,"error",angle_error)
#            print("x pos:", x_position, "y pos: ", y_position, "heading: ", angle, "error: ", angle_error,"deslen",desired_length)
            
    except KeyboardInterrupt:
        GPIO.cleanup()

        

                
