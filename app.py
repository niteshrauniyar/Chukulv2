import streamlit as st
from data_fetcher import ChukulFetcher
from analysis import analyze_market
from signals import generate_signals

st.set_page_config(page_title="NEPSE Quant", layout="wide")

st.title("🚀 NEPSE Institutional Quant Dashboard")

fetcher = ChukulFetcher()
df = fetcher.fetch()

if df is None or df.empty:
    st.warning("No data available from API")
    st.stop()

df = analyze_market(df)
df = generate_signals(df)

st.success("Data Loaded")

col1, col2, col3 = st.columns(3)

col1.metric("BUY", len(df[df["Signal"] == "STRONG BUY"]))
col2.metric("SELL", len(df[df["Signal"] == "EXIT"]))
col3.metric("INST", len(df[df["cluster_name"] == "Institutional"]))

st.subheader("Signals")

st.dataframe(
    df[df["Signal"].isin(["STRONG BUY", "EXIT"])],
    use_container_width=True
)

st.subheader("Full Data")

st.dataframe(df, use_container_width=True)
