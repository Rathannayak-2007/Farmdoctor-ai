"""
Image Analysis Module for FarmDoctor AI
Handles plant disease detection from leaf images using a TensorFlow/Keras model.
"""

import os
import numpy as np
from PIL import Image
import io

# Import class names and knowledge base
from .knowledge import CLASS_NAMES, knowledge_base

# ── Constants ──────────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "farmdoctor_v3.h5")
IMAGE_SIZE = (224, 224)  # Model expects 224x224


def load_model():
    """Load the trained plant disease detection model."""
    try:
        import tensorflow as tf
        if os.path.exists(MODEL_PATH):
            model = tf.keras.models.load_model(MODEL_PATH)
            print(f"[OK] Model loaded from {MODEL_PATH}")
            return model
        else:
            print(f"[WARNING] Model file not found at {MODEL_PATH}")
            print("   Run Train.py first to train and save the model.")
            return None
    except ImportError:
        print("[WARNING] TensorFlow not installed. Install with: pip install tensorflow")
        return None
    except Exception as e:
        print(f"[ERROR] Error loading model: {e}")
        return None


# Try to load model at startup
_model = load_model()


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Preprocess an image for model prediction.

    Args:
        image_bytes: Raw image bytes from upload.

    Returns:
        Preprocessed numpy array ready for prediction.
    """
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("RGB")
    image = image.resize(IMAGE_SIZE)

    # Convert to numpy array
    # Convert to numpy array
    img_array = np.array(image).astype(np.float32)

    # Use official EfficientNet preprocessing (handles scaling based on model requirements)
    import tensorflow as tf
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)

    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


def predict_disease(image_bytes: bytes) -> dict:
    """
    Predict plant disease from an uploaded leaf image.

    Args:
        image_bytes: Raw image bytes from the uploaded file.

    Returns:
        Dictionary with prediction results including:
        - class_name: The predicted disease class
        - confidence: Prediction confidence (0-1)
        - disease_info: Detailed disease information from knowledge base
    """
    global _model

    if _model is None:
        _model = load_model()
        if _model is None:
            return {
                "error": True,
                "message": (
                    "Model not available. Please run Train.py first to train the model, "
                    "or place 'plant_disease_model.h5' in the Backend directory."
                ),
                "class_name": None,
                "confidence": 0,
                "disease_info": None,
            }

    try:
        # Preprocess the image
        try:
            processed_image = preprocess_image(image_bytes)
        except Exception as img_err:
            return {
                "error": True,
                "message": f"Invalid image format or corrupted file. Please upload a valid JPG/PNG.",
                "class_name": None,
                "confidence": 0,
                "disease_info": None,
            }

        # Make prediction
        predictions = _model.predict(processed_image, verbose=0)
        predicted_index = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_index])

        # Get class name
        if predicted_index < len(CLASS_NAMES):
            class_name = CLASS_NAMES[predicted_index]
        else:
            class_name = f"Unknown_class_{predicted_index}"

        # Get disease info from knowledge base
        disease_info = knowledge_base.get_disease_info(class_name)

        return {
            "error": False,
            "class_name": class_name,
            "confidence": round(confidence * 100, 2),
            "disease_info": disease_info,
            "debug_index": int(predicted_index)
        }

    except Exception as e:
        return {
            "error": True,
            "message": f"Error during prediction: {str(e)}",
            "class_name": None,
            "confidence": 0,
            "disease_info": None,
        }


def is_model_available() -> bool:
    """Check if the disease detection model is loaded and ready."""
    return _model is not None