import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import LearningRateScheduler, EarlyStopping, ModelCheckpoint

# Paths
base_dir = "/home/oluwaniyi/ros2_ws/src/my_camera_pkg/german_traffic/train"  # Replace with your dataset path
required_folders = ["Right", "Left", "Forward", "Stop"]  # Updated folder names

# Parameters
img_size = (128, 128)  # Image dimensions
batch_size = 32  # Number of images per batch
epochs = 20  # Number of training epochs

# Data preprocessing and augmentation
datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,  # Normalize pixel values to [0, 1]
    validation_split=0.2,  # Reserve 20% of data for validation
    rotation_range=15,  # Rotate images randomly by up to 15 degrees
    width_shift_range=0.1,  # Shift images horizontally by up to 10%
    height_shift_range=0.1,  # Shift images vertically by up to 10%
    zoom_range=0.1  # Zoom in or out by up to 10%
)

# Training and validation data generators
train_generator = datagen.flow_from_directory(
    base_dir,
    target_size=img_size,
    batch_size=batch_size,
    classes=required_folders,  # Use updated class names
    class_mode="categorical",
    subset="training"
)

val_generator = datagen.flow_from_directory(
    base_dir,
    target_size=img_size,
    batch_size=batch_size,
    classes=required_folders,  # Use updated class names
    class_mode="categorical",
    subset="validation"
)

# Load a pre-trained MobileNetV2 model and fine-tune
base_model = MobileNetV2(input_shape=(img_size[0], img_size[1], 3), include_top=False, weights="imagenet")
base_model.trainable = False  # Freeze the pre-trained layers

# Build the model
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),  # Reduce dimensionality of features
    layers.Dense(128, activation="relu"),  # Add a fully connected layer
    layers.Dropout(0.5),  # Dropout for regularization
    layers.Dense(len(required_folders), activation="softmax")  # Output layer
])

# Compile the model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Callbacks
callbacks = [
    LearningRateScheduler(lambda epoch: 1e-3 * (0.1 ** (epoch // 10)), verbose=1),  # Reduce LR every 10 epochs
    EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True),  # Stop early if validation loss stops improving
    ModelCheckpoint("best_model.keras", save_best_only=True, monitor="val_loss")  # Save the best model
]

# Train the model
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=epochs,
    callbacks=callbacks
)

# Save the final model
model.save("traffic_sign_recognition_model2.h5")
print("Model trained and saved!")
