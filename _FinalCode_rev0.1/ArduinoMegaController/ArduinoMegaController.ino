#include <SoftwareSerial.h>

int pi_TX = 2;
int pi_RX = 3;

SoftwareSerial pi_comm(pi_RX, pi_TX);

float old_angles[5];
float cur_angles[5];

void setup() {
  Serial.begin(9600);
  pi_comm.begin(9600);
}

void loop() {
  //GetData();
  //smoothMovement();
  //old_angles = cur_angles;
  if (pi_comm.available()) {
    Serial.write( pi_comm.read() );
  }
  
  
}

//10, 11, 12, 13, 14

void GetData(){
  for (int i = 0; i < 5; i++) {
    cur_angles[i] = pi_comm.readStringUntil(' ').toFloat();
  }
}

void smoothMovement(){
  int shoulder_diff = abs(cur_angles[1] - old_angles[1]);
  if (shoulder_diff) {
    for ( {
      // INCREMENT THE ANGLE
    }
  }
  
}