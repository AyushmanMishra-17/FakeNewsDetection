import os
import joblib
import json
import torch
import nltk
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.services.credibility import calculate_credibility_score as credibility_score

nltk.download("stopwords", quiet=True)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
META_PATH = os.path.join(MODEL_DIR, "metadata.json")

_model = None
_metadata = None
_tokenizer = None
_transformer = None


def load_assets():
    global _model, _metadata, _tokenizer, _transformer

    if _model is None:
        _model = joblib.load(MODEL_PATH)

    if _metadata is None:
        with open(META_PATH, "r") as f:
            _metadata = json.load(f)

    if _tokenizer is None or _transformer is None:
        model_name = _metadata.get(
            "transformer_model",
            "distilbert-base-uncased-finetuned-sst-2-english"
        )
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _transformer = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            device_map="cpu"
        )


def predict_news(text: str, source_url: str = None):
    load_assets()

    inputs = _tokenizer(
        text[:512],
        truncation=True,
        padding=True,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = _transformer(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)
        confidence, label = torch.max(probs, dim=1)

    prediction = _metadata["label_map"].get(str(label.item()), "Unknown")

    confidence_pct = round(confidence.item() * 100, 2)

    return {
        "prediction": prediction,
        "confidence": confidence_pct,
        "credibility_score": credibility_score(confidence_pct, prediction),
        "source_url": source_url
    }
