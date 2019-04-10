import serial
import RPi.GPIO as GPIO
import time
import math 
from motor import *
GPIO.setwarnings(False)

Kp = 0.7
Kd = 0.2
desired_angle = 30
desired_x_position = 500
desired_y_position = 100
baseSpeed = 4
maxMotorSpeed = 8
minMotorSpeed = 0
constant_divider_forMouse = 34.0
ser = serial.Serial("/dev/ttyUSB0", 115200)
headingArray = []
x_pos_array = []
y_pos_array = []
dx1 = 0
dy1 = 0
dx2 = 0
dy2 = 0
mx1 = 0
my1 = 0
mx2 = 0
my2 = 0
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
angle = 0
anglesum = 90
x_position = 0
y_position = 0
middlePoint = 0
x_position_initial = 0
y_position_initial = 0
counter = 0
counter1 = 0
angle_error = 0
last_angle_error = 0
dutycycle_1_initial = 0
dutycycle_2_initial = 0
coordinate_angle = 0
GPIO.setup(18, GPIO.IN)
#in1, in2, PWM, Stanby, (polarity of motors)
motor1 = Motor(40,36,32,38,True)
motor2 = Motor(35,37,33,38,False)
def PD_controller(desired_angle, angle):
    global counter
    global last_angle_error, angle_error
    global dutycycle_1_initial, dutycycle_2_initial
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
    

def mouseInterrupt(A):
    global mx1,mx2,my1,my2
    dx1 = int(ser.readline())
    dy1 = -int(ser.readline())
    dx2 = int(ser.readline())
    dy2 = -int(ser.readline())
    dx1 = dx1 * constant_divider_forMouse / 255 
    dy1 = dy1 * constant_divider_forMouse / 255 
    dx2 = dx2 * constant_divider_forMouse / 255 
    dy2 = dy2 * constant_divider_forMouse / 255
    dangle1 = 0.05
    dangle2 = 0.05
    dx1 = dx1 * math.cos(dangle1) - dy1 * math.sin(dangle1)
    dy1 = dx1 * math.sin(dangle1) + dy1 * math.cos(dangle1)
    dx2 = dx2 * math.cos(dangle2) + dy2 * math.sin(dangle2)
    dy2 = dx2 * math.sin(dangle2) + dy2 * math.cos(dangle2)
    mx1 += dx1
    my1 += dy1
    mx2 += dx2
    my2 += dy2
    return

GPIO.add_event_detect(18, GPIO.RISING, callback = mouseInterrupt)
time.sleep(5)
try:        
    while True:
    #    time_begin = time.time()
        
        length1 = math.sqrt(math.pow(mx1,2) + math.pow(my1,2))
        length2 = math.sqrt(math.pow(mx2,2) + math.pow(my2,2))
        x_avg = (mx1 + mx2) / 2
        y_avg = (my1 + my2) / 2
        length1_change = length1 - length1_initial   
        length2_change = length2 - length2_initial
        x_avg_change = x_avg - x_avg_initial
        y_avg_change = y_avg - y_avg_initial
       
        if((x_avg >= 0)):
            angle = (anglesum - (length1_change - length2_change) / 1.1) % 360
        else:
            angle = (anglesum + (length1_change - length2_change) / 1.1) % 360

        x_position = x_avg_change * math.cos(anglesum * math.pi / 180) - y_avg_change * math.sin(anglesum * math.pi / 180) + x_position_initial
        y_position = x_avg_change * math.sin(anglesum * math.pi / 180) + y_avg_change * math.cos(anglesum * math.pi / 180) + y_position_initial
#        print("dx1: ", dx1, "dy1: ", dy1, "dx2: ", dx2, "dy2: ",dy2)

#        desired_angle = (math.atan2((desired_y_position - y_position) , (desired_x_position - x_position))) * 180 / math.pi
        if(angle > 240):
            angle = angle - 360
#        if(desired_angle > 180):
#            desired_angle -= 360
        PD_controller(desired_angle, angle)
        print("angle ", angle, "x position ", x_position,"y position ", y_position)

    #    motor1.drive(counter) #Backwards 100% dutycycle
    #    motor2.drive(counter)
    #        
    #    if(counter == 7):
    #        counter = 7
    #    else:
    #        counter = counter + 1   
 #       if((x_position >= 100) | (y_position >= 100)):
    #        motor1.brake() #Short brake
    #        motor2.brake()
    #        motor1.standby(True) #Enable standby
    #        motor1.standby(False) #Disable standby
#        headingArray.append(angle)
#        x_pos_array.append(x_position)
#        y_pos_array.append(y_position)
        if((angle_error > -1) & (angle_error < 1)):
            counter += 1
        if(counter == 1000):    
#        if((abs(x_position) >= abs(desired_x_position)) & (abs(y_position) >= abs(desired_y_position))):
#        if(y_position >= 100):
            desired_angle = 90
            counter = 0
            baseSpeed = -4
            maxMotorSpeed = 0
            minMotorSpeed = -8
            counter1 += 1
        if(counter1 == 2): 
 #       if((x_position >= 100) | (y_position >= 100)):
            motor1.brake() #Short brake
            motor2.brake()
#            np.asarray(headingArray)
#            np.asarray(x_pos_array)
#            np.asarray(y_pos_array)
#            np.savetxt("headingAngle.csv", headingArray, delimiter = ",")
#            np.savetxt("x_position.csv", x_pos_array, delimiter = ",")
#            np.savetxt("y_position.csv", y_pos_array, delimiter = ",")
            GPIO.cleanup()
            break
        anglesum = angle
        x_position_initial = x_position
        y_position_initial = y_position
        length1_initial = length1
        length2_initial = length2
        x_avg_initial = x_avg
        y_avg_initial = y_avg
    #    time_end = time.time()
    #    duration = time_end - time_begin
    #    print(duration)
    #    print("===========")
except KeyboardInterrupt:
    GPIO.cleanup()
