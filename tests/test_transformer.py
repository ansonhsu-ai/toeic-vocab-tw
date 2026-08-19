"""
單元測試模組：test_transformer.py
測試說明：測試 VocabTransformer 雙欄閃卡轉換邏輯
"""

import unittest
from src.transformer import VocabTransformer


class TestVocabTransformer(unittest.TestCase):
    """
    測試 VocabTransformer 轉換器類別
    """

    def test_transformer_filters_multi_word(self):
        """
        測試過濾長度超過一個單字的資料
        """
        transformer = VocabTransformer()
        multi_word_item = {
            "english_word": "arrive in London",
            "chinese_definition": "到達倫敦",
            "parts_of_speech": ["verb"],
        }
        result = transformer.transform_entry(multi_word_item)
        self.assertIsNone(result)

    def test_transformer_single_word_success(self):
        """
        測試單一單字轉換成功生成 VocabCardItem
        """
        transformer = VocabTransformer()
        single_word_item = {
            "english_word": "ability",
            "chinese_definition": "能力、才幹",
            "parts_of_speech": ["noun"],
            "examples": [
                {"english": "She has the ability to solve complex problems.", "chinese": "她有解決複雜問題的能力。"}
            ],
            "exam_tips": ["常見搭配：academic ability (學術能力)"]
        }
        result = transformer.transform_entry(single_word_item)
        self.assertIsNotNone(result)
        self.assertEqual(result.word, "ability")
        self.assertIn("ability (n.) 能力、才幹", result.content)
        self.assertIn("academic ability 學術能力", result.content)


if __name__ == "__main__":
    unittest.main()
