from urllib.parse import urlparse

SOURCE_SCORES = {
    "reuters.com": 95,
    "bbc.com": 92,
    "apnews.com": 93,
    "theguardian.com": 90,
    "nytimes.com": 90,
    "cnn.com": 88
}

def get_domain(url: str):
    return urlparse(url).netloc.replace("www.", "")

def source_credibility_score(url: str | None):
    if not url:
        return None
    domain = get_domain(url)
    return SOURCE_SCORES.get(domain, 50)  # unknown source → neutral score
