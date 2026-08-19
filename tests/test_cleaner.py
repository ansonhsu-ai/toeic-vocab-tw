"""
單元測試模組：test_cleaner.py
測試說明：測試 VocabCleaner 雙欄閃卡排版、詞性縮寫、衍生詞萃取與搭配詞簡化邏輯
"""

import unittest
from src.cleaner import VocabCleaner


class TestVocabCleaner(unittest.TestCase):
    """
    測試 VocabCleaner 清洗與排版類別
    """

    def test_is_single_word(self):
        """
        測試單字長度過濾規則
        """
        self.assertTrue(VocabCleaner.is_single_word("ability"))
        self.assertTrue(VocabCleaner.is_single_word("  accident  "))
        self.assertTrue(VocabCleaner.is_single_word("well-known"))

        self.assertFalse(VocabCleaner.is_single_word("A be followed by B"))
        self.assertFalse(VocabCleaner.is_single_word("arrive at"))
        self.assertFalse(VocabCleaner.is_single_word(""))
        self.assertFalse(VocabCleaner.is_single_word(None))

    def test_format_pos(self):
        """
        測試詞性縮寫轉換
        """
        self.assertEqual(VocabCleaner.format_pos(["noun"]), "(n.)")
        self.assertEqual(VocabCleaner.format_pos(["verb"]), "(v.)")
        self.assertEqual(VocabCleaner.format_pos(["adjective", "adverb"]), "(adj., adv.)")

    def test_clean_definition(self):
        """
        測試中文釋義精簡化
        """
        raw_def = "能力、才能，指完成某項任務或達到特定目標所需的技能或潛力。"
        self.assertEqual(VocabCleaner.clean_definition(raw_def), "能力、才能")

    def test_extract_derived_forms(self):
        """
        測試衍生詞萃取
        """
        tips = [
            "詞性轉變考點：形容詞 'accidental' (意外的) 與副詞 'accidentally' (不小心地)。"
        ]
        derived = VocabCleaner.extract_derived_forms(tips, current_word="accident")
        self.assertEqual(len(derived), 2)
        self.assertEqual(derived[0], "accidental (adj.) 意外的")
        self.assertEqual(derived[1], "accidentally (adv.) 不小心地")

    def test_extract_collocations_list(self):
        """
        測試搭配詞提取列表（最多兩組，直接中英對照）
        """
        tips = [
            "常見搭配詞：'car accident' (車禍) 與 'by accident' (偶然地) 及 'traffic accident' (車禍)。"
        ]
        collocs = VocabCleaner.extract_collocations_list(tips, "accident")
        self.assertEqual(len(collocs), 2)
        self.assertEqual(collocs[0], "car accident 車禍")
        self.assertEqual(collocs[1], "by accident 偶然地")

    def test_format_card_content(self):
        """
        測試排版整合輸出完整閃卡內容
        """
        sample_item = {
            "english_word": "achieve",
            "chinese_definition": "達成、實現",
            "parts_of_speech": ["verb"],
            "examples": [
                {
                    "english": "You can achieve anything if you work hard enough.",
                    "chinese": "如果你足夠努力，你可以實現任何事情。"
                }
            ],
            "exam_tips": [
                "常見搭配詞組：常用於 achieve a goal (達成目標)、achieve success (獲得成功)。",
                "注意名詞形式 'achievement' (名詞，成就/達成)"
            ]
        }
        content = VocabCleaner.format_card_content(sample_item)
        lines = content.split("\n")
        self.assertEqual(lines[0], "achieve (v.) 達成、實現")
        self.assertIn("【詞性變化】", content)
        self.assertIn("achievement (n.) 成就/達成", content)
        self.assertIn("【搭配詞】", content)
        self.assertIn("achieve a goal 達成目標", content)
        self.assertIn("achieve success 獲得成功", content)
        self.assertIn("【例句】", content)
        self.assertIn("You can achieve anything if you work hard enough. (如果你足夠努力，你可以實現任何事情。)", content)


if __name__ == "__main__":
    unittest.main()
