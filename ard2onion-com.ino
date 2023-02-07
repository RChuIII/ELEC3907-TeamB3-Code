#include <SoftwareSerial.h>

SoftwareSerial gtSerial(8, 7); // Arduino RX, Arduino TX

void setup() {
  Serial.begin(9600);    // serial / USB port
  gtSerial.begin(9600);  // software serial port
}

byte rx_byte = 0;        // stores received byte

void loop() {
  // check if byte available from USB port
  if (Serial.available()) {
    rx_byte = Serial.read();
    
  }
