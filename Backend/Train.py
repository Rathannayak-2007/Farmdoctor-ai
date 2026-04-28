"""
Training Script for FarmDoctor AI — Plant Disease Detection Model
Modernized for TensorFlow 2.16+ / Keras 3.

Usage:
    1. Place dataset in: Backend/dataset/PlantVillage/
    2. Run: python Train.py
"""

import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────
# Using pathlib for robust cross-platform path handling
SCRIPT_DIR = Path(__file__).parent
DATASET_DIR = SCRIPT_DIR / "dataset" / "PlantVillage"
MODEL_SAVE_PATH = SCRIPT_DIR / "plant_disease_model.keras"  # Modern .keras format
CLASS_NAMES_PATH = SCRIPT_DIR / "class_indices.json"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20
VALIDATION_SPLIT = 0.2

def get_data_augmentation():
    """Create a sequential model for data augmentation."""
    return models.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.2),
        layers.RandomContrast(0.1),
    ], name="data_augmentation")

def build_model(num_classes: int):
    """
    Build a MobileNetV2-based model with integrated preprocessing and augmentation.
    """
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(*IMAGE_SIZE, 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False  # Freeze the base

    inputs = layers.Input(shape=(*IMAGE_SIZE, 3))
    
    # 1. Apply Augmentation (only during training)
    x = get_data_augmentation()(inputs)
    
    # 2. Apply MobileNetV2 Preprocessing (Scaling from [0,255] to [-1,1])
    # This makes the model "portable" so it accepts raw pixel values.
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    
    # 3. Base Model
    x = base_model(x, training=False)
    
    # 4. Custom Top Layers
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.5)(x)
    
    x = layers.Dense(256, activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    
    outputs = layers.Dense(num_classes, activation="softmax")(x)
    
    model = models.Model(inputs, outputs)
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy", # Use sparse if labels are ints
        metrics=["accuracy"]
    )
    
    return model

def train():
    print("=" * 60)
    print("  FarmDoctor AI — Plant Disease Model Training (Modernized)")
    print("=" * 60)

    if not DATASET_DIR.exists():
        print(f"❌ Dataset not found at: {DATASET_DIR}")
        return

    # 1. Load Datasets using modern tf.data API
    # This is much faster and cleaner than ImageDataGenerator
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=VALIDATION_SPLIT,
        subset="training",
        seed=123,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode='int' # Use 'int' for sparse_categorical_crossentropy
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=VALIDATION_SPLIT,
        subset="validation",
        seed=123,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode='int'
    )

    class_names = train_ds.class_names
    num_classes = len(class_names)
    
    # Save class names for inference
    with open(CLASS_NAMES_PATH, "w") as f:
        json.dump({i: name for i, name in enumerate(class_names)}, f)
    print(f"✅ Saved {num_classes} classes to {CLASS_NAMES_PATH}")

    # 2. Optimize Performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # 3. Build and Train Model
    model = build_model(num_classes)
    model.summary()

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True, verbose=1),
        ModelCheckpoint(MODEL_SAVE_PATH, monitor="val_accuracy", save_best_only=True, verbose=1),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, min_lr=1e-6, verbose=1)
    ]

    print(f"\n🚀 Starting training for {EPOCHS} epochs...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=callbacks
    )

    print("\n✅ Training Complete!")
    print(f"Best Val Accuracy: {max(history.history['val_accuracy']):.4f}")
    print(f"Model saved to: {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train()
