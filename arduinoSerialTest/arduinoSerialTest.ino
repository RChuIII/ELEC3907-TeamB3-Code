//int incomingByte = 0; // Variable for the incomming byte from the serial com.
String a; // Variable for the incoming text from the serial com.

void setup() {
  // Set the LED pins to OUTPUTs.
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);  

  Serial.begin(9600);  // Begin the serial communication with a baud rate of 9600 B/s
}

void loop() {
  // If the serial communication is available, read the the incoming bytes...
  // For an incoming string, trim it to remove trailing spaces and \n (new lines).
  if(Serial.available() > 0){
    //incomingByte = Serial.read();
    a = Serial.readString();
    a.trim();
    Serial.print("Command Recieved: ");
    Serial.println(a);
  }
  
  // If and else if statements for parsing the serial in.
  if (a=="red_on"){ digitalWrite(3, HIGH); }
  else if (a=="red_off"){ digitalWrite(3, LOW); }
  else if (a=="green_on"){ digitalWrite(4, HIGH); }
  else if (a=="green_off"){ digitalWrite(4, LOW); }
  else if (a=="blue_on"){ digitalWrite(5, HIGH); }
  else if (a=="blue_off"){ digitalWrite(5, LOW); }
  else if (a=="white_on"){ digitalWrite(6, HIGH); }
  else if (a=="white_off"){ digitalWrite(6, LOW); }
  else if (a=="clear"){
    digitalWrite(3, LOW);
    digitalWrite(4, LOW);
    digitalWrite(5, LOW);
    digitalWrite(6, LOW);
  }
  else {
    Serial.println("Invalid Command");
  }

  a=""; // Reset the serial in string.
}
