"""import cv2
import numpy as np
from tensorflow.keras.models import load_model
import serial
import time

# Path to your trained model
MODEL_PATH = '/home/oluwaniyi/ros2_ws/src/traffic_sign_recognition_model2.h5'  # Update with the correct path
model = load_model(MODEL_PATH)

# Map model outputs to commands
CLASS_LABELS = {0: "Right", 1: "Left", 2: "Forward", 3: "Stop"}
COMMAND_MAP = {"Right": "R", "Left": "L", "Forward": "F", "Stop": "S"}

# Initialize serial communication with Arduino
try:
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Update port if needed
    time.sleep(2)  # Wait for Arduino to initialize
    print("Arduino connected successfully.")
except serial.SerialException as e:
    print(f"Failed to connect to Arduino: {e}")
    arduino = None

# Initialize the camera
cap = cv2.VideoCapture(0)  # Default camera index
if not cap.isOpened():
    print("Error: Camera could not be opened.")
    exit()

def preprocess_image(frame):
    #Preprocess the image for the model.
    img = cv2.resize(frame, (128, 128))  # Resize to model input size
    img_array = np.expand_dims(img / 255.0, axis=0)  # Normalize and add batch dimension
    return img_array

def send_command_to_arduino(command):
    #Send the command to the Arduino via serial.
    if arduino:
        try:
            arduino.write(command.encode())
            print(f"Command '{command}' sent to Arduino.")
        except Exception as e:
            print(f"Failed to send command to Arduino: {e}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame from camera. Exiting...")
        break

    # Display the live video feed
    cv2.imshow("Traffic Sign Detection", frame)

    # Preprocess the frame and make predictions
    preprocessed_frame = preprocess_image(frame)
    prediction = model.predict(preprocessed_frame)
    predicted_class_index = np.argmax(prediction)
    predicted_label = CLASS_LABELS[predicted_class_index]
    arduino_command = COMMAND_MAP[predicted_label]

    # Display the prediction on the video feed
    cv2.putText(frame, f"Prediction: {predicted_label}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Send the corresponding command to Arduino
    send_command_to_arduino(arduino_command)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()"""



import cv2
import numpy as np
from tensorflow.keras.models import load_model
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import time

# Path to your trained model
MODEL_PATH = '/home/oluwaniyi/ros2_ws/src/traffic_sign_recognition_model2.h5'  # Update with the correct path
model = load_model(MODEL_PATH)

# Map model outputs to commands
CLASS_LABELS = {0: "Right", 1: "Left", 2: "Forward", 3: "Stop"}
COMMAND_MAP = {"Right": "R", "Left": "L", "Forward": "F", "Stop": "S"}

# Initialize serial communication with Arduino
try:
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Update port if needed
    time.sleep(2)  # Wait for Arduino to initialize
    print("Arduino connected successfully.")
except serial.SerialException as e:
    print(f"Failed to connect to Arduino: {e}")
    arduino = None

def preprocess_image(frame):
    """Preprocess the image for the model."""
    img = cv2.resize(frame, (128, 128))  # Resize to model input size
    img_array = np.expand_dims(img / 255.0, axis=0)  # Normalize and add batch dimension
    return img_array

class TrafficSignPublisher(Node):
    """ROS2 Node to publish traffic sign predictions."""

    def __init__(self):
        super().__init__('traffic_sign_publisher')
        self.publisher_ = self.create_publisher(String, 'traffic_sign_command', 10)
        self.cap = cv2.VideoCapture(0)  # Default camera index
        if not self.cap.isOpened():
            self.get_logger().error("Error: Camera could not be opened.")
            rclpy.shutdown()
        self.timer = self.create_timer(0.1, self.process_frame)

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().error("Failed to capture frame from camera.")
            self.cap.release()
            rclpy.shutdown()
            return

        # Preprocess the frame and make predictions
        preprocessed_frame = preprocess_image(frame)
        prediction = model.predict(preprocessed_frame)
        predicted_class_index = np.argmax(prediction)
        predicted_label = CLASS_LABELS[predicted_class_index]
        arduino_command = COMMAND_MAP[predicted_label]

        # Publish to ROS2 topic
        self.publisher_.publish(String(data=predicted_label))
        self.get_logger().info(f"Prediction published: {predicted_label}")

        # Send the command to Arduino
        self.send_command_to_arduino(arduino_command)

        # Display the prediction on the video feed
        cv2.putText(frame, f"Prediction: {predicted_label}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Traffic Sign Detection", frame)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
            rclpy.shutdown()

    def send_command_to_arduino(self, command):
        """Send the command to the Arduino via serial."""
        if arduino:
            try:
                arduino.write(command.encode())
                self.get_logger().info(f"Command '{command}' sent to Arduino.")
            except Exception as e:
                self.get_logger().error(f"Failed to send command to Arduino: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = TrafficSignPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Node stopped by user.")
    finally:
        node.cap.release()
        cv2.destroyAllWindows()
        if arduino:
            arduino.close()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
