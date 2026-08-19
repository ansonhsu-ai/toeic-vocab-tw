"""
模組名稱：exporter.py
模組說明：負責將 VocabItem 清單匯出為標準 CSV 檔案（使用 UTF-8 with BOM 編碼）
遵循原則：Single Responsibility Principle (SRP)
"""

import csv
from typing import List
from src.models import VocabItem


class CsvExporter:
    """
    負責單字庫 CSV 檔案寫入與格式化之匯出器類別
    """

    # 定義 CSV 欄位名稱對應（標題列）
    FIELDNAMES = [
        "單字",
        "中文釋義",
        "詞性",
        "星級",
        "多益分數區間",
        "情境類別",
        "【詞性變化】",
        "搭配詞",
        "英文例句",
        "中文例句",
        "考點重點",
    ]

    @staticmethod
    def export_to_csv(items: List[VocabItem], output_path: str) -> None:
        """
        將 VocabItem 清單寫入至指定 CSV 檔案

        參數：
            items (List[VocabItem]): 轉換完成的單字資料清單
            output_path (str): 輸出 CSV 檔案之目標路徑
        """
        # 使用 utf-8-sig (帶 BOM 的 UTF-8)，以確保繁體中文在 Excel 及各平台環境均能正常開啟不亂碼
        with open(output_path, mode="w", encoding="utf-8-sig", newline="") as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

            # 寫入標題列
            writer.writerow(CsvExporter.FIELDNAMES)

            # 依序寫入資料列
            for item in items:
                writer.writerow([
                    item.english_word,
                    item.chinese_definition,
                    item.parts_of_speech,
                    item.star_rating,
                    item.toeic_score_range,
                    item.category,
                    item.word_forms,
                    item.collocations,
                    item.example_en,
                    item.example_zh,
                    item.exam_tips,
                ])

        print(f"成功匯出 {len(items)} 筆單字至 {output_path}")
