from newspaper import Article
def extract_article_text(url):
    a = Article(url); a.download(); a.parse()
    return a.text