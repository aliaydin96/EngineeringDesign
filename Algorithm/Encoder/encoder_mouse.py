import RPi.GPIO as GPIO
import time
import numpy as np
from motor import *
import csv
import serial
import math

GPIO.setwarnings(False)
#definition for PD controller
Kp = 0.2
Kd = 0.1
Ki = 0.001
#sum_angle_error = 0
desired_angle = 0
desired_x_position = 0
desired_y_position = 0
baseSpeed = 4
maxMotorSpeed = 8
minMotorSpeed = 0
angle_error = 0
last_angle_error = 0
PD_Angle = 0
past_angle_errors = np.zeros(6)
#definition for mouse data
mouse = serial.Serial("/dev/ttyUSB0", 115200)
constant_divider_forMouse = 36.0
dx1 = 0
dy1 = 0
dx2 = 0
dy2 = 0
mouse_sum_x1 = 0
mouse_sum_y1 = 0
mouse_sum_x2 = 0
mouse_sum_y2 = 0
mouse_x_avg = 0
mouse_y_avg = 0
mouse_x_avg_initial = 0
mouse_y_avg_initial = 0
mouse_x_avg_change = 0
mouse_y_avg_change = 0
mouse_length1 = 0
mouse_length2 = 0
mouse_length1_initial = 0
mouse_length2_initial = 0
mouse_length1_change = 0
mouse_length2_change = 0

mouse_angle = 0
mouse_anglesum = 90
mouse_x_position = 0
mouse_y_position = 0
mouse_x_position_initial = 0
mouse_y_position_initial = 10
#definition for encoder data
rpmcount = 0
rpmcount2 = 0
rpmMotor1 = 0
rpmMotor2 = 0
encoder_x_position = 0
encoder_y_position = 0
encoder_x_pos_initial = 25
encoder_y_pos_initial = 0
middlePoint = 0
encoderAngle = 0
encoderAngleSum = 90
rpmMotor1_initial = 0
rpmMotor2_initial = 0
motor1_rpm_change = 0
motor2_rpm_change = 0
#definition for motor 
motor_speed = 0
dutycycle_1 = 0
dutycycle_2 = 0
dutycycle_1_initial = 0
dutycycle_2_initial = 0

counter = 0
counter1 = 0
#input definition
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN)  #arduino serial data interrupt pin
GPIO.setup(24, GPIO.IN)  #encoder A (yellow)
GPIO.setup(26, GPIO.IN)  #encoder B (green)
GPIO.setup(29, GPIO.IN)  #encoder A (yellow)
GPIO.setup(31, GPIO.IN)  #encoder B (green)
#in1, in2, PWM, Stanby, (polarity of motors)
motor1 = Motor(40,36,32,38,True)
motor2 = Motor(35,37,33,38,False)
def PI_controller(PI_desired_angle, PI_Angle):
    global counter
    global last_angle_error, angle_error
    global dutycycle_1_initial, dutycycle_2_initial
    past_angle_errors[5] =angle_error
    angle_error = PI_desired_angle - PI_Angle
    motor_speed = Kp * angle_error + Ki * np.sum(past_angle_errors)#Kd * (angle_error - last_angle_error)
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
    if(dutycycle_1 > dutycycle_1_initial):
        dutycycle_1 = dutycycle_1_initial + 1
    if(dutycycle_1 < dutycycle_1_initial):
        dutycycle_1 = dutycycle_1_initial - 1
    if(dutycycle_2 > dutycycle_2_initial):
        dutycycle_2 = dutycycle_2_initial + 1
    if(dutycycle_2 < dutycycle_2_initial):
        dutycycle_2 = dutycycle_2_initial - 1
    motor1.drive(dutycycle_1)
    motor2.drive(dutycycle_2)
    dutycycle_1_initial = dutycycle_1
    dutycycle_2_initial = dutycycle_2
    past_angle_errors[4] =  past_angle_errors[5]
    past_angle_errors[3] =  past_angle_errors[4]
    past_angle_errors[2] =  past_angle_errors[3]
    past_angle_errors[1] =  past_angle_errors[2]
    past_angle_errors[0] =  past_angle_errors[1]

def encoderDataMotor_1(A):
    global rpmcount
    encoderA = GPIO.input(24)
    encoderB = GPIO.input(26)
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

def mouseInterrupt(A):
    global mouse_sum_x1,mouse_sum_x2,mouse_sum_y1,mouse_sum_y2
    dx1 = int(mouse.readline()) * constant_divider_forMouse / 255
    dy1 = -int(mouse.readline()) * constant_divider_forMouse / 255
    dx2 = int(mouse.readline()) * constant_divider_forMouse / 255
    dy2 = -int(mouse.readline()) * constant_divider_forMouse / 255
    dangle1 = 0.02
    dangle2 = 0.02
    dx1 = dx1 * math.cos(dangle1) - dy1 * math.sin(dangle1)
    dy1 = dx1 * math.sin(dangle1) + dy1 * math.cos(dangle1)
    dx2 = dx2 * math.cos(dangle2) + dy2 * math.sin(dangle2)
    dy2 = dx2 * math.sin(dangle2) + dy2 * math.cos(dangle2)
    mouse_sum_x1 += dx1
    mouse_sum_y1 += dy1
    mouse_sum_x2 += dx2
    mouse_sum_y2 += dy2
    return

GPIO.add_event_detect(18, GPIO.RISING, callback = mouseInterrupt)
GPIO.add_event_detect(24, GPIO.FALLING, callback = encoderDataMotor_1)
GPIO.add_event_detect(29, GPIO.RISING, callback = encoderDataMotor_2)
time.sleep(5)
try:
    while True:
        if((10 >= abs(encoder_x_position - desired_x_position)) & (10 >= abs(encoder_y_position - desired_y_position))):  
            motor1.brake() #Short brake
            motor2.brake()
            past_angle_errors = np.zeros(6)
            desired_x_position = int(input("xpos: "))
            desired_y_position = int(input("ypos: "))
            
        rpmMotor1 = rpmcount / 1.79
        rpmMotor2 = rpmcount2 / 1.65
        motor1_rpm_change = rpmMotor1 - rpmMotor1_initial
        motor2_rpm_change = rpmMotor2 - rpmMotor2_initial
        middlePoint = (motor1_rpm_change + motor2_rpm_change) / 2
        if((motor1_rpm_change >= 0) | (motor2_rpm_change >= 0)):
            encoderAngle = (encoderAngleSum + (motor1_rpm_change - motor2_rpm_change) / 2.53)%360
        else:
            encoderAngle = (encoderAngleSum - (motor1_rpm_change - motor2_rpm_change) / 2.53)%360
        
        encoder_x_position = middlePoint * math.cos(encoderAngleSum * math.pi /180) + encoder_x_pos_initial
        encoder_y_position = middlePoint * math.sin(encoderAngleSum * math.pi /180) + encoder_y_pos_initial
        encoderAngleSum = encoderAngle
        encoder_x_pos_initial = encoder_x_position
        encoder_y_pos_initial = encoder_y_position
        rpmMotor1_initial = rpmMotor1
        rpmMotor2_initial = rpmMotor2        
        #####################################################
        mouse_length1 = math.sqrt(math.pow(mouse_sum_x1,2) + math.pow(mouse_sum_y1,2))
        mouse_length2 = math.sqrt(math.pow(mouse_sum_x2,2) + math.pow(mouse_sum_y2,2))
        mouse_x_avg = (mouse_sum_x1 + mouse_sum_x2) / 2
        mouse_y_avg = (mouse_sum_y1 + mouse_sum_y2) / 2
        mouse_length1_change = mouse_length1 - mouse_length1_initial   
        mouse_length2_change = mouse_length2 - mouse_length2_initial
        mouse_x_avg_change = mouse_x_avg - mouse_x_avg_initial
        mouse_y_avg_change = mouse_y_avg - mouse_y_avg_initial
       
        if((mouse_x_avg >= 0)):
            mouse_angle = (mouse_anglesum - (mouse_length1_change - mouse_length2_change) / 1.05) % 360
        else:
            mouse_angle = (mouse_anglesum + (mouse_length1_change - mouse_length2_change) / 1.05) % 360

        mouse_x_position = mouse_x_avg_change * math.cos(mouse_anglesum * math.pi / 180) - mouse_y_avg_change * math.sin(mouse_anglesum * math.pi / 180) + mouse_x_position_initial
        mouse_y_position = mouse_x_avg_change * math.sin(mouse_anglesum * math.pi / 180) + mouse_y_avg_change * math.cos(mouse_anglesum * math.pi / 180) + mouse_y_position_initial
#        desired_angle = (math.atan2((desired_y_position - mouse_y_position) , (desired_x_position - mouse_x_position))) * 180 / math.pi
#        desired_angle = (math.atan2((desired_y_position - encoder_y_position) , (desired_x_position - encoder_x_position))) * 180 / math.pi
        desired_angle = (math.atan2((desired_y_position - encoder_y_position) , (desired_x_position - encoder_x_position))) * 180 / math.pi

        if(mouse_angle > 180):
            mouse_angle = mouse_angle - 360
        if(encoderAngle > 180):
            encoderAngle -= 360
        PI_controller(desired_angle, encoderAngle)
            
        mouse_anglesum = mouse_angle
        mouse_x_position_initial = mouse_x_position
        mouse_y_position_initial = mouse_y_position
        mouse_length1_initial = mouse_length1
        mouse_length2_initial = mouse_length2
        mouse_x_avg_initial = mouse_x_avg
        mouse_y_avg_initial = mouse_y_avg
        #####################################################

        print("mouse x position ", mouse_x_position,"y position ", mouse_y_position, "mouse_angle ", mouse_angle)
    
        print("x pos:", encoder_x_position, "y pos: ", encoder_y_position, "heading: ", encoderAngle)
except KeyboardInterrupt:
    GPIO.cleanup()

            





