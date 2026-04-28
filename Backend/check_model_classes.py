import tensorflow as tf
import os

model_path = r"c:\Users\Rathan nayak\OneDrive\Desktop\Hackthon\Framdoctor-ai\Backend\farmdoctor_v3.h5"

if os.path.exists(model_path):
    try:
        model = tf.keras.models.load_model(model_path)
        print("Model loaded.")
        
        # Check if model has a class_names attribute (some custom models do)
        if hasattr(model, 'class_names'):
            print(f"Class Names found in model: {model.class_names}")
        
        # Check if it's a Sequential model and look at the last layer
        last_layer = model.layers[-1]
        print(f"Last layer: {last_layer.name}, Units: {getattr(last_layer, 'units', 'N/A')}")
        
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Model not found")
