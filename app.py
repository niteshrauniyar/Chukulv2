import streamlit as st
from data_fetcher import ChukulFetcher
from analysis import analyze_market
from signals import generate_signals

st.set_page_config(page_title="NEPSE Quant", layout="wide")

st.title("🚀 NEPSE Institutional Quant Dashboard")

fetcher = ChukulFetcher()

# ALWAYS SHOW UI FIRST
placeholder = st.empty()
placeholder.info("Fetching market data...")

df = fetcher.fetch()

if df is None or df.empty:
    placeholder.error("API unavailable. Showing empty dashboard.")
    df = None
else:
    placeholder.success("Data loaded successfully")

df = analyze_market(df)
df = generate_signals(df)

col1, col2, col3 = st.columns(3)

if df is not None and not df.empty:
    col1.metric("BUY", len(df[df["Signal"] == "STRONG BUY"]))
    col2.metric("SELL", len(df[df["Signal"] == "EXIT"]))
    col3.metric("INST", len(df[df["cluster_name"] == "Institutional"]))

    st.subheader("Signals")
    st.dataframe(df[df["Signal"].isin(["STRONG BUY", "EXIT"])], use_container_width=True)

    st.subheader("Full Data")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data to display")
