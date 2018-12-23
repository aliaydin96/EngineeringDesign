//PS2 :: mouse (data_pin, clock_pin)
#include <ps2.h>
char mstat;
int mx_1;
int my_1;
int mx_2;
int my_2;
int i=0;
PS2 mouse_1(5, 6);
PS2 mouse_2(7, 8);
void setup()
{
  Serial.begin(115200);
  mouse_1.write(0xff);  // reset
  mouse_1.read();  // ack byte
  mouse_1.read();  // blank */
  mouse_1.read();  // blank */
  mouse_1.write(0xf0);  // remote mode
  mouse_1.read();  // ack
  delayMicroseconds(100);
  
  mouse_2.write(0xff);  // reset
  mouse_2.read();  // ack byte
  mouse_2.read();  // blank */
  mouse_2.read();  // blank */
  mouse_2.write(0xf0);  // remote mode
  mouse_2.read();  // ack
  delayMicroseconds(100);
}

void loop()
{ mouse_1.write(0xeb);
  mouse_2.write(0xeb);
  mouse_1.read();  
  mouse_2.read(); 
  mstat = mouse_1.read();
  mstat = mouse_2.read();
  mx_1 = mx_1 + (char) mouse_1.read();
  my_1 = my_1 + (char) mouse_1.read();
  mx_2 = mx_2 + (char) mouse_2.read();
  my_2 = my_2 + (char) mouse_2.read();
  if(i++ >= 100){

    //Writing data to serial port
    
  
    Serial.println(mx_1);
    //delay(250);
    Serial.println(my_1);
    //delay(250);
    Serial.println(mx_2);
    //delay(250);
    Serial.println(my_2);
    //delay(250);
    i=0;
    }
}