"""
模組名稱：models.py
模組說明：定義 TOEIC 單字資料的資料結構模型（Data Transfer Object）
遵循原則：Single Responsibility Principle (SRP)
"""

from dataclasses import dataclass


@dataclass
class VocabCardItem:
    """
    雙欄閃卡格式單字項目資料物件

    屬性說明：
        word (str): 第一欄，英文單字（單一單字）
        content (str): 第二欄，格式化後的完整內容（包含詞性釋義、詞性變化、搭配詞、例句）
    """
    word: str
    content: str
