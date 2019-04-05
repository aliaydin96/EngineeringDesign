#include <Wire.h>
#include <VL53L0X.h>

//stepper employement
#define DIR 2
#define STP 3
#define SLP 4
#define RST 5
#define M2  6
#define M1  7
#define M0  8
#define EN  9

//sensor employement
#define XSHUT_pin1 10
#define XSHUT_pin2 11
#define XSHUT_pin3 12
#define XSHUT_pin4 13
#define Sensor1_newAddress 41
#define Sensor2_newAddress 42
#define Sensor3_newAddress 43
#define Sensor4_newAddress 44
VL53L0X Sensor1;
VL53L0X Sensor2;
VL53L0X Sensor3;
VL53L0X Sensor4;

int measurement[200];
int i = 0;
void setup()
{ 
  //enabling stepper
  pinMode(DIR,OUTPUT);
  pinMode(STP,OUTPUT);
  pinMode(SLP,OUTPUT);
  pinMode(RST,OUTPUT);
  pinMode(M2,OUTPUT);
  pinMode(M1,OUTPUT);
  pinMode(M0,OUTPUT);
  pinMode(EN,OUTPUT);
  digitalWrite(DIR, LOW);
  digitalWrite(STP, LOW);
  digitalWrite(SLP, HIGH);
  digitalWrite(RST, HIGH);
  digitalWrite(M2, LOW);
  digitalWrite(M1, LOW);
  digitalWrite(M0, LOW);
  digitalWrite(EN, LOW);
  
  //enabling sensors
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
  delay(1);
  if(Serial.read() == 'x'){
    
    digitalWrite(DIR, LOW);
    digitalWrite(STP, LOW);
    for(i = 50; i > 0; i--){
      delay(1);
      measurement[i] = Sensor2.readRangeContinuousMillimeters()+52; 
      measurement[i+50] = Sensor1.readRangeContinuousMillimeters()+44;
      measurement[i+100] = Sensor4.readRangeContinuousMillimeters()+52;
      measurement[i+150] = Sensor3.readRangeContinuousMillimeters()+38;
      digitalWrite(STP, LOW);
      digitalWrite(STP, HIGH);
    }
    for(i = 0; i < 200; i++){
      Serial.println(measurement[i]);
    }
    
    digitalWrite(DIR, HIGH);
    digitalWrite(STP, LOW);
    for(i = 0; i < 50; i++){
      delay(1);
      measurement[i] = Sensor2.readRangeContinuousMillimeters()+52; 
      measurement[i+50] = Sensor1.readRangeContinuousMillimeters()+44;
      measurement[i+100] = Sensor4.readRangeContinuousMillimeters()+52;
      measurement[i+150] = Sensor3.readRangeContinuousMillimeters()+38;
      digitalWrite(STP, LOW);
      digitalWrite(STP, HIGH);
    }
    for(i = 0; i < 200; i++){
      Serial.println(measurement[i]);
    }
  }
  
}
