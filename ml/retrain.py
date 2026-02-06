import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Correct paths (robust & OS-safe)
base_data = BASE_DIR / "data" / "fake_news.csv"
live_data = BASE_DIR / "data" / "live_collected.csv"
output_file = BASE_DIR / "data" / "retrain_ready.csv"

feedback_file = BASE_DIR.parent / "backend" / "app" / "feedback" / "feedback.csv"

# Load datasets
base = pd.read_csv(base_data)

if live_data.exists():
    live = pd.read_csv(live_data)
else:
    live = pd.DataFrame(columns=["title", "text", "label"])

if feedback_file.exists():
    feedback = pd.read_csv(
        feedback_file,
        names=["text", "pred", "label"]
    )
    feedback = feedback[["text", "label"]]
else:
    feedback = pd.DataFrame(columns=["text", "label"])

# Merge everything
combined = pd.concat([base, live, feedback], ignore_index=True)
combined = combined.sample(frac=1, random_state=42).reset_index(drop=True)

combined.to_csv(output_file, index=False)

print("✅ Retraining dataset created:", output_file)
print("Total samples:", len(combined))
