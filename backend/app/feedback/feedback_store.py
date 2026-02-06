import csv

FEEDBACK_FILE = "app/feedback/feedback.csv"

def save_feedback(text, model_pred, user_label):
    with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([text, model_pred, user_label])
