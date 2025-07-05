
import streamlit as st
import pandas as pd
import pandas_ta as ta
import plotly.graph_objs as go
import datetime
import requests

# 幣種選單與天數選單
symbol_map = {
    "比特幣 BTC": "bitcoin",
    "以太幣 ETH": "ethereum",
    "狗狗幣 DOGE": "dogecoin"
}
symbol_display = list(symbol_map.keys())
days_options = ["1", "3", "7", "14", "30", "90", "180", "365"]

st.title("📈 AI 投資助手 - K棒圖 + EMA10/20 + RSI + MACD + 成交量")

symbol_label = st.selectbox("選擇幣種", symbol_display)
days = st.selectbox("查詢天數", days_options)
symbol = symbol_map[symbol_label]

# 取得資料
url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart?vs_currency=usd&days={days}&interval=hourly"
r = requests.get(url)
data = r.json()

df = pd.DataFrame({
    '時間': pd.to_datetime([x[0] for x in data['prices']], unit='ms'),
    '價格': [x[1] for x in data['prices']],
    '成交量': [x[1] for x in data['total_volumes']]
})
df.set_index('時間', inplace=True)
df['EMA10'] = df['價格'].ewm(span=10).mean()
df['EMA20'] = df['價格'].ewm(span=20).mean()
df['RSI'] = ta.rsi(df['價格'], length=14)
macd = ta.macd(df['價格'])
df["MACD"] = macd.macd_diff().fillna(0)

# 畫圖
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['價格'], high=df['價格'], low=df['價格'], close=df['價格'],
    name="K棒"
))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA10'], line=dict(color='blue', width=1), name='EMA10'))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], line=dict(color='purple', width=1), name='EMA20'))

fig.update_layout(title=f"{symbol_label} - K棒圖", yaxis_title="價格", xaxis_rangeslider_visible=False)

st.plotly_chart(fig)

# 額外指標區塊
st.subheader("📊 RSI / MACD 圖表")

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='orange')))
fig2.update_layout(title="RSI (相對強弱指標)", yaxis=dict(range=[0, 100]))
st.plotly_chart(fig2)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='green')))
fig3.update_layout(title="MACD 差離值")
st.plotly_chart(fig3)
