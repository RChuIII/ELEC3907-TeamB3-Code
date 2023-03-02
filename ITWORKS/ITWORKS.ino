#include <SoftwareSerial.h>

int x;
int y;
int z;

//SoftwareSerial hc06(10,11);

void setup() {
  //pinMode(10,INPUT);
  //pinMode(11,OUTPUT);

  Serial.begin(9600);

  //hc06.begin(9600);
  //hc06.print("AT+BAUD4");
  //Serial.println("ENTER AT Commands:");
}

void loop() {
  // put your main code here, to run repeatedly:
  x = analogRead(A5); // read A5 input pin
  y = analogRead(A4); // read A4 input pin
  z = analogRead(A3); // read A3 input pin
  Serial.println(x);
  Serial.println(y);
  Serial.println(z);
  delay(500);
/*
  if (hc06.available()){ // Recieve
    Serial.write(hc06.read());
  }
  if (Serial.available()){ // Send
    //Serial.println();
    hc06.print("X = " + String(x) + ", Y = " + String(y) + ", Z = " + String(z));
  } */
}
