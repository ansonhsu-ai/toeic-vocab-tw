"""
模組名稱：downloader.py
模組說明：負責從 Hugging Face 資料集下載或讀取原始 JSON 檔案
遵循原則：Single Responsibility Principle (SRP)
"""

import json
import os
import urllib.request
from typing import Any, List


class DatasetDownloader:
    """
    負責下載與載入 Hugging Face TOEIC 單字庫資料集之類別
    """

    DEFAULT_URL = "https://huggingface.co/datasets/kknono668/toeic-vocab-tw/resolve/main/toeic_vocabulary.json"

    def __init__(self, url: str = DEFAULT_URL, cache_path: str = "toeic_raw.json"):
        """
        初始化下載器

        參數：
            url (str): 資料集遠端下載網址
            cache_path (str): 本地暫存 JSON 檔案路徑
        """
        self.url = url
        self.cache_path = cache_path

    def fetch_data(self, force_download: bool = False) -> List[dict]:
        """
        取得原始單字庫資料，若本地已有快取則直接讀取

        參數：
            force_download (bool): 是否強制重新下載

        回傳：
            List[dict]: 原始單字清單字典列表
        """
        if force_download or not os.path.exists(self.cache_path):
            print(f"正在從 {self.url} 下載 TOEIC 單字庫...")
            urllib.request.urlretrieve(self.url, self.cache_path)
            print(f"下載完成，已儲存至 {self.cache_path}")
        else:
            print(f"偵測到本地快取檔案 {self.cache_path}，直接載入...")

        with open(self.cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data
