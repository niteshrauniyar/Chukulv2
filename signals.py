# =========================
# signals.py
# =========================
import numpy as np

def generate_signals(df):
    if df.empty:
        return df

    df = df.copy()

    signal = []
    confidence = []
    advice = []
    target = []
    stop = []

    for _, row in df.iterrows():

        if row["cluster_name"] == "Institutional" and row["ltp"] > row["open"]:
            signal.append("STRONG BUY")
            confidence.append(88)
            advice.append(f"🔥 Smart Money absorbing supply. Target Rs {round(row['ltp']*1.06,2)}")
            target.append(round(row["ltp"] * 1.06,2))
            stop.append(round(row["ltp"] * 0.96,2))

        elif row["cluster_name"] == "Institutional" and row["ltp"] < row["open"]:
            signal.append("EXIT")
            confidence.append(82)
            advice.append("⚠ Institutional unloading detected.")
            target.append(round(row["ltp"] * 0.97,2))
            stop.append(round(row["ltp"] * 1.03,2))

        else:
            signal.append("HOLD")
            confidence.append(55)
            advice.append("Neutral activity.")
            target.append(round(row["ltp"],2))
            stop.append(round(row["ltp"] * 0.97,2))

    df["Signal"] = signal
    df["Confidence"] = confidence
    df["SimpleAdvice"] = advice
    df["Target"] = target
    df["StopLoss"] = stop

    return df
