#include <Wire.h>
#include <VL53L0X.h>

#define XSHUT_pin1 2
#define XSHUT_pin2 3
#define XSHUT_pin3 4
#define XSHUT_pin4 5
#define Sensor1_newAddress 41
#define Sensor2_newAddress 42
#define Sensor3_newAddress 43
#define Sensor4_newAddress 44
VL53L0X Sensor1;
VL53L0X Sensor2;
VL53L0X Sensor3;
VL53L0X Sensor4;
void setup()
{ 
  Serial.begin(9600); 
  Wire.begin();  
  pinMode(XSHUT_pin1, OUTPUT);
  pinMode(XSHUT_pin2, OUTPUT);
  pinMode(XSHUT_pin3, OUTPUT); 
  pinMode(XSHUT_pin4, OUTPUT); 
  Sensor1.setAddress(Sensor1_newAddress);
  pinMode(XSHUT_pin1, INPUT);
  delay(10);
  Sensor2.setAddress(Sensor2_newAddress);
  pinMode(XSHUT_pin2, INPUT);
  delay(10);
  Sensor3.setAddress(Sensor3_newAddress);
  pinMode(XSHUT_pin3, INPUT);
  delay(10);
  Sensor4.setAddress(Sensor4_newAddress);
  pinMode(XSHUT_pin4, INPUT);
  delay(10);
  Sensor1.setSensor();
  Sensor2.setSensor();
  Sensor3.setSensor();
  Sensor4.setSensor();
}

void loop()
{
  Serial.print(Sensor1.readRangeContinuousMillimeters());
  Serial.print(',');
  Serial.print(Sensor2.readRangeContinuousMillimeters());
  Serial.print(',');
  Serial.print(Sensor3.readRangeContinuousMillimeters());
  Serial.print(',');
  Serial.println(Sensor4.readRangeContinuousMillimeters());
}
