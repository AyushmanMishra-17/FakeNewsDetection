import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import os
import json

DATA_PATH = "ml/data/retrain_ready.csv"
MODEL_DIR = "backend/app/models"
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
META_PATH = os.path.join(MODEL_DIR, "metadata.json")

os.makedirs(MODEL_DIR, exist_ok=True)

# Load data
df = pd.read_csv(DATA_PATH)
df = df.dropna(subset=["text", "label"])

X = df["text"]
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        stop_words="english",
        max_df=0.9,
        min_df=5
    )),
    ("clf", LogisticRegression(max_iter=1000))
])

# Train
pipeline.fit(X_train, y_train)

# Evaluate
acc = accuracy_score(y_test, pipeline.predict(X_test))
print(f"Accuracy: {acc:.4f}")

# Save model
joblib.dump(pipeline, MODEL_PATH)

# Save metadata
metadata = {
    "model_name": "TFIDF + LogisticRegression",
    "accuracy": round(acc, 4),
    "labels": ["Fake", "Real"]
}

with open(META_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print("Model & metadata saved successfully")
