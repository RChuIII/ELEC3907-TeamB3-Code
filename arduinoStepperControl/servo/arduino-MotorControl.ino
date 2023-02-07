/*

*/

#include <Servo.h>
#include <Stepper.h>

Servo shoulderServo;
Servo elbowServo;
Servo wristServo
Servo clawServo; 
Stepper baseStepper(numSteps, 8, 9, 10, 11); // Stepper, controls pins 1-4


const int numSteps = 200; // # of stepper motor steps (Nema17 = 200)
byte rx_byte = 0;        // stores received byte
float posBase = 90;
float posShoulder = 90;
float posElbow = 90;
float posWrist = 90;
bool actClaw = false;

void setup() {
  baseStepper.setSpeed(60); // Set the speed of the servo motor in RPM

  shoulderServo.attach(7);  // Attach the shoulder servo control pin to pin 7
  elbowServo.attach(6);     // Attach the elbow servo control pin to pin 6
  wristServo.attach(5);     // Attach the wrist servo control pin to pin 5
  clawServo.attach(4);      // Attach the claw servo control pin to pin 4

  shoulderServo.write(posShoulder); // Move servo to the mid-point position
  elbowServo.write(posElbow);       // Move servo to the mid-point position
  wristServo.write(posWrist);       // Move servo to the mid-point position
  clawServo.write(0);               // Move servo calw to the open position
  Serial.begin(9600); // Serial communication Baud rate
}

void loop() {
  /*
  PSUDO Code
  serial.recieve([float base, float shoulder, float elbow, float wrist, bool claw])
  foreach Angle in recieve():
    angle2mmove = -(currentAngle - recieve[angle]);
  
  
  
  */
}