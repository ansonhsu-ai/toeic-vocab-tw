"""
單元測試模組：test_exporter.py
測試說明：測試 CsvExporter 雙欄 CSV 輸出與 UTF-8 with BOM 編碼
"""

import os
import tempfile
import unittest
from src.exporter import CsvExporter
from src.models import VocabCardItem


class TestCsvExporter(unittest.TestCase):
    """
    測試 CsvExporter 雙欄匯出器類別
    """

    def test_export_to_csv(self):
        """
        測試雙欄 CSV 寫入格式
        """
        items = [
            VocabCardItem(
                word="ability",
                content="ability (n.) 能力、才幹\n【搭配詞】\nacademic ability 學術能力"
            )
        ]

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            CsvExporter.export_to_csv(items, tmp_path, include_header=False)
            self.assertTrue(os.path.exists(tmp_path))

            # 驗證 UTF-8 BOM
            with open(tmp_path, "rb") as bf:
                bom = bf.read(3)
                self.assertEqual(bom, b"\xef\xbb\xbf")

            # 驗證內容
            with open(tmp_path, "r", encoding="utf-8-sig") as f:
                content = f.read()
                self.assertTrue(content.startswith('"ability"') or content.startswith('ability'))
                self.assertIn("ability (n.) 能力、才幹", content)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
