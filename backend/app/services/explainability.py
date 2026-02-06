import numpy as np

def explain_prediction(model, text, top_n=5):
    vectorizer = model.named_steps["tfidf"]
    classifier = model.named_steps["clf"]

    features = vectorizer.get_feature_names_out()
    X = vectorizer.transform([text]).toarray()[0]

    coef = classifier.coef_[0]
    contributions = X * coef

    top_indices = np.argsort(np.abs(contributions))[-top_n:][::-1]

    return [
        {
            "word": features[i],
            "impact": round(contributions[i], 4)
        }
        for i in top_indices if X[i] > 0
    ]
