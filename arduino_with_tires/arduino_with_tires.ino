/// LED pins
const int leftLED = 13;  // Left LED connected to pin 13
const int rightLED = 11; // Right LED connected to pin 11

// H-bridge motor pins
const int RightForward = 3;
const int RightBack = 5;
const int LeftForward = 9;
const int LeftBack = 6;

// Motor speed variables
const int Rmotor_speed = 150; // Speed for the right motor (0-255)
const int Lmotor_speed = 150; // Speed for the left motor (0-255)

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Set LED pins as outputs
  pinMode(leftLED, OUTPUT);
  pinMode(rightLED, OUTPUT);

  // Set motor pins as outputs
  pinMode(RightForward, OUTPUT);
  pinMode(RightBack, OUTPUT);
  pinMode(LeftForward, OUTPUT);
  pinMode(LeftBack, OUTPUT);

  // Ensure all outputs are off initially
  Stop();
  digitalWrite(leftLED, LOW);
  digitalWrite(rightLED, LOW);

  // Debugging message
  Serial.println("Arduino is ready and waiting for commands...");
}

void loop() {
  // Check if data is available from Serial
  if (Serial.available() > 0) {
    // Read the command sent via serial
    char command = Serial.read();

    // Process the command
    if (command == 'L') {
      // Turn Left
      Left();
      digitalWrite(leftLED, HIGH);  // Turn on left LED
      digitalWrite(rightLED, LOW); // Turn off right LED
    } else if (command == 'R') {
      // Turn Right
      Right();
      digitalWrite(leftLED, LOW);  // Turn off left LED
      digitalWrite(rightLED, HIGH); // Turn on right LED
    } else if (command == 'F') {
      // Move Forward
      Forward();
      digitalWrite(leftLED, HIGH);  // Turn on both LEDs for forward
      digitalWrite(rightLED, HIGH);
    } else if (command == 'S') {
      // Stop
      Stop();
      digitalWrite(leftLED, LOW);   // Turn off both LEDs for stop
      digitalWrite(rightLED, LOW);
    } else {
      // Handle unknown commands
      Serial.println("Unknown command received.");
    }
  }
}

// Movement Functions
void Left() {
  Serial.println("LEFT");  // Debugging message
  analogWrite(RightForward, Rmotor_speed);
  digitalWrite(RightBack, LOW);
  digitalWrite(LeftForward, LOW);
  analogWrite(LeftBack, Lmotor_speed);
}

void Right() {
  Serial.println("RIGHT");  // Debugging message
  digitalWrite(RightForward, LOW);
  analogWrite(RightBack, Rmotor_speed);
  analogWrite(LeftForward, Lmotor_speed);
  digitalWrite(LeftBack, LOW);
}

void Forward() {
  Serial.println("FORWARD");  // Debugging message
  analogWrite(RightForward, Rmotor_speed);
  digitalWrite(RightBack, LOW);
  analogWrite(LeftForward, Lmotor_speed);
  digitalWrite(LeftBack, LOW);
}

void Stop() {
  Serial.println("STOP");  // Debugging message
  digitalWrite(RightForward, LOW);
  digitalWrite(RightBack, LOW);
  digitalWrite(LeftForward, LOW);
  digitalWrite(LeftBack, LOW);
}
