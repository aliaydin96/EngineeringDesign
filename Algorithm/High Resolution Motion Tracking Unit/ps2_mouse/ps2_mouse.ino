#include <ps2.h>
//PS2 :: mouse (data_pin, clock_pin)

PS2 mouse(5, 6);
void setup()
{
  Serial.begin(9600);
  mouse.write(0xff);  // reset
  mouse.read();  // ack byte
  mouse.read();  // blank */
  mouse.read();  // blank */
  mouse.write(0xf0);  // remote mode
  mouse.read();  // ack
  delayMicroseconds(100);
}

void loop()
{
  char mstat;
  char mx;
  char my;

  mouse.write(0xeb); //Register Activation
  mouse.read();  
  mstat = mouse.read();
  mx = mouse.read();
  my = mouse.read();

  Serial.print(mstat, BIN);
  Serial.print("\tX=");
  Serial.print(mx, DEC);
  Serial.print("\tY=");
  Serial.print(my, DEC);
  Serial.println();
}
