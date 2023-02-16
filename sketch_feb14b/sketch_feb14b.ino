#include <Stepper.h>

const int NUM_STEPS = 200;
int old = 0;
Stepper baseStepper(NUM_STEPS, 8,9,10,11);

void setup() {
  Serial.begin(9600); 
  baseStepper.setSpeed(60);
}

void loop() {
  int y1 = analogRead(A0);
  int y2 = analogRead(A1);
  int y3 = analogRead(A2);
  int y4 = analogRead(A3);

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
  int a = (round(float(y2)*5.0/1024.0 * 10)-18) * 3;
  Serial.println(a - old);
  old = a;
  digitalWrite(8,LOW);
  digitalWrite(9,LOW);
  digitalWrite(10,LOW);
  digitalWrite(11,LOW);
  delay(1000);
}