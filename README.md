# TOEIC 單字庫雙欄閃卡格式轉換工具

自 Hugging Face 資料集 [`kknono668/toeic-vocab-tw`](https://huggingface.co/datasets/kknono668/toeic-vocab-tw) 擷取並轉換為雙欄閃卡（Anki / Excel 背誦專用）CSV 格式。

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

## 專案結構 (S.O.L.I.D)

- `src/models.py`：雙欄閃卡模型 `VocabCardItem`
- `src/downloader.py`：下載與快取模組 `DatasetDownloader`
- `src/cleaner.py`：雙欄排版與精簡萃取工具 `VocabCleaner`
- `src/transformer.py`：資料轉換與過濾核心 `VocabTransformer`
- `src/exporter.py`：雙欄 CSV 匯出模組 `CsvExporter`
- `main.py`：執行進入點
- `tests/`：單元測試套件
- `toeic_vocabulary.csv`：清洗轉換後之雙欄 CSV

## 執行方式

### 執行單元測試
```powershell
python -m unittest discover -s tests -v
```

### 執行資料轉換
```powershell
python main.py
```
