import joblib
import json
from pathlib import Path
from app.services.credibility import calculate_credibility

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "model.pkl"
META_PATH = MODEL_DIR / "metadata.json"

# Load model safely
if not MODEL_PATH.exists():
    raise RuntimeError("Model file not found. Upload model.pkl")

model = joblib.load(MODEL_PATH)

with open(META_PATH) as f:
    meta = json.load(f)

def predict_news(text: str, source_url: str = None):
    prob = model.predict_proba([text])[0]
    label = model.classes_[prob.argmax()]
    confidence = round(prob.max() * 100, 2)

    credibility = calculate_credibility(confidence, label)

    return {
        "prediction": label,
        "confidence": confidence,
        "credibility_score": credibility,
        "source": source_url
    }
