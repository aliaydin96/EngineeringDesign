from motor import *
from time import sleep #Only used for example

#Motor(IN1,IN2,PWM,STANDBY,(Reverse polarity?))
test = Motor(40,36,32,38,False)
test2 = Motor(35,37,33,38,False)

test.drive(10) #Forward 100% dutycycle
test2.drive(10)
sleep(1)
test.drive(-10) #Backwards 100% dutycycle
test2.drive(-10)
sleep(1)
test.brake() #Short brake
test2.brake()
sleep(0.1)

test.standby(True) #Enable standby
test.standby(False) #Disable standby

GPIO.cleanup()