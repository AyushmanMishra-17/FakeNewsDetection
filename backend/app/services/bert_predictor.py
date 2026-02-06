from transformers import pipeline
classifier = pipeline("text-classification", model="jy46604790/Fake-News-Bert-Detect", return_all_scores=True)