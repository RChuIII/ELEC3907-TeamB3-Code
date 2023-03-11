#include <SoftwareSerial.h>
#include <ezButton.h>

SoftwareSerial bt_module_glove(10,11);
ezButton calibration_button(7);
ezButton switch_mode(8);



void setup() {
  serial.begin(9600);
  bt_module_glove.begin(9600);
  switch_mode.setDebounceTime(50);

  bt_module_glove.print("AT+BAUD4");
  Serial.println("Enter Command: ");

  
}

void loop() {
  switch_mode.loop();

  int accel_x_axis = analogRead();
  int accel_y_axis = analogRead();

  Serial.write(accel_x_axis + " " + accel_y_axis + " " + switch_mode.isPressed())
  if (Serial.available()){
    hc06.write(Serial.read());
  }

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