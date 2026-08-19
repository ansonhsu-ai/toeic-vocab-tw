"""
腳本名稱：build_app.py
功能說明：將 TOEIC 單字資料與現代前端單一 HTML 模板整合成 index.html
"""

import json
import csv
import os

def build():
    csv_path = 'toeic_vocabulary.csv'
    cards_data = []
    if os.path.exists(csv_path):
        with open(csv_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if row and len(row) >= 2 and row[0].strip():
                    cards_data.append({
                        "id": i + 1,
                        "word": row[0].strip(),
                        "content": row[1].strip()
                    })
    print(f"Loaded {len(cards_data)} cards from CSV.")

    # 預載前 500 筆作為預設即用庫，載入迅速
    default_cards_json = json.dumps(cards_data[:500], ensure_ascii=False)

    template_file = 'template.html'
    if not os.path.exists(template_file):
        print("template.html not found.")
        return

    with open(template_file, 'r', encoding='utf-8') as tf:
        template = tf.read()

    output_html = template.replace('__DEFAULT_CARDS_DATA__', default_cards_json)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(output_html)
    print("index.html generated successfully.")

if __name__ == '__main__':
    build()
