import csv
from urllib.parse import urlparse
from newspaper import Article
from source_registry import REAL_SOURCES, FAKE_SOURCES

def get_domain(url):
    return urlparse(url).netloc.replace("www.", "")

def label_from_source(domain):
    if domain in REAL_SOURCES:
        return REAL_SOURCES[domain]
    if domain in FAKE_SOURCES:
        return FAKE_SOURCES[domain]
    return None

def scrape_and_store(urls):
    with open("ml/data/live_collected.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for url in urls:
            domain = get_domain(url)
            label = label_from_source(domain)
            if label is None:
                continue

            article = Article(url)
            article.download()
            article.parse()

            writer.writerow([article.title, article.text, label])
