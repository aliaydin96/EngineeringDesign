import RPi.GPIO as GPIO
import time
import numpy as np
from motor import *
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#variable definition
rpmcount = 0
rpmcount2 = 0
rpmMotor1 = 0
rpmMotor2 = 0
counter = 0
counter2 = 0
#input definition
GPIO.setup(16, GPIO.IN)  
GPIO.setup(18, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(24, GPIO.IN)
test = Motor(40,36,32,38,False)
test2 = Motor(35,37,33,38,False)
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
GPIO.add_event_detect(16, GPIO.RISING, callback = encoderDataMotor_1)
GPIO.add_event_detect(22, GPIO.RISING, callback = encoderDataMotor_2)
#GPIO.add_event_detect(18, GPIO.BOTH, callback = rpmmotor)
try:
    while True:
        rpmMotor1 = np.divide(rpmcount, 18.0)
        print("rpm1:",rpmMotor1)
        rpmMotor2 = np.divide(rpmcount2, 18.0)
        print("rpm2:",rpmMotor2)
        
        test.drive(-counter) #Backwards 100% dutycycle
        test2.drive(-counter)
        
        if(counter == 7):
            counter = 7
        else:
            counter = counter + 1
            counter2 += 1
        if((rpmMotor1 >= 10) | (rpmMotor2 >= 10)):
            test.brake() #Short brake
            test2.brake()
            test.standby(True) #Enable standby
            test.standby(False) #Disable standby

        

except KeyboardInterrupt:
    GPIO.cleanup()
#    rpmcount = 0
            



