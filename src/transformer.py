"""
模組名稱：transformer.py
模組說明：負責將原始 JSON 資料轉換為符合業務規範的 VocabItem 模型列表
遵循原則：Open-Closed Principle (OCP), Single Responsibility Principle (SRP)
"""

from typing import Any, Dict, List, Optional
from src.cleaner import VocabCleaner
from src.models import VocabItem


class VocabTransformer:
    """
    單字庫資料轉換器，負責執行資料清理、篩選與扁平化對應
    """

    def __init__(self, cleaner: Optional[VocabCleaner] = None):
        """
        初始化轉換器

        參數：
            cleaner (VocabCleaner, optional): 清理處理器實例
        """
        self.cleaner = cleaner or VocabCleaner()

    def transform_entry(self, item: Dict[str, Any]) -> Optional[VocabItem]:
        """
        轉換單筆原始資料，若不符合規則（例如單字長度超過一個字）則回傳 None

        參數：
            item (Dict[str, Any]): 原始單字字典

        回傳：
            Optional[VocabItem]: 符合規範之單字模型物件，若應過濾則回傳 None
        """
        raw_word = item.get("english_word", "")
        # 規則 1: 第一欄長度超過一個字的資料整列移除
        if not self.cleaner.is_single_word(raw_word):
            return None

        clean_word = raw_word.strip()
        chinese_def = item.get("chinese_definition", "").strip()

        # 詞性處理
        pos_list = item.get("parts_of_speech", [])
        parts_of_speech = ", ".join(pos_list) if isinstance(pos_list, list) else str(pos_list)

        star_rating = item.get("star_rating", 0)
        score_range = item.get("toeic_score_range", "")
        category = item.get("category", "")

        # 考點與提示處理（替換衍生字為【詞性變化】）
        raw_tips = item.get("exam_tips", [])
        cleaned_tips = [self.cleaner.rename_derived_words(t) for t in raw_tips] if raw_tips else []
        exam_tips_str = " \n".join(cleaned_tips)

        # 規則 2: 將[衍生字]改寫成【詞性變化】
        word_forms = self.cleaner.format_word_forms(item.get("word_forms", []), raw_tips)

        # 規則 3: 搭配詞簡化，最多保留兩組，直接翻譯
        collocations = self.cleaner.extract_collocations(raw_tips, clean_word)

        # 規則 4: 例句只留下一句
        example_en, example_zh = self.cleaner.extract_single_example(item.get("examples", []))

        return VocabItem(
            english_word=clean_word,
            chinese_definition=chinese_def,
            parts_of_speech=parts_of_speech,
            star_rating=star_rating,
            toeic_score_range=score_range,
            category=category,
            word_forms=word_forms,
            collocations=collocations,
            example_en=example_en,
            example_zh=example_zh,
            exam_tips=exam_tips_str,
        )

    def transform_all(self, raw_items: List[Dict[str, Any]]) -> List[VocabItem]:
        """
        批次轉換所有原始資料項目並過濾

        參數：
            raw_items (List[Dict[str, Any]]): 原始資料清單

        回傳：
            List[VocabItem]: 清洗並轉換後的單字清單
        """
        results: List[VocabItem] = []
        for item in raw_items:
            transformed = self.transform_entry(item)
            if transformed is not None:
                results.append(transformed)
        return results
