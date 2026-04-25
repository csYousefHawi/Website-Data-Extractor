# Website Data Extractor

> An advanced web crawling tool that automatically extracts data from websites, featuring both a CLI and a modern graphical interface.

---

##  Overview

**Website Data Extractor** is a Python project that crawls websites and extracts four types of data:

-  **Emails** — extracted using Regex pattern matching
-  **Links** — all page links collected and converted to absolute URLs
-  **Images** — image source URLs extracted from the page
-  **News & Articles** — news content identified through keywords

The project supports **two modes**: Command Line (CLI) and Graphical Interface (GUI).

---

##  Project Structure

```
project/
│
├── main.py          # Entry point – CLI mode
├── gui_app.py       # Graphical interface (GUI) using CustomTkinter
├── fetcher.py       # Fetches web pages using Selenium
├── extractor.py     # Extracts data (emails, links, images, news)
├── saver.py         # Saves results (JSON, CSV, TXT)
├── config.py        # General settings
│
└── results/         # Output folder (auto-created)
    ├── data.json
    ├── data.csv
    ├── emails.txt
    ├── links.txt
    ├── images.txt
    └── news.txt
```

---

##  Requirements

### Python
Version **3.8** or higher.

### Dependencies

```bash
pip install selenium webdriver-manager beautifulsoup4 customtkinter
```

| Library | Purpose |
|---------|---------|
| `selenium` | Fetch dynamic web pages |
| `webdriver-manager` | Automatically manage ChromeDriver |
| `beautifulsoup4` | Parse HTML and extract elements |
| `customtkinter` | Build the graphical interface |

### Additional Requirements
- **Google Chrome** must be installed on your machine

---

##  How to Run

### 1. Command Line Mode (CLI)

```bash
python main.py
```

Then enter the target URL when prompted:

```
Enter Website URL: https://example.com
```

### 2. Graphical Interface (GUI)

```bash
python gui_app.py
```

A modern window will open allowing you to:
- Enter the target website URL
- Select crawl depth (1 or 2)
- Monitor the extraction process in real time

---

##  How It Works

```
Target URL
     │
     ▼
 fetcher.py  ──► Fetch HTML using Selenium (headless Chrome)
     │
     ▼
extractor.py ──► Extract: emails | links | images | news
     │
     ▼
  main.py    ──► Control crawling + track internal links
     │
     ▼
  saver.py   ──► Save results to results/ folder
```

### Crawl Depth
- **Depth 0**: Only the entered page
- **Depth 1**: The entered page + its directly linked pages
- **Depth 2 (default)**: Extends to the second level of internal links

> Only **internal links** (same domain) are crawled to avoid leaving the target website.

---

##  File Details

### `config.py`
Contains customizable settings:

```python
MAX_CRAWL_DEPTH = 2        # Maximum crawl depth
CRAWL_DELAY = 1.0          # Delay between requests (seconds)
OUTPUT_FOLDER = "results"  # Output folder name
NEWS_KEYWORDS = [...]      # Keywords for news detection
```

### `fetcher.py`
Uses **Selenium** in headless mode with:
- SSL error bypass
- Real browser User-Agent simulation
- Waits for JavaScript to load before extraction

### `extractor.py`
Contains four main functions:

| Function | Description |
|----------|-------------|
| `extract_emails(raw_html)` | Uses Regex to find email addresses |
| `extract_links(soup, base_url)` | Extracts all `<a href>` links and converts them to absolute URLs |
| `extract_images(soup, base_url)` | Extracts `<img src>` sources and converts them to absolute URLs |
| `extract_news(soup)` | Searches `h1/h2/h3/article/p` elements for news-related text |

### `saver.py`
Saves results in three formats inside the `results/` folder:

- **`.txt`** — a separate file for each data type
- **`data.json`** — all data combined in a formatted JSON file
- **`data.csv`** — a table with two columns: `Category` and `Value`

### `gui_app.py`
A graphical interface built with **CustomTkinter** featuring:
- URL input field
- Crawl depth selector
- Live log box showing real-time progress
- Runs the extraction in a separate **Thread** to keep the UI responsive

---



##  Important Notes

- This tool is intended for **educational and research purposes** only.
- Always verify that the target website allows crawling (check its `robots.txt`).
- Crawling may take longer on large websites or with higher depth settings.
- Make sure **Google Chrome** is installed before running the tool.

---

##  License

This project is open source for educational use.
