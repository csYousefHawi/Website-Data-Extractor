# extractor.py
import re
from urllib.parse import urljoin
from config import NEWS_KEYWORDS

def extract_emails(raw_html):
    # Regex لاستخراج الإيميلات الفريدة [cite: 24, 25]
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return sorted(set(re.findall(pattern, raw_html))) # فريدة فقط [cite: 22, 26]

def extract_links(soup, base_url):
    # استخراج الروابط وتحويلها لمطلقة [cite: 28, 29]
    links = set()
    for tag in soup.find_all("a", href=True):
        links.add(urljoin(base_url, tag["href"]))
    return sorted(links)

def extract_images(soup, base_url):
    # استخراج الصور وتحويلها لمطلقة [cite: 32, 33]
    images = set()
    for tag in soup.find_all("img", src=True):
        images.add(urljoin(base_url, tag["src"]))
    return sorted(images)

def extract_news(soup):
    # استخراج العناوين والمقالات حسب متطلب المشروع [cite: 37, 38, 39]
    news = set()
    for tag in soup.find_all(['h1', 'h2', 'h3', 'article', 'p']):
        text = tag.get_text(strip=True)
        if any(word in text.lower() for word in NEWS_KEYWORDS) and len(text) > 20:
            news.add(text)
    return sorted(news)