"""
模組名稱：cleaner.py
模組說明：負責單字資料清理、過濾、詞性縮寫對照、衍生詞萃取、搭配詞簡化與閃卡格式排版
遵循原則：Single Responsibility Principle (SRP)
"""

import re
from typing import Any, Dict, List, Optional


class VocabCleaner:
    """
    提供 TOEIC 單字資料清理與雙欄閃卡排版工具類別
    """

    # 詞性中文與英文縮寫對應表
    POS_MAP = {
        "noun": "n.",
        "verb": "v.",
        "adjective": "adj.",
        "adverb": "adv.",
        "preposition": "prep.",
        "conjunction": "conj.",
        "pronoun": "pron.",
        "interjection": "interj.",
        "名詞": "n.",
        "動詞": "v.",
        "形容詞": "adj.",
        "副詞": "adv.",
        "介系詞": "prep.",
        "連接詞": "conj.",
        "代名詞": "pron.",
    }

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
        stripped = word.strip()
        tokens = stripped.split()
        return len(tokens) == 1

    @staticmethod
    def format_pos(pos_list: Any) -> str:
        """
        將詞性列表轉換為標準縮寫格式（例如：(n.) 或 (adj., adv.)）

        參數：
            pos_list (Any): 詞性字串列表或以逗號分隔之字串

        回傳：
            str: 格式化後的詞性括號字串，若無則回傳空字串
        """
        if not pos_list:
            return ""
        if isinstance(pos_list, str):
            items = [p.strip() for p in pos_list.split(",") if p.strip()]
        elif isinstance(pos_list, list):
            items = [str(p).strip() for p in pos_list if str(p).strip()]
        else:
            items = [str(pos_list).strip()]

        abbrs = [VocabCleaner.POS_MAP.get(p.lower(), p) for p in items]
        return f"({', '.join(abbrs)})"

    @staticmethod
    def clean_definition(defn: Optional[str]) -> str:
        """
        清理繁體中文釋義，去除長篇說明贅述並統一頓號分隔

        參數：
            defn (str): 原始中文釋義字串

        回傳：
            str: 精簡後之中文釋義
        """
        if not defn:
            return ""
        # 切除「，指...」、「；通常...」等冗長說明句
        cleaned = re.split(r"[，,；;]\s*(?:指|通常|表示|用以|用來|用作)", defn)[0]
        cleaned = cleaned.replace("；", "、").replace(";", "、")
        cleaned = re.sub(r"^[、\s]+|[。、\s]+$", "", cleaned)
        return cleaned

    @staticmethod
    def extract_derived_forms(
        tips: Optional[List[str]],
        word_forms: Optional[List[Dict[str, Any]]] = None,
        current_word: str = "",
    ) -> List[str]:
        """
        從考點提示 (exam_tips) 或詞形資料中擷取格式化的【詞性變化】清單
        格式範例：able (adj.) 有能力的、accidental (adj.) 偶然的、意外的

        參數：
            tips (List[str]): 考點提示列表
            word_forms (List[Dict], optional): 詞形變化字典列表
            current_word (str): 當前主單字

        回傳：
            List[str]: 格式化後的詞性變化字串列表（最多兩組）
        """
        derived_list: List[str] = []
        clean_tips = tips or []

        for tip in clean_tips:
            # Pattern A: 形容詞 'accidental' (意外的) 或 名詞 'achievement' (成就)
            matches_a = re.findall(
                r"(動詞|名詞|形容詞|副詞)\s*['\"「]([a-zA-Z\s\-]+)['\"」]\s*[\(（]([^()（）\n]+)[\)）]",
                tip,
            )
            for pos_zh, w, zh_meaning in matches_a:
                w_clean = w.strip()
                if w_clean.lower() != current_word.lower() and len(w_clean.split()) == 1:
                    pos_abbr = VocabCleaner.POS_MAP.get(pos_zh, "")
                    zh_clean = re.sub(r"^[，,、\s]+|[，,、\s]+$", "", zh_meaning.strip())
                    pos_part = f"({pos_abbr}) " if pos_abbr else ""
                    item = f"{w_clean} {pos_part}{zh_clean}".strip()
                    if item not in derived_list:
                        derived_list.append(item)

            # Pattern B: 'enable' (動詞，使...能夠) 或 'ability' (名詞，能力)
            matches_b = re.findall(
                r"['\"「]([a-zA-Z\s\-]+)['\"」]\s*[\(（](動詞|名詞|形容詞|副詞)[，,、\s]*([^()（）\n]*)[\)）]",
                tip,
            )
            for w, pos_str, zh_meaning in matches_b:
                w_clean = w.strip()
                if w_clean.lower() != current_word.lower() and len(w_clean.split()) == 1:
                    pos_abbr = VocabCleaner.POS_MAP.get(pos_str, pos_str)
                    if not pos_abbr.endswith("."):
                        pos_abbr += "."
                    zh_clean = re.sub(r"^[，,、\s]+|[，,、\s]+$", "", zh_meaning.strip())
                    pos_part = f"({pos_abbr}) " if pos_abbr else ""
                    item = f"{w_clean} {pos_part}{zh_clean}".strip()
                    if item not in derived_list:
                        derived_list.append(item)

        # 若 exam_tips 沒抓到，檢視 word_forms
        if not derived_list and word_forms:
            for wf in word_forms:
                pos = wf.get("part_of_speech", "")
                pos_abbr = VocabCleaner.POS_MAP.get(pos, pos)
                forms = wf.get("forms", [])
                for f in forms:
                    f_clean = f.strip()
                    # 排除常規三單/過去式/進行式後綴，擷取相異單字
                    if (
                        f_clean.lower() != current_word.lower()
                        and len(f_clean.split()) == 1
                        and not f_clean.endswith("ing")
                        and not f_clean.endswith("ed")
                        and not f_clean.endswith("s")
                    ):
                        pos_part = f"({pos_abbr}) " if pos_abbr else ""
                        item = f"{f_clean} {pos_part}".strip()
                        if item not in derived_list:
                            derived_list.append(item)

        return derived_list[:2]

    @staticmethod
    def extract_collocations_list(
        tips: Optional[List[str]],
        current_word: str = "",
    ) -> List[str]:
        """
        從考點提示中擷取最多兩組簡化的搭配詞列表
        格式範例：['academic ability 學術能力', "to the best of one's ability 竭盡所能"]

        參數：
            tips (List[str]): 考點提示列表
            current_word (str): 當前單字

        回傳：
            List[str]: 搭配詞字串列表
        """
        if not tips:
            return []

        collocations: List[str] = []
        target_tips = [t for t in tips if any(k in t for k in ["搭配", "片語", "用法", "結構", "固定"])]
        if not target_tips:
            target_tips = tips

        for tip in target_tips:
            # Pattern 1: 'phrase' (中文)
            matches1 = re.findall(
                r"['\"「]([a-zA-Z\s\+\-\/\']+?)['\"」]\s*[\(（]([^()（）\n]+?)[\)）]", tip
            )
            for en, zh in matches1:
                en_clean = re.sub(r"^[^\w]+|[^\w]+$", "", en.strip())
                zh_clean = re.sub(r"^[，,、\s]+|[，,、\s]+$", "", zh.strip())
                if len(en_clean) >= 3 and len(zh_clean) <= 20:
                    if not any(g in zh_clean for g in ["動詞", "名詞", "形容詞", "副詞", "原形動詞", "受詞"]):
                        item = f"{en_clean} {zh_clean}"
                        if item not in collocations:
                            collocations.append(item)

            # Pattern 2: english phrase (中文)
            matches2 = re.findall(
                r"([a-zA-Z][a-zA-Z\s\+\-\/\']{2,40}[a-zA-Z])\s*[\(（]([\u4e00-\u9fa5A-Za-z0-9\s、/]+?)[\)）]",
                tip,
            )
            for en, zh in matches2:
                en_clean = re.sub(r"^[^\w]+|[^\w]+$", "", en.strip())
                zh_clean = re.sub(r"^[，,、\s]+|[，,、\s]+$", "", zh.strip())
                if len(en_clean.split()) >= 2 and len(zh_clean) <= 20:
                    if not any(g in zh_clean for g in ["動詞", "名詞", "形容詞", "副詞"]):
                        item = f"{en_clean} {zh_clean}"
                        if item not in collocations:
                            collocations.append(item)

        return collocations[:2]

    @staticmethod
    def format_card_content(item: Dict[str, Any]) -> str:
        """
        將單字資料組合排版成符合圖示格式的第二欄完整多行字串

        參數：
            item (Dict[str, Any]): 原始單字字典資料

        回傳：
            str: 格式化後的多行文字內容
        """
        word = item.get("english_word", "").strip()
        pos_str = VocabCleaner.format_pos(item.get("parts_of_speech", []))
        definition = VocabCleaner.clean_definition(item.get("chinese_definition", ""))

        lines: List[str] = []

        # 1. 標題首行：word (pos.) 中文釋義
        if pos_str:
            lines.append(f"{word} {pos_str} {definition}")
        else:
            lines.append(f"{word} {definition}")

        # 2. 【詞性變化】區塊
        tips = item.get("exam_tips", [])
        word_forms = item.get("word_forms", [])
        derived = VocabCleaner.extract_derived_forms(tips, word_forms, word)
        if derived:
            lines.append("【詞性變化】")
            for d in derived:
                lines.append(d)

        # 3. 【搭配詞】區塊
        collocs = VocabCleaner.extract_collocations_list(tips, word)
        if collocs:
            lines.append("【搭配詞】")
            for c in collocs:
                lines.append(c)

        # 4. 【例句】區塊（單句）
        examples = item.get("examples", [])
        if examples and len(examples) > 0:
            first_ex = examples[0]
            en_ex = first_ex.get("english", "").strip()
            zh_ex = first_ex.get("chinese", "").strip()
            if en_ex:
                lines.append("【例句】")
                if zh_ex:
                    if not zh_ex.startswith("(") and not zh_ex.startswith("（"):
                        zh_formatted = f"({zh_ex})"
                    else:
                        zh_formatted = zh_ex
                    lines.append(f"{en_ex} {zh_formatted}")
                else:
                    lines.append(en_ex)

        return "\n".join(lines)
