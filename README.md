# TOEIC 單字庫處理與清洗工具

自 Hugging Face 資料集 [`kknono668/toeic-vocab-tw`](https://huggingface.co/datasets/kknono668/toeic-vocab-tw) 擷取並轉換為繁體中文 CSV 格式的自動化工具。

## 資料過濾與轉換規則

1. **單字篩選**：第一欄（單字欄）長度超過一個字（包含空格的片語/複合詞）整列移除，僅保留單一英文單字（共 9,698 筆）。
2. **詞性變化改寫**：將所有「衍生字」改寫標註為「【詞性變化】」。
3. **搭配詞簡化**：最多保留 2 組搭配詞，僅保留直接中英對照翻譯，去除冗長註解。
4. **例句精簡**：僅保留 1 句英文例句與對應繁體中文翻譯。
5. **編碼規格**：採用 UTF-8 with BOM (`utf-8-sig`) 編碼，確保在 Excel 與各大平台開啟時不亂碼。

## 專案結構 (S.O.L.I.D)

- `src/models.py`：資料模型 `VocabItem`
- `src/downloader.py`：下載與快取模組 `DatasetDownloader`
- `src/cleaner.py`：字串清洗與精簡萃取工具 `VocabCleaner`
- `src/transformer.py`：資料轉換與過濾核心 `VocabTransformer`
- `src/exporter.py`：CSV 匯出模組 `CsvExporter`
- `main.py`：執行進入點
- `tests/`：單元測試套件
- `toeic_vocabulary.csv`：清洗轉換後之完整 CSV 單字庫

## 執行方式

### 執行單元測試
```powershell
python -m unittest discover -s tests -v
```

### 執行資料下載與轉換
```powershell
python main.py
```
