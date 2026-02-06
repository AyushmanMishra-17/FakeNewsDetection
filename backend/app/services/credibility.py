def calculate_credibility(confidence, prediction):
    return round(confidence if prediction=="Real" else 100-confidence, 2)