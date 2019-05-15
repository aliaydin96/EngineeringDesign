import RPi.GPIO as GPIO
import time
import numpy as np
import csv
import serial
import math
import time

coun = 0

GPIO.setwarnings(False)
Environment_Sensing_Unit = serial.Serial("/dev/ttyUSB1", 9600)
measurement1 = np.zeros([1, 400])
time.sleep(4)
try:
    for index in range(75):
            time.sleep(1)
            Environment_Sensing_Unit.write(b'3')  
            for i in range(400):
                measurement1[0][i] = Environment_Sensing_Unit.readline()
            #    measurement1 = np.asarray(measurment1)
            #    measurement2 = np.asarray(measurment2)
            a = measurement1
            np.savetxt('data'+str(coun+1)+'.csv', a, delimiter=',')
            coun = coun + 1
            time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
