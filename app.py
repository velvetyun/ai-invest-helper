import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from voice_alert import speak_alert

st.set_page_config(layout="wide", page_title="AI 投資助手 - 語音版")

st.title("📈 AI 投資助手 v3.0 - 語音提示版")

symbol = st.selectbox("選擇幣種", ["BTC", "ETH"])
days = st.selectbox("查詢天數", [1, 3, 7, 14, 30])

# 假資料模擬
df = pd.DataFrame({
    "Close": [108000 + i * 20 for i in range(40)],
})

# 繪圖
fig = go.Figure()
fig.add_trace(go.Scatter(y=df['Close'], name="收盤價"))
st.plotly_chart(fig, use_container_width=True)

# 檢查條件並播報
rsi_value = 72  # 假資料
macd_signal = "golden_cross"
speak_alert(rsi_value, macd_signal)