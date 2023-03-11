/*
  ELEC 3907 - Team B3 : Robotic Arm Project
  Glove Code
*/

// Libraries
#include <Arduino.h>
#include <ezButton.h> // Simple button usage
#include <AceSorting.h>

// Variables
int isCalibrated = 0;  // Used for auto calibration code
double normX = 0;    // Normalized X value
double normY = 0;    // Normalized Y value
int isRotated = 0;
int current_mode = 0;

// Pin definitions
int calibration_LED_pin = 13;
int calibration_button_pin = 7;
int claw_rotation_btn_pin = 8;
int mode_select_pin = 9;
int claw_actuation_pin = A0;
int accel_X_pin = A5;
int accel_Y_pin = A4;

// Buttons
ezButton calibration_button(calibration_button_pin);
ezButton claw_rotation_button(claw_rotation_btn_pin);
ezButton mode_select(mode_select_pin);

// Structures
struct coordinates {
  double x_coord;
  double y_coord;
};


void setup() {
  Serial.begin(9600); 
  Serial.println("Executed - Setup");
  digitalWrite(calibration_LED_pin, LOW);
}

void loop() {
  calibration_button.loop();
  if (isCalibrated == 1) {
    double accel_X = analogRead(accel_X_pin) * 5.0 / 1024 * 10;
    double accel_Y = analogRead(accel_Y_pin) * 5.0 / 1024 * 10;
    double claw_act = analogRead(claw_actuation_pin);
    Serial.print(accel_X - normX);
    Serial.print("  :  ");
    Serial.println(accel_Y - normY);
    // bluetooth.write([curX, curY, current_mode, claw_act, isRotated]);
    delay(100);
  }
  
  if (calibration_button.isPressed()) { 
    coordinates cords = auto_calibration(); 
    normX = cords.x_coord;
    normY = cords.y_coord;
  }

  if (mode_select.isPressed()) {
    if (current_mode == 0){ current_mode = 1; }
    else { current_mode = 0; }
  }

  if (claw_rotation_button.isPressed()) {
    if (isRotated == 0){ isRotated = 1; }
    else { isRotated = 0; }
  }
  
  
}


coordinates auto_calibration(){
  Serial.println("Executed");
  double numSamples = 100.0;
  double sumX, sumY;
  double arrX[100];
  double arrY[100];
  double nrmX = 0;
  double nrmY = 0;
  
  for (int i = 0; i < numSamples; i++) {
    delay(50);
    digitalWrite(calibration_LED_pin, LOW);
    arrX[i] = analogRead(accel_X_pin);
    arrY[i] = analogRead(accel_Y_pin);
    delay(50);
    digitalWrite(calibration_LED_pin, HIGH);
  }
  
  ace_sorting::quickSortMiddle(arrX, 100);
  ace_sorting::quickSortMiddle(arrY, 100);

  for (int n = numSamples/8; n < (numSamples - numSamples/8) - 1; n++) {
    sumX += arrX[n] / 1024.0;
  }
  
  for (int n = numSamples/8; n < (numSamples - numSamples/8) - 1; n++) {
    sumY += arrY[n] / 1024.0;
  }

  double rec_samples = numSamples - 2.0 * (numSamples / 8);
  isCalibrated = 1;
  return { (sumX/rec_samples) * 50 , (sumY/rec_samples) * 50 };
}