"""
模組名稱：cleaner.py
模組說明：負責單字資料清理、過濾、欄位文字替換與簡化提取邏輯
遵循原則：Single Responsibility Principle (SRP)
"""

import re
from typing import Any, Dict, List, Optional, Tuple


class VocabCleaner:
    """
    提供 TOEIC 單字資料清理與字串精簡處理工具類別
    """

    @staticmethod
    def is_single_word(word: Optional[str]) -> bool:
        """
        檢查英文單字是否為單一單字（過濾包含空格、片語或多詞項目）

        參數：
            word (str): 待檢查的英文單字字串

        回傳：
            bool: 若為單一字詞回傳 True，若包含空格或為空則回傳 False
        """
        if not word:
            return False
        # 去除前後空白後，以空白分割檢驗字數
        stripped = word.strip()
        tokens = stripped.split()
        return len(tokens) == 1

    @staticmethod
    def rename_derived_words(text: Optional[str]) -> str:
        """
        將文字中所有「衍生字」或「衍生詞」改寫為「【詞性變化】」

        參數：
            text (str): 原始文字

        回傳：
            str: 替換標籤後的文字
        """
        if not text:
            return ""
        # 替換衍生字、衍生詞以及包含引號或括號形式
        modified = re.sub(r'\[\s*衍生字\s*\]|【\s*衍生字\s*】|衍生字|衍生詞', '【詞性變化】', text)
        return modified

    @staticmethod
    def format_word_forms(word_forms: Optional[List[Dict[str, Any]]], tips: Optional[List[str]] = None) -> str:
        """
        將原始詞形與衍生字資訊格式化為【詞性變化】文字

        參數：
            word_forms (List[Dict]): 原始詞形列表（包含 part_of_speech 與 forms）
            tips (List[str], optional): 考點提示列表，用以擷取衍生字說明

        回傳：
            str: 格式化後之【詞性變化】字串
        """
        entries = []
        if word_forms:
            for item in word_forms:
                pos = item.get("part_of_speech", "")
                forms = item.get("forms", [])
                if forms:
                    unique_forms = []
                    for f in forms:
                        if f not in unique_forms:
                            unique_forms.append(f)
                    forms_str = ", ".join(unique_forms)
                    if pos:
                        entries.append(f"{pos}: {forms_str}")
                    else:
                        entries.append(forms_str)

        # 檢索 exam_tips 中關於衍生字的補充
        derived_tips = []
        if tips:
            for tip in tips:
                if "衍生" in tip or "詞性轉變" in tip or "詞性變化" in tip or "變化考點" in tip:
                    cleaned_tip = VocabCleaner.rename_derived_words(tip)
                    derived_tips.append(cleaned_tip)

        result_parts = []
        if entries:
            result_parts.append("; ".join(entries))
        if derived_tips:
            result_parts.append(" | ".join(derived_tips))

        return " \n".join(result_parts) if result_parts else ""

    @staticmethod
    def extract_collocations(tips: Optional[List[str]], word: str = "") -> str:
        """
        從考點提示 (exam_tips) 中擷取最多兩組簡化的搭配詞 (英文 中文)，去除冗長說明

        範例：
            arrive at the airport 到達機場; arrive in London 到達倫敦

        參數：
            tips (List[str]): 考點提示列表
            word (str): 當前單字

        回傳：
            str: 最多兩組搭配詞，以分號分隔
        """
        if not tips:
            return ""

        raw_candidates: List[Tuple[str, str]] = []

        # 優先搜尋包含搭配詞關鍵字的句子
        target_tips = [t for t in tips if any(k in t for k in ["搭配", "片語", "用法", "結構", "固定"])]
        if not target_tips:
            target_tips = tips

        for tip in target_tips:
            # Pattern 1: 'phrase' (中文) 或 "phrase" (中文) 或 「phrase」 (中文)
            matches1 = re.findall(
                r"['\"「]([a-zA-Z\s\+\-\/\']+?)['\"」]\s*[\(（]([^()（）\n]+?)[\)）]", tip
            )
            for en, zh in matches1:
                raw_candidates.append((en.strip(), zh.strip()))

            # Pattern 2: english phrase (中文)
            # 例如: abandon a project (放棄專案)
            matches2 = re.findall(
                r"([a-zA-Z][a-zA-Z\s\+\-\/\']{2,45}[a-zA-Z])\s*[\(（]([\u4e00-\u9fa5A-Za-z0-9\s、/]+?)[\)）]",
                tip,
            )
            for en, zh in matches2:
                raw_candidates.append((en.strip(), zh.strip()))

            # Pattern 3: 「phrase」意為「中文」 或 「phrase」表示「中文」
            matches3 = re.findall(
                r"[「『]([a-zA-Z\s\+\-]+?)[」』][^「『\n]{0,10}[「『]([\u4e00-\u9fa5\s]+?)[」』]",
                tip,
            )
            for en, zh in matches3:
                raw_candidates.append((en.strip(), zh.strip()))

        # 清理並過濾搭配詞
        cleaned_collocations: List[str] = []
        seen = set()

        for en_text, zh_text in raw_candidates:
            # 去除首尾標點與符號
            en_clean = re.sub(r"^[^\w]+|[^\w]+$", "", en_text.strip())
            zh_clean = re.sub(r"^[，,、\s]+|[，,、\s]+$", "", zh_text.strip())

            # 排除非實質搭配（例如純詞性標註或單字母）
            if not en_clean or not zh_clean:
                continue
            if len(en_clean) < 3 or len(zh_clean) > 25:
                continue

            # 排除純文法說明字眼
            grammar_stopwords = ["動詞", "名詞", "形容詞", "副詞", "原形動詞", "受詞", "主詞", "句型", "to-infinitive"]
            if zh_clean in grammar_stopwords or all(g in zh_clean for g in ["詞"]):
                continue

            item = f"{en_clean} {zh_clean}"
            if item not in seen:
                seen.add(item)
                cleaned_collocations.append(item)
            if len(cleaned_collocations) == 2:
                break

        return "; ".join(cleaned_collocations)

    @staticmethod
    def extract_single_example(examples: Optional[List[Dict[str, str]]]) -> Tuple[str, str]:
        """
        從例句清單中擷取第一句英文例句與對應中文翻譯

        參數：
            examples (List[Dict]): 原始例句列表（每筆含 english 與 chinese 鍵值）

        回傳：
            Tuple[str, str]: (英文例句, 中文例句)，若無則回傳 ("", "")
        """
        if not examples or len(examples) == 0:
            return ("", "")

        first_ex = examples[0]
        en_text = first_ex.get("english", "").strip() if isinstance(first_ex, dict) else ""
        zh_text = first_ex.get("chinese", "").strip() if isinstance(first_ex, dict) else ""
        return (en_text, zh_text)
