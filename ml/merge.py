import pandas as pd

# Load datasets
fake = pd.read_csv("Fake.csv")
true = pd.read_csv("True.csv")

# Add labels
fake["label"] = 0   # Fake
true["label"] = 1   # Real

# Keep required columns
fake = fake[["title", "text", "label"]]
true = true[["title", "text", "label"]]

# Merge datasets
df = pd.concat([fake, true], ignore_index=True)

# Shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save final dataset
df.to_csv("fake_news.csv", index=False)

print("✅ fake_news.csv created successfully")
print("Shape:", df.shape)
print(df.head())
