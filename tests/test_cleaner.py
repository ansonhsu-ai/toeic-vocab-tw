"""
單元測試模組：test_cleaner.py
測試說明：測試 VocabCleaner 各項資料清洗、過濾、詞性變化改寫與搭配詞簡化邏輯
"""

import unittest
from src.cleaner import VocabCleaner


class TestVocabCleaner(unittest.TestCase):
    """
    測試 VocabCleaner 清洗器類別
    """

    def test_is_single_word(self):
        """
        測試單字長度過濾規則（單一單字回傳 True，多詞/片語回傳 False）
        """
        # 合法單一單字
        self.assertTrue(VocabCleaner.is_single_word("abandon"))
        self.assertTrue(VocabCleaner.is_single_word("  abandoned  "))
        self.assertTrue(VocabCleaner.is_single_word("state-of-the-art"))

        # 片語或多字詞
        self.assertFalse(VocabCleaner.is_single_word("A be followed by B"))
        self.assertFalse(VocabCleaner.is_single_word("abide by"))
        self.assertFalse(VocabCleaner.is_single_word("in terms of"))
        self.assertFalse(VocabCleaner.is_single_word(""))
        self.assertFalse(VocabCleaner.is_single_word("   "))
        self.assertFalse(VocabCleaner.is_single_word(None))

    def test_rename_derived_words(self):
        """
        測試將「衍生字」改寫為「【詞性變化】」
        """
        text1 = "注意[衍生字] enable (動詞) 與 ability (名詞)。"
        expected1 = "注意【詞性變化】 enable (動詞) 與 ability (名詞)。"
        self.assertEqual(VocabCleaner.rename_derived_words(text1), expected1)

        text2 = "此單字無其他衍生字。"
        expected2 = "此單字無其他【詞性變化】。"
        self.assertEqual(VocabCleaner.rename_derived_words(text2), expected2)

        text3 = "【衍生字】：ability, unable"
        expected3 = "【詞性變化】：ability, unable"
        self.assertEqual(VocabCleaner.rename_derived_words(text3), expected3)

    def test_extract_collocations_max_two(self):
        """
        測試搭配詞簡化萃取（最多兩組，直接中英對照，不帶多餘說明）
        """
        tips = [
            "常見搭配詞組：在多益考試中常以 abandon a project (放棄專案)、abandon a plan (放棄計畫) 或 abandon an idea (放棄念頭) 的形式出現。",
            "商業情境應用：通常用於描述因預算刪減而停止計畫。"
        ]
        collocations = VocabCleaner.extract_collocations(tips, "abandon")
        self.assertIn("abandon a project 放棄專案", collocations)
        self.assertIn("abandon a plan 放棄計畫", collocations)
        self.assertNotIn("abandon an idea", collocations)
        items = collocations.split("; ")
        self.assertEqual(len(items), 2)

    def test_extract_collocations_quoted(self):
        """
        測試單引號形式的搭配詞萃取
        """
        tips = [
            "常見搭配詞：'abandoned building' (廢棄建築)、'abandoned vehicle' (廢棄車輛) 及 'abandoned project' (被中止的計畫)。"
        ]
        collocations = VocabCleaner.extract_collocations(tips, "abandoned")
        self.assertIn("abandoned building 廢棄建築", collocations)
        self.assertIn("abandoned vehicle 廢棄車輛", collocations)
        items = collocations.split("; ")
        self.assertEqual(len(items), 2)

    def test_extract_single_example(self):
        """
        測試例句擷取（只取第一句英文與中文）
        """
        examples = [
            {"english": "The storm is expected to abate by tomorrow morning.", "chinese": "預計明天早上風暴會減弱。"},
            {"english": "The company is working to abate the negative impact.", "chinese": "公司正在努力減輕負面影響。"}
        ]
        en, zh = VocabCleaner.extract_single_example(examples)
        self.assertEqual(en, "The storm is expected to abate by tomorrow morning.")
        self.assertEqual(zh, "預計明天早上風暴會減弱。")

        # 測試空列表情況
        empty_en, empty_zh = VocabCleaner.extract_single_example([])
        self.assertEqual(empty_en, "")
        self.assertEqual(empty_zh, "")


if __name__ == "__main__":
    unittest.main()
