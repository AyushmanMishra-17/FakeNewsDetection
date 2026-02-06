import json, joblib
from app.services.credibility import calculate_credibility
from app.services.source_credibility import source_credibility_score
from app.services.explainability import explain_prediction
from app.blockchain.blockchain import Blockchain

with open("app/models/metadata.json") as f:
    meta = json.load(f)

model = joblib.load(f"app/models/{meta['current_model']}")
bc = Blockchain()

def predict_news(text, source_url=None):
    probs = model.predict_proba([text])[0]
    pred = model.predict([text])[0]

    prediction = "Real" if pred == 1 else "Fake"
    confidence = round(max(probs) * 100, 2)

    src_score = source_credibility_score(source_url)
    credibility = calculate_credibility(confidence, prediction)

    if src_score:
        credibility = round((credibility * 0.7 + src_score * 0.3), 2)

    explanation = explain_prediction(model, text)

    block = bc.add_block({
        "prediction": prediction,
        "confidence": confidence,
        "credibility_score": credibility,
        "source_score": src_score,
    })

    return {
        "prediction": prediction,
        "confidence": confidence,
        "credibility_score": credibility,
        "source_score": src_score,
        "explanation": explanation,
        "block_hash": block.hash
    }
