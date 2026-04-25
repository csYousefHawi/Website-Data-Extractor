# saver.py
import os
import json
import csv

def save_all(data, base_url):
    if not os.path.exists("results"): os.makedirs("results") 
    
    for key in ["emails", "links", "images", "news"]:
        with open(f"results/{key}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(list(data[key])))

    with open("results/data.json", "w", encoding="utf-8") as f:
        json.dump({k: list(v) for k, v in data.items()}, f, indent=4, ensure_ascii=False)

    with open("results/data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Value"])
        for cat, vals in data.items():
            for v in vals: writer.writerow([cat, v])
