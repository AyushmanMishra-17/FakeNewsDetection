import pandas as pd, joblib
from sklearn.metrics import classification_report
from preprocessing import clean_text

model = joblib.load("../backend/app/models/model.pkl")
df = pd.read_csv("data/fake_news.csv")
df["text"] = df["text"].apply(clean_text)

print(classification_report(df["label"], model.predict(df["text"])))