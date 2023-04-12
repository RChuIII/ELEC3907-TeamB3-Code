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

void smoothMovement(int motor_num, double new_angle, double old_angle){
  double angle_change = 0;
    for (angle_change = old_angle; i < new_angle; angle_change+=2.5) {
      srituhobby.setPWM(motor_num, 0, angle_change);

    }
    if (angle_change > new_angle) {
      srituhobby.setPWM(motor_num, 0, new_angle);
    }
    
}






void loop() {
  delay(4000);
  int CCW = SHOULDERservoMAX;
  for (int CW = SHOULDERservoMIN; CW <= SHOULDERservoMAX; CW++) {
    CCW = CCW - 1;
    srituhobby.setPWM(0, 0, CW-0);
    srituhobby.setPWM(1, 0, CCW);
    delay(5);
  }

  delay(2000);
  for (int ELBOWrot = ELBOWservoMAX; ELBOWrot >= ELBOWservoMIN; ELBOWrot--) {
    srituhobby.setPWM(2, 0, ELBOWrot);
    delay(5);
  }
  delay(2000);
  for (int ELBOWrot = ELBOWservoMIN; ELBOWrot <= ELBOWservoMAX; ELBOWrot++) {
    srituhobby.setPWM(2, 0, ELBOWrot);
    delay(5);
  }
  delay(3000);
  CCW = SHOULDERservoMIN;
  for (int CW = SHOULDERservoMAX; CW >= SHOULDERservoMIN; CW--) {
    CCW = CCW + 1;
    srituhobby.setPWM(0, 0, CW-0);
    srituhobby.setPWM(1, 0, CCW);
    delay(5);
  }
  delay(5000);
}