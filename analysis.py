import pandas as pd
import numpy as np

def analyze_market(df):
    if df.empty:
        return df

    df = df.copy()

    # Return %
    df["return_pct"] = ((df["ltp"] - df["open"]) / df["open"]) * 100

    # Turnover in millions
    df["turnover_m"] = df["turnover"] / 1000000
    df["turnover_m"] = df["turnover_m"].replace(0, 0.0001)

    # Amihud Ratio
    df["amihud"] = abs(df["return_pct"]) / df["turnover_m"]

    # Rule-based clustering
    high_turn = df["turnover"].quantile(0.80)
    high_amihud = df["amihud"].quantile(0.80)
    low_amihud = df["amihud"].quantile(0.30)

    df["cluster_name"] = "Retail"

    df.loc[df["amihud"] >= high_amihud, "cluster_name"] = "Speculative"

    df.loc[
        (df["turnover"] >= high_turn) &
        (df["amihud"] <= low_amihud),
        "cluster_name"
    ] = "Institutional"

    return df
