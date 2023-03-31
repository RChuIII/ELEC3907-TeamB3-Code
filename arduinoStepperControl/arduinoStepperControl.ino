#include <Stepper.h>

const int numSteps = 200; // # of stepper motor steps (Nema17 = 200)
Stepper baseStepper(numSteps, 22, 23, 24, 25); // Stepper, controls pins 1-4
byte rx_byte = 0;        // stores received byte

void setup() {
  // put your setup code here, to run once:
  baseStepper.setSpeed(60); // Spepd of motor in RPM
  Serial.begin(9600); // Serial Baud rate
}

void loop() {
  baseStepper.step(100);
  delay(500);
  baseStepper.step(100);
  delay(500);
}
/*
  -> Write calibration code for accelerometer
  -> Integrate accelerometer and bluetooth moduels
  -> Read Accelerometer data from bluetooth device
  -> Accelerometer to maths
  -> Clean up the maths code
  -> write a better python main program.


*/