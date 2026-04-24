import streamlit as st
import pandas as pd
from data_fetcher import ChukulFetcher
from analysis import analyze_market
from signals import generate_signals

st.set_page_config(page_title="NEPSE Quant", layout="wide")

st.title("🚀 NEPSE Institutional Quant")

try:
    fetcher = ChukulFetcher()
    df = fetcher.fetch()

    if df is None or df.empty:
        st.warning("No market data available.")
        st.stop()

    required = ["symbol", "ltp", "open", "volume", "turnover"]

    for col in required:
        if col not in df.columns:
            df[col] = 0

    df = analyze_market(df)
    df = generate_signals(df)

    st.success("Data Loaded Successfully")

    col1, col2, col3 = st.columns(3)

    buy_count = len(df[df["Signal"] == "STRONG BUY"]) if "Signal" in df.columns else 0
    sell_count = len(df[df["Signal"] == "EXIT"]) if "Signal" in df.columns else 0
    inst_count = len(df[df["cluster_name"] == "Institutional"]) if "cluster_name" in df.columns else 0

    col1.metric("BUY", buy_count)
    col2.metric("SELL", sell_count)
    col3.metric("Institutional", inst_count)

    st.subheader("Signals")

    if "Signal" in df.columns:
        sig = df[df["Signal"].isin(["STRONG BUY", "EXIT"])]
        st.dataframe(sig, use_container_width=True)

    st.subheader("Full Data")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("App crashed.")
    st.code(str(e))
