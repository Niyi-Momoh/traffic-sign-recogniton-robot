from tensorflow.keras.models import load_model, Model
from tensorflow.keras.models import load_model

# Path to the updated model
MODEL_PATH = "/home/oluwaniyi/recreated_model_fixed.h5"

try:
    model = load_model(MODEL_PATH)
    print("Model loaded successfully!")
    print("Input shape:", model.input_shape)
except Exception as e:
    print(f"Error loading model: {e}")

