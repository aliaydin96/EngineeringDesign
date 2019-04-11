import RPi.GPIO as GPIO
import time
import numpy as np
from motor import *
import csv
import math
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
Kp = 1
Kd = 0.8
Ki = 0.01

desired_x_position = 0
desired_y_position = 0
baseSpeed = 5
maxMotorSpeed = 10
minMotorSpeed = 0
desired_angle = 0
interCounter = 0
interCounter2 = 0
loopcounter = 0
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
past_angle_errors = np.zeros(6)
anglesum = 90
angle_error = 0
last_angle_error = 0
rpmMotor1_initial = 0
rpmMotor2_initial = 0
motor1_rpm_change = 0
motor2_rpm_change = 0
motor_speed = 0
dutycycle_1 = 0
dutycycle_2 = 0
dutycycle_1_initial=0
dutycycle_2_initial  =0
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
def PI_controller(PI_desired_angle,PI_angle):
    global counter, dutycycle_1_initial, dutycycle_2_initial
    global last_angle_error
    global counter1
    global angle_error
    angle_error = PI_desired_angle - PI_angle
    past_angle_errors[5] =angle_error
    motor_speed = Kp * angle_error + Ki * np.sum(past_angle_errors)##Kd * (angle_error - last_angle_error)#
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
    if((angle_error > -1) & (angle_error < 1)):
        counter += 1
    past_angle_errors[4] =  past_angle_errors[5]
    past_angle_errors[3] =  past_angle_errors[4]
    past_angle_errors[2] =  past_angle_errors[3]
    past_angle_errors[1] =  past_angle_errors[2]
    past_angle_errors[0] =  past_angle_errors[1]

    
def encoderDataMotor_1(A):
    global rpmcount,rpmMotor1, interCounter
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
    
    interCounter += 1
    return
#            
def encoderDataMotor_2(A):
    global rpmcount2,rpmMotor2, interCounter2
    encoderA2 = GPIO.input(29)
    encoderB2 = GPIO.input(31)
    if(encoderA2 == 1):
        if(encoderB2 == 1):
            rpmcount2 = rpmcount2 + 1
        else:
            rpmcount2 = rpmcount2 - 1
    else:
        if(encoderB2 == 0):
            rpmcount2 = rpmcount2 - 1
        else:
            rpmcount2 = rpmcount2 + 1
    
    interCounter2 += 1
    return
GPIO.add_event_detect(24, GPIO.FALLING, callback = encoderDataMotor_1)
GPIO.add_event_detect(29, GPIO.RISING, callback = encoderDataMotor_2)
try:
    while True:
        if((10 >= abs(x_position - desired_x_position)) & (10 >= abs(y_position - desired_y_position))):  
            motor1.brake() #Short brake
            motor2.brake()
            desired_x_position = int(input("xpos: "))
            desired_y_position = int(input("ypos: "))
        rpmMotor1 = rpmcount / 1.79
        rpmMotor2 = rpmcount2 / 1.65
        #print("rpm1: ",rpmMotor1,"rpm2: ",rpmMotor2)
        motor1_rpm_change = rpmMotor1 - rpmMotor1_initial
        motor2_rpm_change = rpmMotor2 - rpmMotor2_initial
        middlePoint = (motor1_rpm_change + motor2_rpm_change) / 2
        if((motor1_rpm_change >= 0) | (motor2_rpm_change >= 0)):
            angle = (anglesum + (motor1_rpm_change - motor2_rpm_change) / 2.53)%360
        else:
            angle = (anglesum - (motor1_rpm_change - motor2_rpm_change) / 2.53)%360
        
        x_position = middlePoint * math.cos(anglesum * math.pi /180) + x_pos_initial
        y_position = middlePoint * math.sin(anglesum * math.pi /180) + y_pos_initial
        if(angle>240):
            angle -= 360
#        if(counter1 == 0):
        desired_angle = (math.atan2((desired_y_position - y_position) , (desired_x_position - x_position))) * 180 / math.pi            
        PI_controller(desired_angle, angle)
#        else:
#            desired_distance = math.sqrt(math.pow((desired_y_position - encoder_y_position), 2) + math.pow((desired_x_position - encoder_x_position), 2))
            #PD_DistanceController(desired_distance)
#        headingArray.append(angle)
#        x_pos_array.append(x_position)
#        y_pos_array.append(y_position)
        if((angle_error > -1) & (angle_error < 1)):
            counter += 1
#            
#        if(counter >= 1000):
##        if(y_position >= 30):
#            desired_angle = 90
#            last_angle_error = 0
#            baseSpeed = 0
#            maxMotorSpeed = 8
#            minMotorSpeed = -8
#            motor1.brake() #Short brake
#            motor2.brake()
#            time.sleep(1)
#            counter = 0
#            counter1 += 1
#        if(counter1 == 2):
#            motor1.brake() #Short brake
#            motor2.brake()
##            np.asarray(headingArray)
##            np.asarray(x_pos_array)
##            np.asarray(y_pos_array)
##            np.savetxt("headingAngle.csv", headingArray, delimiter = ",")
##            np.savetxt("x_position.csv", x_pos_array, delimiter = ",")
##            np.savetxt("y_position.csv", y_pos_array, delimiter = ",")
#            print("int1: ",interCounter,"int2: ",interCounter2,"loop: ",loopcounter)
#            GPIO.cleanup()
#            break
        anglesum = angle
        x_pos_initial = x_position
        y_pos_initial = y_position
        rpmMotor1_initial = rpmMotor1
        rpmMotor2_initial = rpmMotor2
        loopcounter += 1
        print("x pos:", x_position, "y pos: ", y_position, "heading: ", angle, "counter: ", counter)
#        print("rpm1: ", rpmMotor1, "rpm2: ", rpmMotor2, "heading: ", angle, "counter: ", counter)
except KeyboardInterrupt:
    GPIO.cleanup()

            




