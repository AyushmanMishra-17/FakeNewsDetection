import re, nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))

def clean_text(text):
    text = re.sub(r"http\S+|[^a-zA-Z ]","", text.lower())
    return " ".join(w for w in text.split() if w not in STOPWORDS)