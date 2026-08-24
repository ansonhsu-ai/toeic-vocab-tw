"""
模組名稱：exporter.py
模組說明：負責將 VocabCardItem 清單匯出為標準雙欄 CSV 檔案（使用 UTF-8 with BOM 編碼）
遵循原則：Single Responsibility Principle (SRP)
"""

import csv
from typing import List
from src.models import VocabCardItem


class CsvExporter:
    """
    負責單字庫 CSV 檔案寫入與格式化之匯出器類別
    """

    @staticmethod
    def export_to_csv(items: List[VocabCardItem], output_path: str, include_header: bool = False) -> None:
        """
        將 VocabCardItem 清單寫入至指定 CSV 檔案

        參數：
            items (List[VocabCardItem]): 雙欄閃卡資料清單
            output_path (str): 輸出 CSV 檔案之目標路徑
            include_header (bool): 是否包含標題列（預設 False，直接以第一列開始資料呈現）
        """
        with open(output_path, mode="w", encoding="utf-8-sig", newline="") as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

            if include_header:
                writer.writerow(["單字", "內容"])

            for item in items:
                writer.writerow([
                    item.word,
                    item.content,
                ])

        print(f"成功匯出 {len(items)} 筆單字至 {output_path}")
