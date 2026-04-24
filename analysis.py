import pandas as pd
import numpy as np

def analyze_market(df):
    if df.empty:
        return df

    df = df.copy()

    # Return %
    df["return_pct"] = ((df["ltp"] - df["open"]) / df["open"]) * 100

    # Turnover million
    df["turnover_m"] = df["turnover"] / 1000000
    df["turnover_m"] = df["turnover_m"].replace(0, 0.0001)

    # Amihud Ratio
    df["amihud"] = abs(df["return_pct"]) / df["turnover_m"]

    # Quantile Rules instead of sklearn
    high_turn = df["turnover"].quantile(0.80)
    high_amihud = df["amihud"].quantile(0.80)
    low_amihud = df["amihud"].quantile(0.30)

    conditions = [
        (df["turnover"] >= high_turn) & (df["amihud"] <= low_amihud),
        (df["amihud"] >= high_amihud),
    ]

    labels = ["Institutional", "Speculative"]

    df["cluster_name"] = np.select(conditions, labels, default="Retail")

    return df
