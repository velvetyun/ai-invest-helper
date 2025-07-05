import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📈 BTC K線圖（TradingView風格）")
st.caption("資料來源：Yahoo Finance（BTC-USD），K線 + EMA10/EMA20 + 成交量")

# 抓取資料
ticker = "BTC-USD"
data = yf.download(ticker, period="7d", interval="1h")
data["EMA10"] = data["Close"].ewm(span=10, adjust=False).mean()
data["EMA20"] = data["Close"].ewm(span=20, adjust=False).mean()

# 畫圖
fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=data.index,
    open=data["Open"],
    high=data["High"],
    low=data["Low"],
    close=data["Close"],
    name="K線"
))

fig.add_trace(go.Scatter(x=data.index, y=data["EMA10"], mode="lines", line=dict(color="blue"), name="EMA10"))
fig.add_trace(go.Scatter(x=data.index, y=data["EMA20"], mode="lines", line=dict(color="purple"), name="EMA20"))

# 成交量放底下
fig.update_layout(
    xaxis_rangeslider_visible=False,
    yaxis_title="價格",
    margin=dict(l=10, r=10, t=40, b=10),
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("📊 成交量")
st.bar_chart(data["Volume"])
