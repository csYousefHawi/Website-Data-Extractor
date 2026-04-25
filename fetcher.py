# fetcher.py
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def get_html(url):
    """استخدام Selenium لجلب المحتوى الديناميكي وتجاوز حماية الـ SSL """
    options = Options()
    options.add_argument("--headless")  # التشغيل في الخلفية لسرعة الأداء
    options.add_argument("--ignore-certificate-errors")  # تجاوز أخطاء SSL
    options.add_argument("user-agent=Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        time.sleep(3)  # انتظار تحميل الجافا سكريبت 
        
        html_content = driver.page_source
        driver.quit()
        return BeautifulSoup(html_content, "html.parser"), html_content
    except Exception as e:
        print(f"Error: {e}")
        return None, None