
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="AI 投資助手", layout="wide")

st.title("📈 AI 投資助手 - K棒圖 + EMA10/20 + RSI + MACD + 成交量")

symbol = st.selectbox("選擇幣種", ["BTC-USD", "ETH-USD"])
days = st.selectbox("查詢天數", list(range(1, 31)))

try:
    df = yf.download(symbol, period=f"{days}d", interval="1h")
    df = df.dropna()
    df["EMA10"] = df["Close"].ewm(span=10, adjust=False).mean()
    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    df["MACD"] = df["Close"].ewm(span=12, adjust=False).mean() - df["Close"].ewm(span=26, adjust=False).mean()
except Exception as e:
    st.error(f"資料讀取錯誤：{e}")
    st.stop()

fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index,
                open=df["Open"], high=df["High"],
                low=df["Low"], close=df["Close"], name="K棒"))
fig.add_trace(go.Scatter(x=df.index, y=df["EMA10"], mode="lines", name="EMA10"))
fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], mode="lines", name="EMA20"))
st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 RSI + MACD 指標")
st.line_chart(df[["RSI", "MACD"]])

if "RSI" in df.columns and len(df) > 0:
    rsi_latest = df["RSI"].iloc[-1]
    macd_latest = df["MACD"].iloc[-1]
    signal = "看漲" if rsi_latest > 50 and macd_latest > 0 else "看跌"
    msg = f"{symbol}，最新 RSI 為 {rsi_latest:.2f}，MACD 為 {macd_latest:.2f}，綜合判斷：{signal}"
    st.markdown(f'<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance("{msg}"));</script>', unsafe_allow_html=True)
    st.success(msg)
