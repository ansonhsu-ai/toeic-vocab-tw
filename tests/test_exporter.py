"""
單元測試模組：test_exporter.py
測試說明：測試 CsvExporter CSV 檔案輸出格式與 UTF-8 with BOM 編碼
"""

import os
import tempfile
import unittest
from src.exporter import CsvExporter
from src.models import VocabItem


class TestCsvExporter(unittest.TestCase):
    """
    測試 CsvExporter 匯出器類別
    """

    def test_export_to_csv(self):
        """
        測試匯出 CSV 格式、標題列及資料列正確性
        """
        items = [
            VocabItem(
                english_word="abandon",
                chinese_definition="放棄；拋棄",
                parts_of_speech="verb",
                star_rating=3,
                toeic_score_range="600-780",
                category="營運管理",
                word_forms="verb: abandon, abandons",
                collocations="abandon a project 放棄專案; abandon a plan 放棄計畫",
                example_en="The company decided to abandon the project.",
                example_zh="公司決定放棄這個專案。",
                exam_tips="常用考點"
            )
        ]

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            CsvExporter.export_to_csv(items, tmp_path)
            self.assertTrue(os.path.exists(tmp_path))

            # 驗證 UTF-8 with BOM
            with open(tmp_path, "rb") as bf:
                bom = bf.read(3)
                self.assertEqual(bom, b"\xef\xbb\xbf")

            # 驗證文字讀取
            with open(tmp_path, "r", encoding="utf-8-sig") as f:
                lines = f.readlines()
                self.assertEqual(len(lines), 2)  # Header + 1 row
                self.assertIn("單字", lines[0])
                self.assertIn("abandon", lines[1])
                self.assertIn("放棄；拋棄", lines[1])
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
