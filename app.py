import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import pandas_ta as ta

st.set_page_config(page_title="AI 投資助手", layout="wide")

st.title("📈 AI 投資助手 - K棒圖 + EMA10/20 + RSI + MACD + 成交量")

symbol_dict = {
    "比特幣 BTC": "BTC-USD",
    "以太幣 ETH": "ETH-USD",
    "台積電 2330.TW": "2330.TW",
    "蘋果 AAPL": "AAPL"
}
symbol_label = st.selectbox("選擇幣種", list(symbol_dict.keys()))
symbol = symbol_dict[symbol_label]

days = st.selectbox("查詢天數", [1, 3, 5, 10, 30])
interval = "15m" if days <= 3 else "1h"

try:
    df = yf.download(symbol, period=f"{days}d", interval=interval, progress=False)
    df = df.dropna(subset=["Open", "High", "Low", "Close"])
    df["EMA10"] = ta.ema(df["Close"], length=10)
    df["EMA20"] = ta.ema(df["Close"], length=20)
    df["RSI"] = ta.rsi(df["Close"], length=14)
    macd_df = ta.macd(df["Close"])
    df["MACD"] = macd_df["MACD_12_26_9"]
    df["MACD_hist"] = macd_df["MACDh_12_26_9"]

    st.subheader(f"{symbol_label} K棒圖")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df["Open"],
                                 high=df["High"],
                                 low=df["Low"],
                                 close=df["Close"],
                                 name="K棒"))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA10"], line=dict(color='blue', width=1), name='EMA10'))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], line=dict(color='purple', width=1), name='EMA20'))
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 RSI + MACD 指標")
    if "RSI" in df.columns and "MACD" in df.columns:
        fig2 = px.line(df, y=["RSI", "MACD", "MACD_hist"], labels={"value": "指標值", "variable": "指標"})
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.error("指標資料不足，請調高查詢天數。")
except Exception as e:
    st.error(f"資料讀取錯誤：\n{e}")