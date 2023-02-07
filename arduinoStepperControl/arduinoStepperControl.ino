#include <Stepper.h>

const int numSteps = 200; // # of stepper motor steps (Nema17 = 200)
Stepper baseStepper(numSteps, 8, 9, 10, 11); // Stepper, controls pins 1-4
byte rx_byte = 0;        // stores received byte

void setup() {
  // put your setup code here, to run once:
  baseStepper.setSpeed(60); // Spepd of motor in RPM
  Serial.begin(9600); // Serial Baud rate
}

void loop() {
 baseStepper.step(90);
}
