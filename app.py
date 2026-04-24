import streamlit as st
from data_fetcher import ChukulFetcher
from analysis import analyze_market
from signals import generate_signals

st.set_page_config(page_title="NEPSE Quant", layout="wide")

st.title("🚀 NEPSE Institutional Quant")

# ALWAYS SHOW SOMETHING FIRST (prevents "infinite loading")
status = st.empty()
status.info("App started... loading data")

fetcher = ChukulFetcher()

try:
    df = fetcher.fetch()
except:
    df = None

if df is None or df.empty:
    status.error("⚠ Data not available (API issue)")
    df = None
else:
    status.success("Data loaded")

# SAFE PIPELINE
df = analyze_market(df)
df = generate_signals(df)

col1, col2, col3 = st.columns(3)

if df is not None and not df.empty:
    col1.metric("BUY", len(df[df["Signal"] == "STRONG BUY"]))
    col2.metric("SELL", len(df[df["Signal"] == "EXIT"]))
    col3.metric("INST", len(df[df["cluster_name"] == "Institutional"]))

    st.subheader("Signals")
    st.dataframe(df[df["Signal"].isin(["STRONG BUY", "EXIT"])])

    st.subheader("Full Data")
    st.dataframe(df)

else:
    st.warning("No data available right now. App is still working.")
