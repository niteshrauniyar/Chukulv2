# =========================
# data_fetcher.py
# =========================
import requests
import pandas as pd
import numpy as np

class ChukulFetcher:
    def __init__(self):
        self.url = "https://chukul.com/api/market-data/today-price"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
            "Referer": "https://chukul.com/nepse-charts"
        }

    def to_float(self, x):
        try:
            return float(str(x).replace(",", "").strip())
        except:
            return 0.0

    def fetch(self):
        try:
            r = requests.get(self.url, headers=self.headers, timeout=10)
            r.raise_for_status()
            js = r.json()

            rows = []
            for item in js:
                rows.append({
                    "symbol": item.get("symbol", ""),
                    "ltp": self.to_float(item.get("ltp", 0)),
                    "open": self.to_float(item.get("open", 0)),
                    "volume": self.to_float(item.get("vol", 0)),
                    "turnover": self.to_float(item.get("turnover", 0)),
                })

            df = pd.DataFrame(rows)

            # pre cleaning
            df = df[(df["ltp"] > 0) & (df["volume"] > 0)].copy()

            return df

        except Exception as e:
            return pd.DataFrame()
