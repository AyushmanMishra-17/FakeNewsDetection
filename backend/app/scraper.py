import socket
import requests
from newspaper import Article
from bs4 import BeautifulSoup

socket.setdefaulttimeout(10)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def extract_article_text(url: str) -> str:
    # 1️⃣ Try newspaper3k
    try:
        article = Article(url, language="en")
        article.download()
        article.parse()
        if len(article.text) > 200:
            return article.text
    except Exception as e:
        print("⚠ newspaper3k failed:", e)

    # 2️⃣ Fallback: requests + BeautifulSoup
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text() for p in paragraphs)

        if len(text) > 200:
            return text

    except Exception as e:
        print("❌ requests fallback failed:", e)

    # 3️⃣ Give up gracefully
    return ""
