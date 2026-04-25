# main.py
from fetcher import get_html
from extractor import *
from saver import save_all
from config import MAX_CRAWL_DEPTH
from urllib.parse import urlparse

def start_crawl(start_url):
    domain = urlparse(start_url).netloc
    visited = set()
    to_visit = [(start_url, 0)]
    all_results = {"emails": set(), "links": set(), "images": set(), "news": set()}

    while to_visit:
        url, depth = to_visit.pop(0)
        if url in visited or depth > MAX_CRAWL_DEPTH: continue 
        
        print(f"[*] Crawling: {url} (Depth: {depth})")
        visited.add(url)
        
        soup, raw = get_html(url)
        if not soup: continue

        all_results["emails"].update(extract_emails(raw))
        all_results["images"].update(extract_images(soup, url))
        all_results["news"].update(extract_news(soup))
        
        links = extract_links(soup, url)
        all_results["links"].update(links)

       
        if depth < MAX_CRAWL_DEPTH:
            for link in links:
                if urlparse(link).netloc == domain:
                    to_visit.append((link, depth + 1))

    save_all(all_results, start_url)
    print("\n[✓] Done! Results saved in 'results' folder.")

if __name__ == "__main__":
    target = input("Enter Website URL: ").strip()
    start_crawl(target)
