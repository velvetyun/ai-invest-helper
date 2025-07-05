
import streamlit as st
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import yfinance as yf

st.title("AI 投資助手 - K棒圖 + EMA10/20 + RSI + MACD + 成交量")

symbol = st.selectbox("選擇幣種", ["比特幣 BTC", "以太幣 ETH"])
symbol_map = {"比特幣 BTC": "BTC-USD", "以太幣 ETH": "ETH-USD"}
days = st.selectbox("查詢天數", [1, 3, 7, 14, 30], index=2)

ticker = symbol_map[symbol]
df = yf.download(ticker, period=f"{days}d", interval="1h")
if df.empty or not all(c in df.columns for c in ['Open','High','Low','Close']):
    st.error("資料讀取錯誤：['Open', 'High', 'Low', 'Close']")
    st.stop()

df["EMA10"] = df["Close"].ewm(span=10).mean()
df["EMA20"] = df["Close"].ewm(span=20).mean()
df["RSI"] = ta.rsi(df["Close"])
df["MACD"] = ta.macd(df["Close"])["MACD_12_26_9"]

fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index,
                             open=df["Open"], high=df["High"],
                             low=df["Low"], close=df["Close"],
                             name="K棒"))
fig.add_trace(go.Scatter(x=df.index, y=df["EMA10"], line=dict(color="blue"), name="EMA10"))
fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], line=dict(color="purple"), name="EMA20"))
fig.update_layout(title=ticker, xaxis_title="時間", yaxis_title="價格")
st.plotly_chart(fig, use_container_width=True)

st.line_chart(df[["RSI"]], use_container_width=True)
st.line_chart(df[["MACD"]], use_container_width=True)
