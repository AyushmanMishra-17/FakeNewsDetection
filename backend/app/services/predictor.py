import os
import json
import joblib
import numpy as np

from app.utils.preprocess import clean_text
from app.services.credibility import credibility_score
from app.services.explainability import explain_prediction
from app.services.source_credibility import get_source_score

# -------------------------------------------------
# Resolve BASE directory safely (CRITICAL FIX)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
METADATA_PATH = os.path.join(MODELS_DIR, "metadata.json")

# -------------------------------------------------
# Load metadata safely
# -------------------------------------------------
if not os.path.exists(METADATA_PATH):
    raise FileNotFoundError(
        f"metadata.json not found at {METADATA_PATH}. "
        "Make sure models are committed or mounted correctly."
    )

with open(METADATA_PATH, "r") as f:
    meta = json.load(f)

MODEL_PATH = os.path.join(MODELS_DIR, meta["current_model"])

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model file not found at {MODEL_PATH}. "
        "Train the model or update metadata.json."
    )

# -------------------------------------------------
# Load ML model
# -------------------------------------------------
model = joblib.load(MODEL_PATH)

# -------------------------------------------------
# Prediction function
# -------------------------------------------------
def predict_news(text: str, source_url: str | None = None):
    cleaned = clean_text(text)

    prob = model.predict_proba([cleaned])[0]
    prediction = int(np.argmax(prob))
    confidence = float(np.max(prob))

    label = "REAL" if prediction == 1 else "FAKE"

    credibility = credibility_score(text)
    explanation = explain_prediction(model, cleaned)

    source_score = (
        get_source_score(source_url) if source_url else None
    )

    return {
        "prediction": label,
        "confidence": round(confidence, 4),
        "credibility_score": credibility,
        "source_score": source_score,
        "explanation": explanation,
    }
