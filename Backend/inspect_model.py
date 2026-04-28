import tensorflow as tf
import os

model_path = r"c:\Users\Rathan nayak\OneDrive\Desktop\Hackthon\Framdoctor-ai\Backend\farmdoctor_v3.h5"

if os.path.exists(model_path):
    try:
        model = tf.keras.models.load_model(model_path)
        print(f"Model Name: {model.name}")
        print(f"Input Shape: {model.input_shape}")
        
        # Check for Rescaling layer
        for layer in model.layers:
            if 'rescaling' in layer.name.lower():
                print(f"Found Rescaling layer: {layer.name}")
                if hasattr(layer, 'scale'):
                    print(f"  Scale: {layer.scale}")
                if hasattr(layer, 'offset'):
                    print(f"  Offset: {layer.offset}")
        
        # Check first few layers to guess architecture
        print("\nFirst 5 layers:")
        for layer in model.layers[:5]:
            print(f" - {layer.name}: {layer.__class__.__name__}")
            
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Model not found")
