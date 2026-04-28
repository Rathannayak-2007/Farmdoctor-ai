"""
Training Script for FarmDoctor AI — Plant Disease Detection Model
Trains a CNN on the PlantVillage dataset using TensorFlow/Keras.

Usage:
    1. Download PlantVillage dataset and place in:
       Backend/dataset/PlantVillage/
       (each subdirectory = one class, e.g. Tomato___Early_blight/)

    2. Run:
       cd Backend
       python Train.py
"""

import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# ── Configuration ──────────────────────────────────────────────────────────────
DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset", "PlantVillage")
MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), "plant_disease_model.h5")
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20
VALIDATION_SPLIT = 0.2
NUM_CLASSES = 38  # PlantVillage has 38 classes


def create_model(num_classes: int) -> tf.keras.Model:
    """
    Create a CNN model for plant disease classification.
    Uses transfer learning with MobileNetV2 for efficiency.
    """
    # Use MobileNetV2 as base (lightweight and fast)
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(*IMAGE_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )

    # Freeze base model layers
    base_model.trainable = False

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(256, activation="relu"),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation="softmax"),
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


def create_data_generators():
    """Create training and validation data generators with augmentation."""
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest",
        validation_split=VALIDATION_SPLIT,
    )

    train_generator = train_datagen.flow_from_directory(
        DATASET_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="training",
        shuffle=True,
    )

    val_generator = train_datagen.flow_from_directory(
        DATASET_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="validation",
        shuffle=False,
    )

    return train_generator, val_generator


def train():
    """Main training function."""
    print("=" * 60)
    print("  FarmDoctor AI — Plant Disease Model Training")
    print("=" * 60)

    # Check dataset
    if not os.path.exists(DATASET_DIR):
        print(f"\n❌ Dataset not found at: {DATASET_DIR}")
        print("\nTo set up the dataset:")
        print("  1. Download PlantVillage dataset from Kaggle:")
        print("     https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset")
        print(f"  2. Extract to: {DATASET_DIR}")
        print("     Each subdirectory should be a class name (e.g., Tomato___Early_blight)")
        return

    # Count classes
    classes = [d for d in os.listdir(DATASET_DIR)
               if os.path.isdir(os.path.join(DATASET_DIR, d))]
    num_classes = len(classes)
    
    if num_classes != NUM_CLASSES:
        print(f"\n❌ CRITICAL ERROR: Found {num_classes} classes, but exactly {NUM_CLASSES} are required.")
        print("Your PlantVillage dataset is incomplete.")
        print("Please download the full dataset before training to prevent model mismatch crashes.")
        return
        
    print(f"\n📂 Found {num_classes} classes in dataset")
    print(f"📏 Image size: {IMAGE_SIZE}")
    print(f"📦 Batch size: {BATCH_SIZE}")
    print(f"🔄 Epochs: {EPOCHS}")

    # Create data generators
    print("\n📊 Creating data generators...")
    train_gen, val_gen = create_data_generators()
    print(f"   Training samples: {train_gen.samples}")
    print(f"   Validation samples: {val_gen.samples}")

    # Create model
    print("\n🏗️  Building model (MobileNetV2 transfer learning)...")
    model = create_model(num_classes)
    model.summary()

    # Callbacks
    callbacks = [
        EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1,
        ),
        ModelCheckpoint(
            MODEL_SAVE_PATH,
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1,
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-6,
            verbose=1,
        ),
    ]

    # Train
    print("\n🚀 Starting training...")
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS,
        callbacks=callbacks,
    )

    # Results
    best_val_acc = max(history.history["val_accuracy"])
    print(f"\n✅ Training complete!")
    print(f"   Best validation accuracy: {best_val_acc:.4f}")
    print(f"   Model saved to: {MODEL_SAVE_PATH}")
    print("\nYou can now use the model in the FarmDoctor AI app!")


if __name__ == "__main__":
    train()