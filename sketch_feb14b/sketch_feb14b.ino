#include <Stepper.h>

const int NUM_STEPS = 200;
int old = 0;
Stepper baseStepper(NUM_STEPS, 8,9,10,11);

void setup() {
  Serial.begin(9600); 
  baseStepper.setSpeed(60);
}

void loop() {
  int a0 = analogRead(A0);
  int x1 = analogRead(A1);
  int y1 = analogRead(A2);
  int a3 = analogRead(A3);
  int x2 = analogRead(A4);
  int y2 = analogRead(A5);
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
  int xpos = -(round(float(x1) * 5.0 / 1024.0 * 10) - 17);
  int ypos = (round(float(y1) * 5.0 / 1024.0 * 10) - 18);
  float zpos = ((float(x2) * 5.0 / 1024.0) - 0.9) * 6.25;
  if (zpos <= 0){ zpos = 0; }
  if (zpos >= 10){ zpos = 10; }
  Serial.print(xpos);
  Serial.print(" : ");
  Serial.print(ypos);
  Serial.print(" : ");
  Serial.print(zpos);
  Serial.println();
  Serial.println();
  //Serial.println(a - old);
  //old = a;
  //digitalWrite(8,LOW);
  //digitalWrite(9,LOW);
  //digitalWrite(10,LOW);
  //digitalWrite(11,LOW);
  delay(100);
}