# =========================
# analysis.py
# =========================
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def analyze_market(df):
    if df.empty:
        return df

    df = df.copy()

    # Return %
    df["return_pct"] = ((df["ltp"] - df["open"]) / df["open"]) * 100

    # Turnover million
    df["turnover_m"] = df["turnover"] / 1_000_000

    # Avoid divide by zero
    df["turnover_m"] = df["turnover_m"].replace(0, 0.0001)

    # Amihud Ratio
    df["amihud"] = abs(df["return_pct"]) / df["turnover_m"]

    # High turnover threshold
    turnover_cut = df["turnover"].quantile(0.80)

    # Low amihud threshold
    amihud_cut = df["amihud"].quantile(0.30)

    df["institutional_flag"] = np.where(
        (df["turnover"] >= turnover_cut) &
        (df["amihud"] <= amihud_cut), 1, 0
    )

    # KMeans clustering
    features = df[["turnover", "volume", "amihud"]].fillna(0)

    km = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["cluster"] = km.fit_predict(features)

    centers = pd.DataFrame(km.cluster_centers_, columns=["turnover","volume","amihud"])

    high_turn = centers["turnover"].idxmax()
    high_amihud = centers["amihud"].idxmax()

    labels = {}
    for i in range(3):
        if i == high_turn:
            labels[i] = "Institutional"
        elif i == high_amihud:
            labels[i] = "Speculative"
        else:
            labels[i] = "Retail"

    df["cluster_name"] = df["cluster"].map(labels)

    return df
