import pandas as pd
import numpy as np

def analyze_market(df):
    if df.empty:
        return df

    df = df.copy()

    df["return_pct"] = ((df["ltp"] - df["open"]) / df["open"]) * 100
    df["turnover_m"] = df["turnover"] / 1000000
    df["turnover_m"] = df["turnover_m"].replace(0, 0.0001)

    df["amihud"] = abs(df["return_pct"]) / df["turnover_m"]

    high_turn = df["turnover"].quantile(0.8)
    low_amihud = df["amihud"].quantile(0.3)
    high_amihud = df["amihud"].quantile(0.8)

    df["cluster_name"] = "Retail"
    df.loc[df["amihud"] >= high_amihud, "cluster_name"] = "Speculative"
    df.loc[
        (df["turnover"] >= high_turn) &
        (df["amihud"] <= low_amihud),
        "cluster_name"
    ] = "Institutional"

    return df
