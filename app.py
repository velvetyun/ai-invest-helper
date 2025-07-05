
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

st.set_page_config(page_title="AI 投資助手", page_icon="📈", layout="wide")
st.title("📈 AI 投資助手 - K線圖 + EMA10/EMA20 + 成交量")

symbol = st.text_input("輸入標的（如 BTC-USD、2330.TW、AAPL）", value="BTC-USD")

# 下載資料
df = yf.download(symbol, period="30d", interval="1h", progress=False)

# 檢查欄位是否存在
expected_columns = ['Open', 'High', 'Low', 'Close']
if not all(col in df.columns for col in expected_columns):
    st.error("❌ 資料格式錯誤，無法繪製 K 線圖，請檢查輸入的標的是否正確。")
    st.stop()

# 計算 EMA
df['EMA10'] = df['Close'].ewm(span=10).mean()
df['EMA20'] = df['Close'].ewm(span=20).mean()

# 畫圖
fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Open'],
                             high=df['High'],
                             low=df['Low'],
                             close=df['Close'],
                             name='K線'))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA10'], name='EMA10', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], name='EMA20', line=dict(color='purple')))

fig.update_layout(title=f"{symbol} K線圖 + EMA10/20 + 成交量", xaxis_title='時間', yaxis_title='價格')
st.plotly_chart(fig, use_container_width=True)
