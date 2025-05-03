import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import numpy as np

# Paths
base_dir = "/home/oluwaniyi/ros2_ws/src/my_camera_pkg/german_traffic/train"  # Path to your training dataset

# Parameters
img_size = (128, 128)  # Resize all images to this size
batch_size = 32  # Number of images per batch

# Data preprocessing using ImageDataGenerator
datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,  # Normalize images to [0, 1]
    validation_split=0.2  # 20% for validation from the training data
)

# Train and validation generators
train_generator = datagen.flow_from_directory(
    base_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical",  # Multiclass classification
    subset="training"  # This subset is for training data
)

val_generator = datagen.flow_from_directory(
    base_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical",  # Multiclass classification
    subset="validation"  # This subset is for validation data
)

# Build a simple CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_size[0], img_size[1], 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(os.listdir(base_dir)), activation='softmax')  # Output layer matches number of classes
])

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
model.save("traffic_sign_recognition_model3.h5")

print("Model trained and saved!")
