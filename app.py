
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

st.set_page_config(layout="wide")
st.title("📈 AI 投資助手 - K線圖 + EMA10/EMA20 + 成交量")

symbol = st.text_input("輸入標的（如 BTC-USD、2330.TW、AAPL）", "BTC-USD")

df = yf.download(symbol, period="7d", interval="1h")
df = df.dropna(subset=['Open', 'High', 'Low', 'Close'])

df['EMA10'] = df['Close'].ewm(span=10, adjust=False).mean()
df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name='K線'
))
fig.add_trace(go.Scatter(
    x=df.index, y=df['EMA10'], mode='lines', name='EMA10', line=dict(color='blue')
))
fig.add_trace(go.Scatter(
    x=df.index, y=df['EMA20'], mode='lines', name='EMA20', line=dict(color='purple')
))

fig.update_layout(
    title=f"{symbol} K線 + EMA10/EMA20",
    xaxis_title="時間", yaxis_title="價格",
    xaxis_rangeslider_visible=False,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.caption("資料來源：Yahoo Finance")
