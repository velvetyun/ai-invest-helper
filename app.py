import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="AI 投資助手 v7.5.1", layout="wide")
st.title("📊 BTC 互動式 K 線圖（TradingView 風格）")

# 抓取 BTC-USD 的 1 小時 K 線資料
symbol = st.selectbox("選擇標的", ["BTC-USD", "ETH-USD", "AAPL", "2330.TW"])
data = yf.download(symbol, period="7d", interval="1h")

# 計算 EMA10 / EMA20
data["EMA10"] = data["Close"].ewm(span=10).mean()
data["EMA20"] = data["Close"].ewm(span=20).mean()

# 建立 K 線圖
fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close'],
    name='K線',
    increasing_line_color='green',
    decreasing_line_color='red'
))

# 加入 EMA 線
fig.add_trace(go.Scatter(x=data.index, y=data["EMA10"], line=dict(color='blue', width=1), name="EMA10"))
fig.add_trace(go.Scatter(x=data.index, y=data["EMA20"], line=dict(color='purple', width=1), name="EMA20"))

# 加入成交量（次圖）
fig.update_layout(
    title=f"{symbol} - 1H K 線圖（含 EMA10 / EMA20）",
    xaxis_title="時間",
    yaxis_title="價格",
    xaxis_rangeslider_visible=False,
    template="plotly_white",
    height=600
)

# 成交量圖（疊在下方）
fig.update_layout(
    margin=dict(l=30, r=30, t=60, b=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

st.plotly_chart(fig, use_container_width=True)