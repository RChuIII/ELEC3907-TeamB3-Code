#include <SoftwareSerial.h>
#include <Stepper.h>

Stepper arm_base_stepper(NUM_STEPS, 8,9,10,11);
SoftwareSerial bt_module_glove(10,11);

const int NUM_STEPS = 200;

void setup() {
  serial.begin(9600);
  bt_module_glove.begin(9600);
  arm_base_stepper.setSSpeed(60);

  bt_module_glove.print("AT+BAUD4");
  Serial.println("Enter Command: ");

  
}

void loop() {
  int accel_x_axis = analogRead();
}


/*


  int xpos = -(round(float(x1) * 5.0 / 1024.0 * 10) - 17);
  int ypos = (round(float(y1) * 5.0 / 1024.0 * 10) - 18);
  float zpos = ((float(x2) * 5.0 / 1024.0) - 0.9) * 6.25;
  if (zpos <= 0){ zpos = 0; }
  if (zpos >= 10){ zpos = 10; }
  Serial.print(xpos);


*/

/*
  Serial.print(float(x1)*5.0/1024.0);
  Serial.print(" : ");
  Serial.print(float(y1)*5.0/1024.0);
  Serial.println();
  Serial.print(float(x2)*5.0/1024.0);
  Serial.print(" : ");
  Serial.print(float(y2)*5.0/1024.0);
  Serial.println();
  Serial.println();
*/


  //Serial.print(float(y1)*5.0/1024.0);
  //Serial.print(" "); // a space ' ' or  tab '\t' character is printed between the two values.
  //Serial.print(float(y2)*5.0/1024.0);
  //Serial.print(" "); // a space ' ' or  tab '\t' character is printed between the two values.
  //Serial.print(float(y3)*5.0/1024.0);
  //Serial.print(" "); // a space ' ' or  tab '\t' character is printed between the two values.
  //Serial.println(y4); // the last value is followed by a carriage return and a newline characters.

  //baseStepper.step(((float(y2)*5.0/1024.0) - 1.9) * 30);
  //Serial.println(((float(y2)*5.0/1024.0) - 1.8) * 30);
  //Serial.println();
  
  /*
  
  int xpos = -(round(float(x1) * 5.0 / 1024.0 * 10) - 17);
  int ypos = (round(float(y1) * 5.0 / 1024.0 * 10) - 18);
  float zpos = ((float(x2) * 5.0 / 1024.0) - 0.9) * 6.25;
  if (zpos <= 0){ zpos = 0; }
  if (zpos >= 10){ zpos = 10; }
  Serial.print(xpos);


  Serial.println(a3);
  Serial.println(x2);
  Serial.println(y2);
  
  
  */

  //Serial.println(a - old);
  //old = a;
  //digitalWrite(8,LOW);
  //digitalWrite(9,LOW);
  //digitalWrite(10,LOW);
  //digitalWrite(11,LOW);