import requests
import pandas as pd

class ChukulFetcher:
    def __init__(self):
        self.url = "https://chukul.com/api/market-data/today-price"
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://chukul.com/nepse-charts"
        }

    def to_float(self, x):
        try:
            return float(str(x).replace(",", ""))
        except:
            return 0.0

    def fetch(self):
        try:
            r = requests.get(self.url, headers=self.headers, timeout=5)
            r.raise_for_status()

            data = r.json()

            rows = []
            for i in data:
                rows.append({
                    "symbol": i.get("symbol", ""),
                    "ltp": self.to_float(i.get("ltp", 0)),
                    "open": self.to_float(i.get("open", 0)),
                    "volume": self.to_float(i.get("vol", 0)),
                    "turnover": self.to_float(i.get("turnover", 0)),
                })

            df = pd.DataFrame(rows)

            if df.empty:
                return pd.DataFrame()

            df = df[(df["ltp"] > 0) & (df["volume"] > 0)]

            return df

        except Exception as e:
            print("API error:", e)
            return pd.DataFrame()
