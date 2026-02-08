from transformers import pipeline
from app.services.credibility import calculate_credibility

# Load model directly from Hugging Face (no GitHub storage issue)
classifier = pipeline(
    "text-classification",
    model="mrm8488/bert-tiny-finetuned-fake-news-detection",
    tokenizer="mrm8488/bert-tiny-finetuned-fake-news-detection",
    device=-1  # CPU (Render-safe)
)

def predict_news(text: str, source_url: str | None = None):
    """
    Predicts whether news is Fake or Real.
    """

    result = classifier(text[:512])[0]  # truncate long articles safely

    label = result["label"]
    confidence = round(result["score"] * 100, 2)

    prediction = "Real" if label.lower() == "real" else "Fake"

    credibility = calculate_credibility(confidence, prediction)

    return {
        "prediction": prediction,
        "confidence": confidence,
        "credibility_score": credibility,
        "source": source_url
    }
