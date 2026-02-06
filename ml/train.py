import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

# --------------------------------------------------
# PATH SETUP (robust, OS-independent)
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR.parent / "backend" / "app" / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# DATA SELECTION (SMART LOGIC)
# --------------------------------------------------

RETRAIN_FILE = DATA_DIR / "retrain_ready.csv"
BASE_FILE = DATA_DIR / "fake_news.csv"

if RETRAIN_FILE.exists():
    print("✅ Using retrained dataset:", RETRAIN_FILE.name)
    df = pd.read_csv(RETRAIN_FILE)
else:
    print("⚠ Using base dataset:", BASE_FILE.name)
    df = pd.read_csv(BASE_FILE)

# --------------------------------------------------
# DATA VALIDATION
# --------------------------------------------------

required_cols = {"text", "label"}
if not required_cols.issubset(df.columns):
    raise ValueError(f"Dataset must contain columns: {required_cols}")

df = df.dropna(subset=["text", "label"])

X = df["text"]
y = df["label"]

print(f"📊 Total samples: {len(df)}")

# --------------------------------------------------
# TRAIN / TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# --------------------------------------------------
# ML PIPELINE
# --------------------------------------------------

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        stop_words="english",
        max_df=0.9,
        min_df=5,
        ngram_range=(1, 2)
    )),
    ("clf", LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        n_jobs=-1
    ))
])

print("🚀 Training model...")
pipeline.fit(X_train, y_train)

# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"✅ Accuracy: {accuracy:.4f}")
print(f"✅ F1 Score: {f1:.4f}")

# --------------------------------------------------
# MODEL VERSIONING
# --------------------------------------------------

existing_models = list(MODEL_DIR.glob("model_v*.pkl"))
next_version = len(existing_models) + 1
model_name = f"model_v{next_version}.pkl"

model_path = MODEL_DIR / model_name
joblib.dump(pipeline, model_path)

print(f"💾 Model saved as: {model_name}")

# --------------------------------------------------
# METADATA UPDATE (OPTIONAL BUT RECOMMENDED)
# --------------------------------------------------

metadata = {
    "current_model": model_name,
    "trained_on": pd.Timestamp.now().strftime("%Y-%m-%d"),
    "accuracy": round(accuracy, 4),
    "f1_score": round(f1, 4),
    "dataset": "retrain_ready.csv" if RETRAIN_FILE.exists() else "fake_news.csv"
}

metadata_path = MODEL_DIR / "metadata.json"
with open(metadata_path, "w") as f:
    import json
    json.dump(metadata, f, indent=2)

print("🧾 Metadata updated")
print("🎉 Training complete!")
