"""
模組名稱：models.py
模組說明：定義 TOEIC 單字資料的資料結構模型（Data Transfer Object）
"""

from dataclasses import dataclass


@dataclass
class VocabItem:
    """
    單一單字項目的結構化資料物件

    屬性說明：
        english_word (str): 英文單字（必須為單一單字，不可為片語）
        chinese_definition (str): 繁體中文釋義
        parts_of_speech (str): 詞性（以逗號分隔之字串，例如：verb, noun）
        star_rating (int): 星級評分（1~5）
        toeic_score_range (str): 多益分數目標區間（例如：600-780）
        category (str): 商務或生活情境類別
        word_forms (str): 詞性變化與衍生字說明（標註為【詞性變化】）
        collocations (str): 簡化後的搭配詞（最多兩組，直接中英對照）
        example_en (str): 第一句英文例句
        example_zh (str): 第一句中文例句
        exam_tips (str): 考點與技巧精華（替換衍生字為【詞性變化】）
    """
    english_word: str
    chinese_definition: str
    parts_of_speech: str
    star_rating: int
    toeic_score_range: str
    category: str
    word_forms: str
    collocations: str
    example_en: str
    example_zh: str
    exam_tips: str
