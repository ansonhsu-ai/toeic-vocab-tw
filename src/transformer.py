"""
模組名稱：transformer.py
模組說明：負責將原始 JSON 資料轉換為符合雙欄閃卡規範的 VocabCardItem 模型列表
遵循原則：Open-Closed Principle (OCP), Single Responsibility Principle (SRP)
"""

from typing import Any, Dict, List, Optional
from src.cleaner import VocabCleaner
from src.models import VocabCardItem


class VocabTransformer:
    """
    單字庫資料轉換器，負責執行單字長度過濾與閃卡排版轉換
    """

    def __init__(self, cleaner: Optional[VocabCleaner] = None):
        """
        初始化轉換器

        參數：
            cleaner (VocabCleaner, optional): 清理處理器實例
        """
        self.cleaner = cleaner or VocabCleaner()

    def transform_entry(self, item: Dict[str, Any]) -> Optional[VocabCardItem]:
        """
        轉換單筆原始資料為雙欄閃卡項目，若單字長度超過一個字則過濾移除

        參數：
            item (Dict[str, Any]): 原始單字字典

        回傳：
            Optional[VocabCardItem]: 符合規範之雙欄閃卡模型物件，若應過濾則回傳 None
        """
        raw_word = item.get("english_word", "")
        # 規則: 第一欄長度超過一個字的資料整列移除
        if not self.cleaner.is_single_word(raw_word):
            return None

        clean_word = raw_word.strip()
        card_content = self.cleaner.format_card_content(item)

        return VocabCardItem(
            word=clean_word,
            content=card_content,
        )

    def transform_all(self, raw_items: List[Dict[str, Any]]) -> List[VocabCardItem]:
        """
        批次轉換所有原始資料項目並過濾

        參數：
            raw_items (List[Dict[str, Any]]): 原始資料清單

        回傳：
            List[VocabCardItem]: 清洗並轉換後的雙欄閃卡單字清單
        """
        results: List[VocabCardItem] = []
        for item in raw_items:
            transformed = self.transform_entry(item)
            if transformed is not None:
                results.append(transformed)
        return results
