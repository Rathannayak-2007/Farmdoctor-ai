
import os, json, io
import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf

app = FastAPI(title="FarmDoctor AI", version="1.0")

# Allow calls from Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

MODEL_DIR  = os.environ.get("MODEL_DIR", "./models")
IMAGE_SIZE = (224, 224)
model        = None
class_names  = {}
pesticide_db = {}

@app.on_event("startup")
async def load_model():
    global model, class_names, pesticide_db
    print("Loading FarmDoctor model...")
    model = tf.keras.models.load_model(f"{MODEL_DIR}/farmdoctor_v3.h5")
    with open(f"{MODEL_DIR}/class_names.json")  as f: class_names  = json.load(f)
    with open(f"{MODEL_DIR}/pesticide_db.json") as f: pesticide_db = json.load(f)
    print(f"Model ready. Classes: {len(class_names)}")

def preprocess(image_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize(IMAGE_SIZE)
    arr = np.array(img, dtype=np.float32)
    return np.expand_dims(arr, axis=0)

def get_severity(confidence: float, class_name: str) -> str:
    if "Healthy" in class_name:
        return "Healthy"
    viral = {"Mosaic_Virus", "Yellow_Leaf_Curl_Virus", "Citrus_Greening"}
    disease = class_name.split("__")[-1] if "__" in class_name else ""
    if any(v in disease for v in viral): return "Severe"
    if confidence >= 0.95: return "Severe"
    if confidence >= 0.80: return "Moderate"
    return "Mild"

@app.get("/")
async def root():
    return {"status": "FarmDoctor AI is running", "classes": len(class_names)}

@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/diagnose")
async def diagnose(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(503, "Model not loaded yet. Please wait.")
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Please upload an image file.")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(400, "Image too large. Max 10MB.")

    try:
        img_array = preprocess(contents)
    except Exception as e:
        raise HTTPException(400, f"Could not process image: {e}")

    preds       = model.predict(img_array, verbose=0)[0]
    top_indices = np.argsort(preds)[::-1][:3]

    top_class      = class_names[str(top_indices[0])]
    top_confidence = float(preds[top_indices[0]])
    parts          = top_class.split("__")
    crop           = parts[0].replace("_", " ")
    disease        = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown"
    is_healthy     = "Healthy" in disease

    db       = pesticide_db.get(top_class, {
        "cause": None, "cultural_control": [], "pesticides": []
    })
    severity = get_severity(top_confidence, top_class)

    top3 = [
        {
            "class": class_names[str(i)].replace("__", " — ").replace("_", " "),
            "confidence": round(float(preds[i]) * 100, 2)
        }
        for i in top_indices
    ]

    return {
        "crop":             crop,
        "disease":          disease,
        "is_healthy":       is_healthy,
        "confidence":       round(top_confidence * 100, 2),
        "severity":         severity,
        "low_confidence":   top_confidence < 0.70,
        "cause":            db.get("cause"),
        "cultural_control": db.get("cultural_control", []),
        "pesticides":       db.get("pesticides", []),
        "top3":             top3,
    }
