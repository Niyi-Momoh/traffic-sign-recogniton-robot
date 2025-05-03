import cv2
import numpy as np
from tensorflow.keras.models import load_model
import serial
import time
import threading

# Path to your trained model
MODEL_PATH = '/home/oluwaniyi/traffic_sign_recognition_model_compatible.h5'  # Update with the correct path
model = load_model(MODEL_PATH)

# Map model outputs to commands
CLASS_LABELS = {0: "Right", 1: "Left", 2: "Forward", 3: "Stop"}  # Ensure this matches the number of classes from your training
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
    """Preprocess the image for the model."""
    img = cv2.resize(frame, (128, 128))  # Resize to model input size
    img_array = np.expand_dims(img / 255.0, axis=0)  # Normalize and add batch dimension
    return img_array

def send_command_to_arduino(command):
    """Send the command to the Arduino via serial."""
    if arduino:
        try:
            arduino.write(command.encode())
            print(f"Command '{command}' sent to Arduino.")
        except Exception as e:
            print(f"Failed to send command to Arduino: {e}")

def process_frame(frame):
    """Process the frame to predict and send command."""
    preprocessed_frame = preprocess_image(frame)
    prediction = model.predict(preprocessed_frame)
    predicted_class_index = np.argmax(prediction)

    # Ensure the class index is within the expected range
    if predicted_class_index not in CLASS_LABELS:
        print(f"Unexpected class index: {predicted_class_index}. Skipping prediction.")
        return None, None

    predicted_label = CLASS_LABELS[predicted_class_index]
    arduino_command = COMMAND_MAP[predicted_label]
    
    # Return the prediction label and command
    return predicted_label, arduino_command

def display_and_predict():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from camera. Exiting...")
            break

        # Display the live video feed
        cv2.imshow("Traffic Sign Detection", frame)

        # Process the frame to predict
        predicted_label, arduino_command = process_frame(frame)
        
        if predicted_label:
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
        arduino.close()

def main():
    # Run the prediction and display in a separate thread for smoother video feed
    display_thread = threading.Thread(target=display_and_predict)
    display_thread.start()
    display_thread.join()

if __name__ == "__main__":
    main()
