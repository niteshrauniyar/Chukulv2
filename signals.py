import numpy as np

def generate_signals(df):
    if df is None or df.empty:
        return df

    df = df.copy()

    signals = []
    confidence = []
    advice = []
    target = []
    stop = []

    for _, r in df.iterrows():

        if r["cluster_name"] == "Institutional" and r["ltp"] > r["open"]:
            signals.append("STRONG BUY")
            confidence.append(88)
            advice.append("🔥 Smart Money Accumulation")
            target.append(round(r["ltp"] * 1.06, 2))
            stop.append(round(r["ltp"] * 0.96, 2))

        elif r["cluster_name"] == "Institutional" and r["ltp"] < r["open"]:
            signals.append("EXIT")
            confidence.append(82)
            advice.append("⚠ Distribution Detected")
            target.append(round(r["ltp"] * 0.97, 2))
            stop.append(round(r["ltp"] * 1.03, 2))

        else:
            signals.append("HOLD")
            confidence.append(55)
            advice.append("Neutral Flow")
            target.append(round(r["ltp"], 2))
            stop.append(round(r["ltp"] * 0.97, 2))

    df["Signal"] = signals
    df["Confidence"] = confidence
    df["Advice"] = advice
    df["Target"] = target
    df["StopLoss"] = stop

    return df
