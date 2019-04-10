import RPi.GPIO as GPIO
import time
import numpy as np
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#variable definition
rpmcount = 0
rpmcount2 = 0
rpmMotor1 = 0
rpmMotor2 = 0
#input definition
GPIO.setup(24, GPIO.IN)  
GPIO.setup(26, GPIO.IN)
GPIO.setup(29, GPIO.IN)
GPIO.setup(31, GPIO.IN)

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
GPIO.add_event_detect(26, GPIO.RISING, callback = encoderDataMotor_1)
GPIO.add_event_detect(29, GPIO.RISING, callback = encoderDataMotor_2)
#GPIO.add_event_detect(18, GPIO.BOTH, callback = rpmmotor)
try:
    while True:
        rpmMotor1 = rpmcount / 17.9
        rpmMotor2 = rpmcount2 / 16.5
        print("rpm1:",rpmMotor1,"rpm2:",rpmMotor2)

except KeyboardInterrupt:
    GPIO.cleanup()
#    rpmcount = 0
            


