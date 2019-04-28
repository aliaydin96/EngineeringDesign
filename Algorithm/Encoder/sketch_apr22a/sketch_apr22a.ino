byte encoderA1 = 2;
byte encoderB1 = 4;
byte encoderA2 = 3;
byte encoderB2 = 5;
byte encoderA1_result = 0;
byte encoderB1_result = 0;
byte encoderA2_result = 0;
byte encoderB2_result = 0;
int rpmcount = 0;
int rpmcount2 = 0;
int i =0;
int mode =0;
void setup() {
  Serial.begin(9600);
  pinMode(encoderA1,INPUT);
  pinMode(encoderB1,INPUT);
  pinMode(encoderA2,INPUT);
  pinMode(encoderB2,INPUT);
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);
  digitalWrite(10,LOW);
  digitalWrite(11,LOW);
  attachInterrupt(digitalPinToInterrupt(encoderA1), encoderInterrupt_1, FALLING);
  attachInterrupt(digitalPinToInterrupt(encoderA2), encoderInterrupt_2, RISING);
  
  delay(1000);
}

void loop() {
 if(Serial.available()>0){
  mode = Serial.read()-'0';
 }
 if(mode == 1){
  Serial.println(rpmcount);  
  mode = 0;
 }
 if(mode == 2){
  Serial.println(rpmcount2);
  mode = 0;
 }
 if(mode ==3){
  rpmcount = 0;
  rpmcount2 = 0;
  mode = 0;
 }
}
void encoderInterrupt_1(void){
    encoderA1_result = digitalRead(encoderA1);
    encoderB1_result = digitalRead(encoderB1);
    if(encoderA1_result == HIGH){
        if(encoderB1_result == HIGH) rpmcount = rpmcount + 1;
        else                         rpmcount = rpmcount - 1;
    }
    else{
        if(encoderB1_result == LOW)  rpmcount = rpmcount - 1;
        else                         rpmcount = rpmcount + 1;
    }
//    Serial.print("1: ");
//    Serial.println(rpmcount); 
}
void encoderInterrupt_2(void){
    encoderA2_result = digitalRead(encoderA2);
    encoderB2_result = digitalRead(encoderB2);
    if(encoderA2_result == HIGH){
        if(encoderB2_result == HIGH) rpmcount2 = rpmcount2 + 1;
        else                         rpmcount2 = rpmcount2 - 1;
    }
    else{
        if(encoderB2_result == LOW)  rpmcount2 = rpmcount2 - 1;
        else                         rpmcount2 = rpmcount2 + 1;
    }
//    Serial.print("2: ");
//    Serial.println(rpmcount2);
}

