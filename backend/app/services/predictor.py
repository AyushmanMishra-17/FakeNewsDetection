import os
import json
import joblib
import requests

from app.services.explainability import explain_prediction
from app.services.credibility import calculate_credibility
from app.services.source_credibility import source_score
from app.utils.preprocess import preprocess_text

MODEL_DIR = "models"
MODEL_PATH = f"{MODEL_DIR}/model.pkl"
META_PATH = f"{MODEL_DIR}/metadata.json"

# 🔗 Replace this with your actual model URL later
MODEL_URL = "https://YOUR_MODEL_HOST_URL/model.pkl"

os.makedirs(MODEL_DIR, exist_ok=True)

def download_model():
    if not os.path.exists(MODEL_PATH):
        print("⬇️ Downloading ML model...")
        r = requests.get(MODEL_URL, stream=True)
        with open(MODEL_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print("✅ Model downloaded")

download_model()

model = joblib.load(MODEL_PATH)

# Metadata fallback (safe)
if os.path.exists(META_PATH):
    with open(META_PATH) as f:
        metadata = json.load(f)
else:
    metadata = {"version": "cloud"}

def predict_news(text: str, source_url: str | None = None):
    clean = preprocess_text(text)
    pred = model.predict([clean])[0]
    prob = model.predict_proba([clean])[0].max() * 100

    label = "Real" if pred == 1 else "Fake"

    credibility = calculate_credibility(prob, label)
    explanation = explain_prediction(model, clean)

    source = source_score(source_url) if source_url else None

    return {
        "prediction": label,
        "confidence": round(prob, 2),
        "credibility_score": credibility,
        "source_score": source,
        "explanation": explanation,
        "model_version": metadata.get("version", "unknown")
    }
