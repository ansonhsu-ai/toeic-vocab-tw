"""
單元測試模組：test_transformer.py
測試說明：測試 VocabTransformer 整體轉換、模型封裝與過濾邏輯
"""

import unittest
from src.transformer import VocabTransformer


class TestVocabTransformer(unittest.TestCase):
    """
    測試 VocabTransformer 轉換器類別
    """

    def test_transformer_filters_multi_word(self):
        """
        測試轉換器是否正確過濾長度超過一個單字的項目
        """
        transformer = VocabTransformer()
        multi_word_item = {
            "english_word": "A be followed by B",
            "chinese_definition": "接續在...之後",
            "parts_of_speech": ["verb"],
            "star_rating": 4,
            "toeic_score_range": "600-780",
            "category": "辦公日常",
            "examples": [{"english": "A is followed by B.", "chinese": "A 接在 B 之後。"}],
            "exam_tips": ["固定片語"]
        }
        result = transformer.transform_entry(multi_word_item)
        self.assertIsNone(result)

    def test_transformer_single_word_success(self):
        """
        測試單一單字正常轉換並填入所有欄位
        """
        transformer = VocabTransformer()
        single_word_item = {
            "english_word": "abbreviate",
            "chinese_definition": "縮寫；簡略化",
            "parts_of_speech": ["verb"],
            "star_rating": 3,
            "toeic_score_range": "600-780",
            "category": "辦公日常",
            "word_forms": [{"part_of_speech": "verb", "forms": ["abbreviate", "abbreviates"]}],
            "examples": [
                {"english": "We often abbreviate company names.", "chinese": "我們經常縮寫公司名稱。"},
                {"english": "The team will abbreviate the report.", "chinese": "團隊將簡化報告。"}
            ],
            "exam_tips": [
                "常見搭配詞：'be abbreviated to' (縮寫成)",
                "注意衍生字 abbreviation (名詞)"
            ]
        }
        result = transformer.transform_entry(single_word_item)
        self.assertIsNotNone(result)
        self.assertEqual(result.english_word, "abbreviate")
        self.assertEqual(result.chinese_definition, "縮寫；簡略化")
        self.assertEqual(result.parts_of_speech, "verb")
        self.assertEqual(result.star_rating, 3)
        self.assertEqual(result.toeic_score_range, "600-780")
        self.assertEqual(result.category, "辦公日常")
        self.assertEqual(result.example_en, "We often abbreviate company names.")
        self.assertEqual(result.example_zh, "我們經常縮寫公司名稱。")
        self.assertIn("【詞性變化】", result.exam_tips)
        self.assertIn("【詞性變化】", result.word_forms)


if __name__ == "__main__":
    unittest.main()
