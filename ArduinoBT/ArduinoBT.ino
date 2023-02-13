#include <SoftwareSerial.h>

SoftwareSerial hc06(10,11);

void setup() {
  pinMode(10,INPUT);
  pinMode(11,OUTPUT);

  Serial.begin(9600);

  hc06.begin(9600);
  hc06.print("AT+BAUD4");
  Serial.println("ENTER AT Commands:");
}

void loop() {
  // put your main code here, to run repeatedly:
  if (hc06.available()){
    Serial.write(hc06.read());
  }
  if (Serial.available()){
    hc06.write(Serial.read());
  }

}
