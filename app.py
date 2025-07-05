import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def calculate_rsi(data, period=14):
    delta = data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data, fast=12, slow=26, signal=9):
    ema_fast = data["Close"].ewm(span=fast, adjust=False).mean()
    ema_slow = data["Close"].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

st.set_page_config(page_title="AI 投資助手", layout="wide")
st.title("📈 AI 投資助手 - K棒圖 + EMA10/20 + RSI + MACD + 成交量")

symbol_map = {
    "比特幣 BTC": "BTC-USD",
    "以太幣 ETH": "ETH-USD",
    "蘋果 AAPL": "AAPL",
    "台積電 2330.TW": "2330.TW"
}

symbol_display = st.selectbox("選擇幣種", list(symbol_map.keys()))
symbol = symbol_map[symbol_display]

days = st.selectbox("查詢天數", [1, 3, 5, 7, 14, 30], index=1)

try:
    df = yf.download(symbol, period=f"{days}d", interval="1h")
    df = df.dropna()

    df["EMA10"] = df["Close"].ewm(span=10).mean()
    df["EMA20"] = df["Close"].ewm(span=20).mean()
    df["RSI"] = calculate_rsi(df)
    df["MACD"], df["Signal"], df["Histogram"] = calculate_macd(df)

    fig = go.Figure()

    fig.add_trace(go.Candlestick(x=df.index, open=df["Open"], high=df["High"],
                                 low=df["Low"], close=df["Close"], name="K棒"))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA10"], line=dict(color="blue"), name="EMA10"))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], line=dict(color="purple"), name="EMA20"))

    fig.update_layout(title=f"{symbol_display} K棒圖", xaxis_title="時間", yaxis_title="價格")

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 RSI + MACD 指標")

    st.line_chart(df[["RSI"]])
    st.line_chart(df[["MACD", "Signal", "Histogram"]])

except Exception as e:
    st.error(f"發生錯誤：{e}")
