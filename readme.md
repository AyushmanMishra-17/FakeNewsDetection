# 📰 Fake News Detection System

An end-to-end, industry-inspired Fake News Detection system that combines **Machine Learning**, **Credibility Scoring**, **Explainable AI**, **Blockchain-based audit logging**, and a **modern React UI**.

This project is designed to simulate how real-world misinformation detection systems operate, including continuous retraining and human-in-the-loop feedback.

---

## 🚀 Features

- ✅ Fake / Real news classification using ML
- 🌐 URL-based live article analysis
- 📊 Confidence & credibility scoring
- 🧠 Explainable AI (key influencing words)
- 🧾 Blockchain ledger for immutable prediction logs
- 🔁 Continuous retraining pipeline
- 👍 User feedback loop
- 🎨 Modern React + Tailwind UI

---

## 🏗️ Tech Stack

### Backend
- Python 3.10+
- FastAPI
- Scikit-learn
- Newspaper3k + BeautifulSoup
- Joblib
- Blockchain (custom implementation)

### Frontend
- React (Vite)
- Tailwind CSS
- Axios

### ML
- TF-IDF Vectorization
- Logistic Regression
- Incremental retraining support

---
## 📊 Dataset Information

Due to GitHub file size limits, datasets are not included in this repository.

### Required files:
- Fake.csv
- True.csv

Place them inside:
ml/data/


You may download equivalent datasets from:
- Kaggle Fake News Dataset
- ISOT Fake News Dataset
After placing datasets, run:

```bash
cd ml
python retrain.py
python train.py
```
```bash
## 📂 Project Structure
FakeNewsDetection/
│
├── ml/
│ ├── data/
│ ├── train.py
│ ├── retrain.py
│
├── backend/
│ ├── app/
│ │ ├── api/
│ │ ├── services/
│ │ ├── models/
│ │ └── main.py
│
├── frontend/
│ ├── src/
│ └── package.json
│
└── README.md
```



