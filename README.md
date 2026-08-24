# TOEIC 單字集與 SRS 智能閃卡學習系統

本專案自 Hugging Face 資料集 [`kknono668/toeic-vocab-tw`](https://huggingface.co/datasets/kknono668/toeic-vocab-tw) 擷取 9,698 筆 TOEIC 單字庫，提供清洗轉換後的**雙欄閃卡 CSV** 以及**單一 HTML 檔案的 SRS (Spaced Repetition System) 智能單字卡 App**。

---

## 快速開始

直接使用任何現代瀏覽器開啟 `index.html` 即可立即開始背單字，無須架設後端伺服器。

```powershell
# 在瀏覽器中開啟
Start-Process .\index.html
```

---

## 核心功能與使用說明

### 1. 每日學習 Session 與多元隨機抽樣
- **10 字一組**：每次學習以 10 個單字為一組（Session），輕量無負擔。
- **多元字母分散抽樣（Diverse Multi-Letter Sampling）**：系統會自動自 A~Z 不同開頭字母中各隨機抽選單字，避免單字集中在同一字母。
- **掌握單字避讓**：已標記為 `Easy (簡單)` 的熟練單字會自動移出抽樣池，優先練習未掌握的單字。

### 2. 每日打卡與連續學習紀錄（Streak）
- **打卡機制**：每天只要完成 1 組 10 字 Session，系統便會自動完成當日打卡。
- **連續天數統計**：右上角即時顯示連續打卡天數（🔥 Streak），點擊可開啟打卡紀錄面板查看歷史紀錄與已掌握單字總數。

### 3. 語音朗讀（Web Speech API）
- 採用瀏覽器原生 `en-US` 語音合成引擎。
- **正面**：朗讀目標英文單字。
- **背面**：只朗讀英文例句。
- 翻面或切換卡片時會自動朗讀，亦可按 `Enter` 隨時重播。

### 4. 🗣️ AI 語音對話提示詞（ChatGPT / Gemini 連動）
- **例句對話按鈕**：翻至卡片背面時，【例句】區塊右上角設有 `[🗣️ AI 對話]` 按鈕（或按快捷鍵 `D`）。
- **自動複製與原生分享**：
  - 點擊後會自動將專屬提示詞（Prompt）複製到剪貼簿。
  - 手機瀏覽時將自動喚起系統原生分享面板，可直接傳送給 ChatGPT / Gemini App。
  - 桌面端會彈出提示詞視窗，並附有 ChatGPT / Gemini 網頁版快速跳轉連結。
- **提示詞特色**：AI 扮演友善朋友，圍繞例句情境逐一提問 3 個口語問題，每次回覆精簡在 1~2 句話，專門為實時語音對話優化。

### 5. SRS 間隔重複 4 鍵操作規則
| 按鍵 / 快捷鍵 | 名稱 | 佇列排程邏輯 | 說明 |
| :---: | :---: | :--- | :--- |
| **`1`** | **Again** | 插入佇列第 2 位 | 完全不熟，馬上再次複習 |
| **`2`** | **Hard** | 插入佇列中央位置 | 稍微生疏，過幾張後再測一次 |
| **`3`** | **Known** | 插入佇列最尾端 | 已理解，本組複習完畢再確認一次 |
| **`4`** | **Easy** | 直接移出佇列 | 完全掌握，本次不再出現並記錄為已熟練 |

### 6. CSV 匯入與拖曳支援 (Drag & Drop)
- 支援上傳自訂雙欄 CSV 檔案，可直接將檔案拖曳至網頁任意處完成匯入。
- 第 1 欄為卡片正面（單字），第 2 欄為卡片背面內容。

---

## 鍵盤快捷鍵一覽

| 快捷鍵 | 功能說明 |
| :---: | :--- |
| <kbd>Space</kbd> | 翻轉字卡（正面 / 背面） |
| <kbd>Enter</kbd> | 重播當前畫面語音（單字 / 例句） |
| <kbd>D</kbd> | 生成並分享例句 **AI 語音對話提示詞** |
| <kbd>1</kbd> | 選擇 **Again**（重來） |
| <kbd>2</kbd> | 選擇 **Hard**（困難） |
| <kbd>3</kbd> | 選擇 **Known**（已掌握） |
| <kbd>4</kbd> | 選擇 **Easy**（簡單） |

---

## 雙欄 CSV 格式規範

- **第一欄**：英文單字（單一單字，共 9,698 筆）。
- **第二欄**：格式化後的完整排版內容（包含多行換行）：
  ```text
  {單字} ({詞性縮寫}) {中文釋義}
  【詞性變化】
  {相關詞性衍生字} ({詞性}) {中文}
  【搭配詞】
  {搭配詞1英文} {搭配詞1中文}
  {搭配詞2英文} {搭配詞2中文}
  【例句】
  {英文例句} ({中文例句})
  ```
- **編碼格式**：UTF-8 with BOM (`utf-8-sig`)。

---

## 專案架構與開發

本專案遵循 **S.O.L.I.D** 設計原則與模組化架構：

```text
├── build_app.py               # 建置腳本：將 9,698 筆單字庫與 template.html 打包為單一 index.html
├── index.html                 # 最終發布之單一獨立 HTML App
├── template.html              # Flashcard 前端模板（包含 CSS、UI 與 JavaScript 服務層）
├── toeic_vocabulary.csv       # 清洗完成之 9,698 筆雙欄單字庫
├── main.py                    # 資料下載與 CSV 轉換進入點
├── src/                       # 後端資料處理核心模組
│   ├── models.py              # 雙欄閃卡資料模型
│   ├── downloader.py          # Hugging Face 資料集下載模組
│   ├── cleaner.py             # 內容清洗與詞性、例句簡化萃取
│   ├── transformer.py         # 資料轉換與過濾核心
│   └── exporter.py            # CSV 匯出模組
└── tests/                     # 測試套件
    ├── test_dialogue_prompt.js# AI 語音對話提示詞生成單元測試
    ├── test_session_checkin.js# 多字母抽樣與打卡 Streak 單元測試
    ├── test_srs_logic.js      # SRS 佇列操作單元測試
    ├── test_e2e.js            # 瀏覽器端到端 (E2E) 渲染測試
    ├── test_cleaner.py        # Python 清洗邏輯測試
    ├── test_transformer.py    # Python 轉換邏輯測試
    └── test_exporter.py       # Python 匯出邏輯測試
```

---

## 測試與建置指令

### 執行全套前端與演算法測試
```powershell
node tests/test_dialogue_prompt.js
node tests/test_session_checkin.js
node tests/test_srs_logic.js
node tests/test_e2e.js
```

### 執行後端資料清洗單元測試
```powershell
python -m unittest discover -s tests -v
```

### 重新打包生成 index.html
```powershell
python build_app.py
```
