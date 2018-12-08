/*The system uses polar coordiantes with a bias.
 *The bias is on the radial coordinate due to the geomety of the test setup.
 *The bias r0 is 15 mm.
 *The core sends the bias filtered data to the communication port when serial port is opened.
 *The measurement presicion is defined by the rho_sensor.
 *For any problem, please contact selman dinc 
 *SDA == A4
 *SCLK == A5
 *COM10
 */
#include "Adafruit_VL53L0X.h"
#include "Servo.h"
Servo rotational_actuator;

int precision = 1;
int lowlimit = 55;
int highlimit = 125;
int theta = lowlimit;
boolean servo_direction = true;
int bias = 15;

Adafruit_VL53L0X rho_sensor = Adafruit_VL53L0X();

void setup() {
  pinMode(9,OUTPUT);
  rotational_actuator.attach(9);
  rotational_actuator.write(theta);
  delay(100);
  Serial.begin(115200);
  while (! Serial) {
    delay(100);
  }  
  if (!rho_sensor.begin()) {
    while(true){
      digitalWrite(9, HIGH);
      delay(1000);
      digitalWrite(9, LOW);
      delay(1000);
    }
  }
}


void loop() {
 if (servo_direction == true){ theta = theta + precision; if(theta >= highlimit){servo_direction = false;}}
 else {theta = theta - precision; if(theta <= lowlimit){servo_direction = true;}}

  rotational_actuator.write(theta);
  delay(25);
  VL53L0X_RangingMeasurementData_t measure;
  rho_sensor.rangingTest(&measure, false);
  if (measure.RangeStatus != 4) { 
    int rho = measure.RangeMilliMeter + bias;
    Serial.println(rho);
    delay(25);
    Serial.println(theta);
  } else {
    Serial.println(0);
    delay(25);
    Serial.println(0);
  }
}
