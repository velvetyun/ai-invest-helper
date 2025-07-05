
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import numpy as np

# 技術指標：原生 EMA、RSI、MACD 實作
def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def rsi(close, period=14):
    delta = close.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    gain = pd.Series(gain).rolling(window=period).mean()
    loss = pd.Series(loss).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(close):
    exp1 = close.ewm(span=12, adjust=False).mean()
    exp2 = close.ewm(span=26, adjust=False).mean()
    macd_line = exp1 - exp2
    signal = macd_line.ewm(span=9, adjust=False).mean()
    return macd_line, signal

# 介面設計
st.set_page_config("AI 投資助手 - v2.3.6", layout="wide")
st.title("📊 AI 投資助手 - K棒圖 + EMA10/20 + RSI + MACD + 成交量")

symbol = st.selectbox("選擇幣種", ["BTC-USD", "ETH-USD", "2330.TW", "AAPL"], index=0)
days = st.selectbox("查詢天數", [1, 3, 5, 10, 30], index=2)

try:
    df = yf.download(symbol, period=f"{days}d", interval="1h")
    df = df.dropna()
    df["EMA10"] = ema(df["Close"], 10)
    df["EMA20"] = ema(df["Close"], 20)
    df["RSI"] = rsi(df["Close"])
    df["MACD"], df["MACD_signal"] = macd(df["Close"])

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df["Open"], high=df["High"],
                                 low=df["Low"], close=df["Close"], name="K棒"))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA10"], line=dict(color="blue"), name="EMA10"))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], line=dict(color="purple"), name="EMA20"))
    fig.update_layout(title=f"{symbol} K棒圖", height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 RSI / MACD 指標")
    st.line_chart(df[["RSI"]])
    st.line_chart(df[["MACD", "MACD_signal"]])

except Exception as e:
    st.error(f"資料讀取錯誤：{e}")
