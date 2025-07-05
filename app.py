import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="AI 投資助手 v2.2", layout="wide")
st.title("📈 AI 投資助手 - K 線圖 ＋ EMA10/EMA20 ＋ 成交量")

symbol = st.text_input("輸入幣種（如 BTC-USD、ETH-USD、2330.TW）", value="BTC-USD")

try:
    df = yf.download(symbol, period="7d", interval="1h", progress=False)
    if df.empty or not all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
        raise ValueError("資料讀取錯誤：Yahoo Finance 無法提供此幣種的 K 線資料")

    df.dropna(subset=['Open', 'High', 'Low', 'Close'], inplace=True)
    df['EMA10'] = df['Close'].ewm(span=10).mean()
    df['EMA20'] = df['Close'].ewm(span=20).mean()

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name='K線'))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA10'], line=dict(color='blue', width=1), name='EMA10'))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], line=dict(color='purple', width=1), name='EMA20'))
    fig.update_layout(title=f"{symbol} K 線圖＋EMA", xaxis_title="時間", yaxis_title="價格", height=600)

    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"資料讀取錯誤：{e}")
    st.info("✅ 請確認幣種格式（如 BTC-USD）與 Yahoo Finance 是否支援。\n📌 推薦測試：ETH-USD、AAPL、2330.TW")