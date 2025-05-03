import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import numpy as np

# Paths
base_dir = "/home/oluwaniyi/ros2_ws/src/my_camera_pkg/german_traffic/train"  # Replace with the path to your dataset

# Folders to include
required_folders = ["Right", "Left", "forward", "Stop"]

# Parameters
img_size = (128, 128)  # Resize all images to this size
batch_size = 32  # Number of images per batch

# Data preprocessing using ImageDataGenerator
datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,  # Normalize images to [0, 1]
    validation_split=0.2  # 20% for validation
)

# Train and validation generators
train_generator = datagen.flow_from_directory(
    base_dir,
    target_size=img_size,
    batch_size=batch_size,
    classes=required_folders,  # Specify only the required folders
    class_mode="categorical",  # Multiclass classification
    subset="training"
)

val_generator = datagen.flow_from_directory(
    base_dir,
    target_size=img_size,
    batch_size=batch_size,
    classes=required_folders,
    class_mode="categorical",
    subset="validation"
)

# Build a simple CNN model
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input

model = Sequential([
    Input(shape=(128, 128, 3)),
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(4, activation='softmax')
])
model.save("recreated_model.h5")



# Compile the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train the model
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10  # You can adjust the number of epochs
)

# Save the model
#model.save("traffic_sign_recognition_model.h5")

print("Model trained and saved!")
