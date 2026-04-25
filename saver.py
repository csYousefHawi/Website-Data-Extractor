# saver.py
import os
import json
import csv

def save_all(data, base_url):
    if not os.path.exists("results"): os.makedirs("results") # [cite: 60, 64]
    
    # حفظ الملفات النصية المنفصلة [cite: 67, 69, 70, 71]
    for key in ["emails", "links", "images", "news"]:
        with open(f"results/{key}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(list(data[key])))

    # حفظ JSON [cite: 61]
    with open("results/data.json", "w", encoding="utf-8") as f:
        json.dump({k: list(v) for k, v in data.items()}, f, indent=4, ensure_ascii=False)

    # حفظ CSV [cite: 62]
    with open("results/data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Value"])
        for cat, vals in data.items():
            for v in vals: writer.writerow([cat, v])