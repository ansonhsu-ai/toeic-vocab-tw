"""
專案名稱：TOEIC 單字庫處理程式
檔案名稱：main.py
檔案說明：主程式進入點，串接下載、資料清理轉換與雙欄閃卡格式 CSV 匯出
"""

import os
import sys
from src.downloader import DatasetDownloader
from src.exporter import CsvExporter
from src.transformer import VocabTransformer


def run_pipeline(output_csv: str = "toeic_vocabulary.csv", cache_json: str = "toeic_raw.json") -> None:
    """
    執行完整的 TOEIC 單字庫下載、清洗轉換與雙欄閃卡 CSV 匯出流程

    參數：
        output_csv (str): 目標輸出的 CSV 檔案名稱
        cache_json (str): 原始 JSON 暫存檔案名稱
    """
    print("=== 開始執行 TOEIC 單字集雙欄閃卡格式轉換 ===")

    # 1. 下載或載入資料
    downloader = DatasetDownloader(cache_path=cache_json)
    raw_data = downloader.fetch_data()
    print(f"原始資料筆數: {len(raw_data)} 筆")

    # 2. 轉換與清洗資料
    transformer = VocabTransformer()
    transformed_items = transformer.transform_all(raw_data)
    print(f"過濾並排版後單字筆數 (僅保留單一單字): {len(transformed_items)} 筆")

    # 3. 匯出為雙欄 CSV
    CsvExporter.export_to_csv(transformed_items, output_csv, include_header=False)
    print(f"=== 處理完成！檔案已儲存至: {os.path.abspath(output_csv)} ===")


if __name__ == "__main__":
    output_filename = "toeic_vocabulary.csv"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    run_pipeline(output_csv=output_filename)
