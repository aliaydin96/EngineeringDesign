import serial
import csv
import numpy as np
import time
def ESU(ESU_counter):
    Environment_Sensing_Unit = serial.Serial("/dev/ttyUSB1", 9600)
    Environment_Sensing_Unit_Measurement = np.zeros([1, 400])
    time.sleep(3) 
    Environment_Sensing_Unit.write(b'3')
    for i in range(400):
        Environment_Sensing_Unit_Measurement[0][i] = Environment_Sensing_Unit.readline()
    np.savetxt('data'+str(ESU_counter)+'.csv', Environment_Sensing_Unit_Measurement, delimiter=',')

