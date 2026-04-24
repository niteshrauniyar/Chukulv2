import requests
import pandas as pd

class ChukulFetcher:
    def __init__(self):
        self.url = "https://chukul.com/api/market-data/today-price"
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://chukul.com/nepse-charts"
        }

    def fetch(self):
        try:
            r = requests.get(self.url, headers=self.headers, timeout=5)

            if r.status_code != 200:
                return pd.DataFrame()

            try:
                data = r.json()
            except:
                return pd.DataFrame()

            rows = []

            if isinstance(data, list):
                for i in data:
                    rows.append({
                        "symbol": i.get("symbol", ""),
                        "ltp": float(i.get("ltp", 0) or 0),
                        "open": float(i.get("open", 0) or 0),
                        "volume": float(i.get("vol", 0) or 0),
                        "turnover": float(i.get("turnover", 0) or 0),
                    })

            df = pd.DataFrame(rows)

            if df.empty:
                return df

            return df[(df["ltp"] > 0) & (df["volume"] > 0)]

        except:
            return pd.DataFrame()
