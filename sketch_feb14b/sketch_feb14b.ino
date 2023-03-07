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

  Serial.print(a0);
  Serial.print(" ");
  Serial.print(x1);
  Serial.print(" ");
  Serial.print(y1);
  Serial.print(" ");
  Serial.print(a3);
  Serial.print(" ");
  Serial.print(x2);
  Serial.print(" ");
  Serial.println(y2);
  delay(100);
}