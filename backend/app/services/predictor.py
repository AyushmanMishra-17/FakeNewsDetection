import os
import joblib
import requests
import json
from app.services.credibility import calculate_credibility
from app.services.source_credibility import get_source_score

MODEL_URL = os.getenv(
    "MODEL_URL",
    "https://huggingface.co/AyushmanMishra/fake-news-classifier-tfidf/resolve/main/model.pkl"
)

META_URL = os.getenv(
    "META_URL",
    "https://huggingface.co/AyushmanMishra/fake-news-classifier-tfidf/resolve/main/metadata.json"
)

MODEL_CACHE = "/tmp/model.pkl"
META_CACHE = "/tmp/metadata.json"

_model = None
_meta = None


def load_model():
    global _model, _meta

    if _model is None:
        r = requests.get(MODEL_URL)
        with open(MODEL_CACHE, "wb") as f:
            f.write(r.content)
        _model = joblib.load(MODEL_CACHE)

    if _meta is None:
        r = requests.get(META_URL)
        with open(META_CACHE, "wb") as f:
            f.write(r.content)
        with open(META_CACHE) as f:
            _meta = json.load(f)

    return _model, _meta


def predict_news(text, source_url=None):
    model, meta = load_model()

    prob = model.predict_proba([text])[0]
    pred_idx = prob.argmax()
    prediction = meta["labels"][pred_idx]
    confidence = round(prob[pred_idx] * 100, 2)

    credibility = calculate_credibility(confidence, prediction)
    source_score = get_source_score(source_url) if source_url else None

    return {
        "prediction": prediction,
        "confidence": confidence,
        "credibility_score": credibility,
        "source_score": source_score,
        "model": meta["model_name"]
    }
