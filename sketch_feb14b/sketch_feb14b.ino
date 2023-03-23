/*
  ELEC 3907 - Team B3 : Robotic Arm Project
  Glove Code
*/

// Libraries
#include <Arduino.h>
#include <ezButton.h>         // Simple button usage
#include <AceSorting.h>       // Sorting Algorithm
#include <SoftwareSerial.h>   // Serial communication

// Variables
int isCalibrated = 0;   // Used for auto calibration code
double normX = 0;       // Normalized X value
double normY = 0;       // Normalized Y value
int isRotated = 0;      // False/True claw is rotated 90 degrees
int current_mode = 0;   // Mode 0/1 toggle
int claw_act = 0;       // False/True claw is actuated

// LEDs pins
int calibrating_LED_pin = 2;            // LED for calibration in progress
int calibration_complete_LED_pin = 3;   // LED for calibration completed


// Button pins
int calibration_button_pin = 7; // Button for calibration
int claw_rotation_btn_pin = 8;  // Button to toggle claw rotation
int mode_select_pin = 9;        // Button to toggle accelerometer mode

// Analog pins
int accel_X_pin = A5;           // Accelerometer X input
int accel_Y_pin = A4;           // Accelerometer Y input
int claw_actuation_pin = A0;    // Flex/Pressure sensor input

// Bluetooth
int bt_TX = 11;                         // Software serial TX (connect to bt RX)
int bt_RX = 10;                         // Software serial RX (connect to bt TX)
SoftwareSerial bt_module(bt_RX,bt_TX);  // Setup software serial with the bluetooth pins

// Button Setups
ezButton calibration_button(calibration_button_pin);
ezButton claw_rotation_button(claw_rotation_btn_pin);
ezButton mode_select_button(mode_select_pin);

// Structures
struct coordinates {
  double x_coord;
  double y_coord;
};

// CONSTS
double FLEX_SENSOR_THRESHOLD_VOLTAGE = 950.0;


void setup() {
  // Setup input pins
  pinMode(bt_RX,INPUT);
  pinMode(accel_X_pin,INPUT);
  pinMode(accel_Y_pin,INPUT);
  pinMode(claw_rotation_btn_pin,INPUT);
  pinMode(mode_select_pin,INPUT);
  pinMode(claw_actuation_pin, INPUT);

  // Setup output pins
  pinMode(bt_TX,OUTPUT);
  pinMode(calibrating_LED_pin,OUTPUT);
  pinMode(calibration_complete_LED_pin,OUTPUT);

  // Setup serial and software serial (bt module)
  Serial.begin(9600); 
  bt_module.begin(9600);
  bt_module.print("AT+BAUD4");

  // Drop the LEDs to low
  digitalWrite(calibrating_LED_pin, LOW);
  digitalWrite(calibration_complete_LED_pin, LOW);
}

void loop() {
  // Start the buttons
  calibration_button.loop();
  claw_rotation_button.loop();
  mode_select_button.loop();

  // Run this code only if the calibration has been done.
  if (isCalibrated == 1) {
    double flex_read = analogRead(claw_actuation_pin);
    double x_sums = 0;
    double y_sums = 0;
    double x_avg, y_avg;

    for (int i = 0; i < 10; i++) {
      x_sums += analogRead(accel_X_pin) * 5.0 / 1024 * 10;
      y_sums += analogRead(accel_Y_pin) * 5.0 / 1024 * 10;
      delay(10);
    }
    x_avg = round(x_sums / 10);
    y_avg = round(y_sums / 10);

    double avg_X = round((x_avg - normX) * 10) / 10;
    double avg_Y = round((y_avg - normY) * 10) / 10;


    check_inputs(mode_select_button.isPressed(), claw_rotation_button.isPressed(), flex_read);
    String output = String(avg_X,2)
                   + " " + String(avg_Y,2)
                   + " " + String(current_mode)
                   + " " + String(claw_act)
                   + " " + String(isRotated)
                   + "\n\r";

    bt_module.print(output);
    Serial.print(output);
    //delay(10);
  }
  
  // Run the calibration if button is pressed
  if (calibration_button.isPressed()) { 
    digitalWrite(calibrating_LED_pin, HIGH);
    digitalWrite(calibration_complete_LED_pin, LOW);
    coordinates cords = auto_calibration(); 
    normX = cords.x_coord;
    normY = cords.y_coord;
    digitalWrite(calibrating_LED_pin, LOW);
    digitalWrite(calibration_complete_LED_pin, HIGH);
  }
}

void check_inputs(bool mode_btn, bool clrt_btn, double flx_rx){
  // Toggle mode select button
  if (mode_btn) {
    if (current_mode == 0){ current_mode = 1; }
    else { current_mode = 0; }
  }

  // Toggle claw rotation
  if (clrt_btn) {
    if (isRotated == 0){ isRotated = 1; }
    else { isRotated = 0; }
  }
  if (flx_rx != NULL) {
    if (flx_rx < FLEX_SENSOR_THRESHOLD_VOLTAGE) { claw_act = 1; } 
    else { claw_act = 0; }
    
  }
  
}

coordinates auto_calibration(){
  double numSamples = 100.0;
  int num_limit = 10;
  double sumX, sumY;
  double arrX[100];
  double arrY[100];
  double nrmX = 0;
  double nrmY = 0;
  
  for (int i = 0; i < numSamples; i++) {
    arrX[i] = analogRead(accel_X_pin);
    arrY[i] = analogRead(accel_Y_pin);
    delay(100);
  }
  
  ace_sorting::quickSortMiddle(arrX, 100);
  ace_sorting::quickSortMiddle(arrY, 100);

  for (int n = numSamples/num_limit; n < (numSamples - numSamples/num_limit) - 1; n++) {
    sumX += arrX[n] / 1024.0;
  }
  
  for (int n = numSamples/num_limit; n < (numSamples - numSamples/num_limit) - 1; n++) {
    sumY += arrY[n] / 1024.0;
  }

  double rec_samples = numSamples - 2.0 * (numSamples / num_limit);
  isCalibrated = 1;
  return { (sumX/rec_samples) * 50 , (sumY/rec_samples) * 50 };
}