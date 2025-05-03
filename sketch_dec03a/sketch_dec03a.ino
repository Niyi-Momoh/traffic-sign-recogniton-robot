const int leftLED = 13;  // Left LED connected to pin 13
const int rightLED = 11; // Right LED connected to pin 11

void setup() {
  Serial.begin(9600);       // Set the baud rate to match the ROS2 publisher
  pinMode(leftLED, OUTPUT); // Set the left LED pin as an output
  pinMode(rightLED, OUTPUT); // Set the right LED pin as an output
}

void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();

    if (receivedChar == 'R') {
      digitalWrite(rightLED, HIGH); // Turn on the right LED
      digitalWrite(leftLED, LOW);  // Turn off the left LED
      Serial.println("Turning Right");
    } else if (receivedChar == 'L') {
      digitalWrite(leftLED, HIGH); // Turn on the left LED
      digitalWrite(rightLED, LOW); // Turn off the right LED
      Serial.println("Turning Left");
    } else if (receivedChar == 'F') {
      digitalWrite(leftLED, HIGH);  // Turn on both LEDs
      digitalWrite(rightLED, HIGH);
      Serial.println("Moving Forward");
    } else if (receivedChar == 'S') {
      digitalWrite(leftLED, LOW);   // Turn off both LEDs
      digitalWrite(rightLED, LOW);
      Serial.println("Stopping");
    } else {
      Serial.println("Unknown Command");
    }
  }
}
