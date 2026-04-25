import customtkinter as ctk
import threading
import os
import json
import csv
import re
import time
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime

# إعدادات الواجهة الرسومية المتقدمة
ctk.set_appearance_mode("dark")  # وضع داكن أنيق
ctk.set_default_color_theme("blue")  # نظام ألوان أزرق

class CyberExtractorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # إعدادات النافذة الرئيسية
        self.title("🛡️ Cyber Data Extractor Pro v2.0")
        self.geometry("900x750")
        self.minsize(800, 650)
        
        # تعيين أيقونة النافذة (اختياري - إذا كان لديك ملف ico)
        # self.iconbitmap("icon.ico")
        
        # إطار رئيسي مع مسافات
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ========== الهيدر ==========
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        # عنوان رئيسي مع تأثير
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="🛡️ CYBER DATA EXTRACTOR", 
            font=ctk.CTkFont(size=32, weight="bold", family="Microsoft Sans Serif"),
            text_color="#00b4d8"
        )
        self.title_label.pack()
        
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Advanced Web Crawler & Data Extraction Tool",
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color="#adb5bd"
        )
        self.subtitle_label.pack()
        
        # ========== منطقة الإدخال ==========
        self.input_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, border_width=2, border_color="#2b2d42")
        self.input_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        # عنوان القسم
        self.section1_label = ctk.CTkLabel(
            self.input_frame, 
            text="⚙️ CONFIGURATION", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#00b4d8"
        )
        self.section1_label.pack(anchor="w", padx=20, pady=(15, 10))
        
        # حقل الرابط
        self.url_label = ctk.CTkLabel(self.input_frame, text="Target URL:", font=ctk.CTkFont(size=14, weight="bold"))
        self.url_label.pack(anchor="w", padx=20)
        
        self.url_entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="https://example.com", 
            width=600,
            height=45,
            font=ctk.CTkFont(size=14)
        )
        self.url_entry.pack(pady=(5, 15), padx=20)
        
        # إطار اختيار العمق
        self.depth_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.depth_frame.pack(fill="x", pady=(0, 20), padx=20)
        
        self.depth_label = ctk.CTkLabel(
            self.depth_frame, 
            text="📊 Crawl Depth:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.depth_label.pack(side="left", padx=(0, 20))
        
        self.depth_var = ctk.StringVar(value="2")
        self.depth_menu = ctk.CTkSegmentedButton(
            self.depth_frame, 
            values=["1 (Basic)", "2 (Standard)", "3 (Deep)"], 
            variable=self.depth_var,
            width=300,
            height=35
        )
        self.depth_menu.pack(side="left")
        
        # ========== أزرار التحكم ==========
        self.control_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, border_width=2, border_color="#2b2d42")
        self.control_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        self.button_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.button_frame.pack(pady=20)
        
        # زر البدء مع تأثير
        self.start_btn = ctk.CTkButton(
            self.button_frame, 
            text="🚀 START EXTRACTION", 
            command=self.start_thread, 
            fg_color="#00b4d8",
            hover_color="#0096c7",
            width=250,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10
        )
        self.start_btn.pack(side="left", padx=10)
        
        # زر المسح
        self.clear_btn = ctk.CTkButton(
            self.button_frame, 
            text="🗑️ CLEAR LOGS", 
            command=self.clear_logs, 
            fg_color="#6c757d",
            hover_color="#495057",
            width=150,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        self.clear_btn.pack(side="left", padx=10)
        
        # زر فتح مجلد النتائج
        self.open_folder_btn = ctk.CTkButton(
            self.button_frame, 
            text="📁 OPEN RESULTS", 
            command=self.open_results_folder, 
            fg_color="#495057",
            hover_color="#343a40",
            width=150,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        self.open_folder_btn.pack(side="left", padx=10)
        
        # ========== منطقة الحالة مع شريط التقدم ==========
        self.status_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, border_width=2, border_color="#2b2d42")
        self.status_frame.pack(fill="both", expand=True, padx=10)
        
        self.status_header = ctk.CTkFrame(self.status_frame, fg_color="transparent")
        self.status_header.pack(fill="x", padx=20, pady=(15, 10))
        
        self.status_label = ctk.CTkLabel(
            self.status_header, 
            text="📋 EXTRACTION LOGS", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#00b4d8"
        )
        self.status_label.pack(side="left")
        
        self.status_count = ctk.CTkLabel(
            self.status_header, 
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color="#6c757d"
        )
        self.status_count.pack(side="right")
        
        # شريط التقدم
        self.progress_bar = ctk.CTkProgressBar(self.status_frame, height=8, corner_radius=4)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 10))
        self.progress_bar.set(0)
        
        # صندوق النصوص المحسن
        self.status_box = ctk.CTkTextbox(
            self.status_frame, 
            width=800, 
            height=300,
            font=ctk.CTkFont(size=12),
            wrap="word",
            corner_radius=10
        )
        self.status_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # إعداد الألوان للنصوص
        self.status_box.tag_config("success", foreground="#2ecc71")
        self.status_box.tag_config("error", foreground="#e74c3c")
        self.status_box.tag_config("info", foreground="#3498db")
        self.status_box.tag_config("warning", foreground="#f39c12")
        
        # عرض رسالة ترحيب
        self.log("✨ Cyber Data Extractor Pro initialized successfully!", "success")
        self.log("⚡ Ready to extract data from websites", "info")
        
    def log(self, message, tag=None):
        """إضافة رسالة إلى سجل الحالة مع تنسيق"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}\n"
        
        if tag:
            self.status_box.insert("end", formatted_msg, tag)
        else:
            self.status_box.insert("end", formatted_msg)
        self.status_box.see("end")
        
        # تحديث عداد الرسائل
        line_count = int(self.status_box.index('end-1c').split('.')[0])
        self.status_count.configure(text=f"{line_count} lines")
        
    def clear_logs(self):
        """مسح سجل الحالة"""
        self.status_box.delete("1.0", "end")
        self.log("Logs cleared successfully", "info")
        self.progress_bar.set(0)
        
    def open_results_folder(self):
        """فتح مجلد النتائج"""
        results_path = os.path.join(os.getcwd(), "results")
        if os.path.exists(results_path):
            os.startfile(results_path)
            self.log(f"📂 Opened results folder: {results_path}", "success")
        else:
            self.log("❌ Results folder not found. Run extraction first.", "error")
        
    def update_progress(self, current, total):
        """تحديث شريط التقدم"""
        if total > 0:
            progress = current / total
            self.progress_bar.set(progress)
        
    def start_thread(self):
        url = self.url_entry.get().strip()
        if not url.startswith("http"):
            self.log("❌ Error: Please enter a valid URL starting with http:// or https://", "error")
            return
        
        # تحويل قيمة العمق
        depth_map = {
            "1 (Basic)": 1,
            "2 (Standard)": 2,
            "3 (Deep)": 3
        }
        depth = depth_map.get(self.depth_var.get(), 2)
        
        self.start_btn.configure(state="disabled", text="⏳ EXTRACTING...", fg_color="#e67e22")
        self.log(f"🎯 Target URL: {url}", "info")
        self.log(f"📊 Crawl Depth: {depth}", "info")
        self.log("🕷️ Starting extraction process...", "info")
        
        threading.Thread(target=self.run_process, args=(url, depth), daemon=True).start()

    def run_process(self, start_url, max_depth):
        domain = urlparse(start_url).netloc
        visited = set()
        to_visit = [(start_url, 0)]
        all_data = {"emails": set(), "links": set(), "images": set(), "news": set()}
        
        total_pages = 1  # تقدير أولي
        
        # إعدادات Selenium المتطورة لتجاوز الحماية
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        try:
            self.log("🔄 Initializing Chrome driver...", "info")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                """
            })
            self.log("✅ Chrome driver initialized successfully", "success")

            page_count = 0
            while to_visit:
                url, depth = to_visit.pop(0)
                if url in visited or depth > max_depth: 
                    continue
                
                page_count += 1
                self.log(f"🌐 Processing [{page_count}]: {url} (Depth: {depth})", "info")
                visited.add(url)
                
                # تحديث شريط التقدم
                self.update_progress(len(visited), total_pages + len(to_visit))
                
                try:
                    driver.get(url)
                    time.sleep(2)  # انتظار تحميل المحتوى الديناميكي
                    
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    html_raw = driver.page_source

                    # 1. استخراج الإيميلات
                    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html_raw)
                    new_emails = [e for e in emails if e not in all_data["emails"]]
                    all_data["emails"].update(emails)
                    if new_emails:
                        self.log(f"📧 Found {len(new_emails)} new email(s)", "success")

                    # 2. استخراج الروابط
                    links_found = 0
                    for a in soup.find_all('a', href=True):
                        link = urljoin(url, a['href'])
                        if link not in all_data["links"]:
                            all_data["links"].add(link)
                            links_found += 1
                        
                        # إضافة الروابط الداخلية فقط للزحف
                        if depth < max_depth and urlparse(link).netloc == domain and link not in visited:
                            to_visit.append((link, depth + 1))
                    if links_found:
                        self.log(f"🔗 Found {links_found} new link(s)", "info")

                    # 3. استخراج الصور
                    images_found = 0
                    for img in soup.find_all('img', src=True):
                        img_url = urljoin(url, img['src'])
                        if img_url not in all_data["images"]:
                            all_data["images"].add(img_url)
                            images_found += 1
                    if images_found:
                        self.log(f"🖼️ Found {images_found} new image(s)", "info")

                    # 4. استخراج الأخبار
                    news_found = 0
                    for tag in soup.find_all(['h1', 'h2', 'h3', 'article', 'p']):
                        text = tag.get_text().strip()
                        if len(text) > 30:
                            if text not in all_data["news"]:
                                all_data["news"].add(text)
                                news_found += 1
                    if news_found:
                        self.log(f"📰 Found {news_found} new news article(s)", "success")

                except Exception as e:
                    self.log(f"⚠️ Error processing {url}: {str(e)[:50]}", "warning")
                    continue

            driver.quit()
            
            # عرض ملخص النتائج
            self.log("\n" + "="*50, "info")
            self.log("📊 EXTRACTION SUMMARY:", "success")
            self.log(f"📧 Emails extracted: {len(all_data['emails'])}", "info")
            self.log(f"🔗 Links extracted: {len(all_data['links'])}", "info")
            self.log(f"🖼️ Images extracted: {len(all_data['images'])}", "info")
            self.log(f"📰 News articles: {len(all_data['news'])}", "info")
            self.log(f"🌐 Total pages crawled: {page_count}", "info")
            self.log("="*50, "info")
            
            # حفظ النتائج
            self.save_all(all_data)
            self.log("✅ All data extracted and saved successfully!", "success")
            self.log(f"📁 Results saved in: {os.path.join(os.getcwd(), 'results')}", "info")
            
            self.progress_bar.set(1)
            
        except Exception as e:
            self.log(f"❌ Critical Error: {str(e)}", "error")
        
        self.start_btn.configure(state="normal", text="🚀 START EXTRACTION", fg_color="#00b4d8")

    def save_all(self, data):
        """حفظ النتائج في ملفات مختلفة"""
        path = "results"
        if not os.path.exists(path): 
            os.makedirs(path)
            self.log(f"📁 Created results folder: {path}", "info")

        # حفظ الملفات النصية المنفصلة
        file_count = 0
        for key in ["emails", "links", "images", "news"]:
            file_path = f"{path}/{key}.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                content = "\n".join(sorted(list(data[key])))
                f.write(content)
            file_count += 1
            self.log(f"💾 Saved: {key}.txt ({len(data[key])} items)", "success")

        # حفظ JSON
        with open(f"{path}/data.json", "w", encoding="utf-8") as f:
            json.dump({k: sorted(list(v)) for k, v in data.items()}, f, indent=4, ensure_ascii=False)
        file_count += 1
        self.log(f"💾 Saved: data.json", "success")

        # حفظ CSV
        with open(f"{path}/data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Value"])
            for cat, vals in data.items():
                for v in vals:
                    writer.writerow([cat, v])
        file_count += 1
        self.log(f"💾 Saved: data.csv", "success")
        
        self.log(f"✅ Total {file_count} files saved successfully!", "success")

if __name__ == "__main__":
    app = CyberExtractorGUI()
    app.mainloop()