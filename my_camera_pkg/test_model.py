import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

# Paths
test_dir = "/home/oluwaniyi/ros2_ws/src/my_camera_pkg/german_traffic/Test"  # Replace with your test folder path
model_path = "traffic_sign_recognition_model.h5"  # Path to your saved model

# Parameters
img_size = (128, 128)  # Same size as during training

# Load the trained model
model = load_model(model_path)
print("Model loaded successfully!")

# Class indices (ensure this matches your training class mapping)
class_indices = {"33": 0, "34": 1, "35": 2, "14": 3}  # Update this mapping if needed
reversed_class_indices = {v: k for k, v in class_indices.items()}

# Load test images
test_images = [os.path.join(test_dir, fname) for fname in os.listdir(test_dir) if fname.endswith(".png")]

for img_path in test_images:
    # Load and preprocess image
    img = load_img(img_path, target_size=img_size)  # Load and resize image
    img_array = img_to_array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Predict
    prediction = model.predict(img_array)
    predicted_class = reversed_class_indices[np.argmax(prediction)]

    # Print results
    print(f"Image: {img_path} -> Predicted Class: {predicted_class}")
