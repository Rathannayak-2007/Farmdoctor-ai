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
import sys

# Force UTF-8 encoding for standard output to support emojis in Windows console
sys.stdout.reconfigure(encoding='utf-8')

import tensorflow as tf
from tensorflow.keras import layers, models
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
    """Create training and validation data generators.

    Uses the modern tf.keras.utils.image_dataset_from_directory API
    (replaces the deprecated ImageDataGenerator from keras.preprocessing).
    Augmentation is applied only to training data via preprocessing layers.
    """
    # --- Training dataset (with augmentation) ---
    train_dataset = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=VALIDATION_SPLIT,
        subset="training",
        seed=42,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
        shuffle=True,
    )

    # --- Validation dataset (no augmentation, only rescaling) ---
    val_dataset = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=VALIDATION_SPLIT,
        subset="validation",
        seed=42,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
        shuffle=False,
    )

    # Normalise pixel values to [0, 1]
    normalization = layers.Rescaling(1.0 / 255)

    # Augmentation pipeline — applied to training only
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),          # ~20 degrees
        layers.RandomZoom(0.2),
        layers.RandomTranslation(0.2, 0.2),  # width/height shift
    ], name="data_augmentation")

    train_dataset = train_dataset.map(
        lambda x, y: (data_augmentation(normalization(x), training=True), y),
        num_parallel_calls=tf.data.AUTOTUNE,
    ).prefetch(tf.data.AUTOTUNE)

    val_dataset = val_dataset.map(
        lambda x, y: (normalization(x), y),
        num_parallel_calls=tf.data.AUTOTUNE,
    ).prefetch(tf.data.AUTOTUNE)

    return train_dataset, val_dataset


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
    
    # BUG FIX: Instead of aborting, warn if the class count differs and continue
    # with the actual detected count. This allows training on partial or custom datasets.
    if num_classes != NUM_CLASSES:
        print(f"\n⚠️  Warning: Found {num_classes} classes (expected {NUM_CLASSES}).")
        print("   Proceeding with the detected class count. The saved model will reflect this.")
        print("   If you need exactly 38 classes, please use the full PlantVillage dataset.")
        
    print(f"\n📂 Found {num_classes} classes in dataset")
    print(f"📏 Image size: {IMAGE_SIZE}")
    print(f"📦 Batch size: {BATCH_SIZE}")
    print(f"🔄 Epochs: {EPOCHS}")

    # Create data generators
    print("\n📊 Creating data generators...")
    train_gen, val_gen = create_data_generators()
    # tf.data.Dataset does not expose .samples; cardinality() gives batch count
    train_batches = train_gen.cardinality().numpy()
    val_batches = val_gen.cardinality().numpy()
    print(f"   Training batches : {train_batches}  (~{train_batches * BATCH_SIZE} samples)")
    print(f"   Validation batches: {val_batches}  (~{val_batches * BATCH_SIZE} samples)")

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
    # BUG FIX: Use .get() to avoid KeyError if training is stopped early
    # or if val_accuracy is not tracked (e.g. wrong metric name).
    val_acc_history = history.history.get("val_accuracy", [])
    if val_acc_history:
        best_val_acc = max(val_acc_history)
        print(f"\n✅ Training complete!")
        print(f"   Best validation accuracy: {best_val_acc:.4f}")
    else:
        print(f"\n✅ Training complete! (val_accuracy not recorded)")
    print(f"   Model saved to: {MODEL_SAVE_PATH}")
    print("\nYou can now use the model in the FarmDoctor AI app!")


if __name__ == "__main__":
    train()