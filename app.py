# =========================
# app.py
# =========================
import streamlit as st
import pandas as pd
from data_fetcher import ChukulFetcher
from analysis import analyze_market
from signals import generate_signals

st.set_page_config(
    page_title="NEPSE Institutional Quant",
    layout="wide"
)

# session state safe init
if "loaded" not in st.session_state:
    st.session_state.loaded = True

# Dark Mode CSS
st.markdown("""
<style>
body {background:#0e1117;color:white;}
[data-testid="metric-container"]{
background:#111827;
padding:15px;
border-radius:12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 NEPSE Institutional Quant App")

st.latex(r'''
Amihud = \frac{|Return\%|}{Turnover\ in\ Millions}
''')

fetcher = ChukulFetcher()
df = fetcher.fetch()

if df.empty:
    st.warning("⚠ Unable to connect to Chukul API. Please try again later.")
    st.stop()

# Process
df = analyze_market(df)
df = generate_signals(df)

# Market Pulse
col1, col2, col3 = st.columns(3)

buy_count = len(df[df["Signal"] == "STRONG BUY"])
sell_count = len(df[df["Signal"] == "EXIT"])
inst_count = len(df[df["cluster_name"] == "Institutional"])

col1.metric("🔥 Buy Signals", buy_count)
col2.metric("⚠ Exit Signals", sell_count)
col3.metric("🏦 Institutional Stocks", inst_count)

st.divider()

# Signal Table
st.subheader("📈 Actionable Signals")

sig = df[df["Signal"].isin(["STRONG BUY", "EXIT"])]

show_cols = [
    "symbol","ltp","Signal","Confidence",
    "Target","StopLoss","SimpleAdvice"
]

available = [c for c in show_cols if c in sig.columns]

st.dataframe(
    sig[available].sort_values("Confidence", ascending=False),
    use_container_width=True
)

st.divider()

# Full Matrix
st.subheader("🧠 Full Quant Matrix")

def color_rows(row):
    if row["cluster_name"] == "Institutional":
        return ["background-color:#123524"] * len(row)
    return [""] * len(row)

st.dataframe(
    df.style.apply(color_rows, axis=1),
    use_container_width=True
)
