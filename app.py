import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pandas_ta as ta

st.set_page_config(page_title="AI 投資助手", layout="wide")
st.title("✅ AI 投資助手 - K棒圖 + EMA10/20 + RSI + MACD + 成交量")

symbol = st.selectbox("選擇幣種", ["BTC", "ETH", "BNB"], index=0)
days = st.selectbox("查詢天數", [1, 3, 7, 14, 30], index=2)

# 模擬資料錯誤處理邏輯
try:
    st.info(f"讀取 {symbol} 最近 {days} 天資料...（此版本為展示用途）")
    df = pd.DataFrame()
    df["Close"] = pd.Series([1, 2, 3, 4, 5])
    df["EMA10"] = df["Close"].ewm(span=10).mean()
    df["EMA20"] = df["Close"].ewm(span=20).mean()
    df["RSI"] = ta.rsi(df["Close"])
    df["MACD"] = ta.macd(df["Close"])["MACD_12_26_9"]

    st.success("技術指標計算完成 ✅")
except Exception as e:
    st.error(f"讀取錯誤：{e}")