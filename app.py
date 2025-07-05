import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pycoingecko import CoinGeckoAPI
import ta

st.set_page_config(page_title="AI 投資助手 - K棒圖 + RSI + MACD", layout="wide")
st.title("📈 AI 投資助手 - K棒圖 + EMA10/20 + RSI + MACD + 成交量")

cg = CoinGeckoAPI()

coin_mapping = {
    "比特幣 BTC": "bitcoin",
    "以太幣 ETH": "ethereum",
    "幣安幣 BNB": "binancecoin",
    "狗狗幣 DOGE": "dogecoin",
    "萊特幣 LTC": "litecoin"
}

coin_name = st.selectbox("選擇幣種", list(coin_mapping.keys()))
coin_id = coin_mapping[coin_name]
days = st.selectbox("查詢天數", ["1", "7", "30", "90"], index=1)

data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=days)
prices = data['prices']
df = pd.DataFrame(prices, columns=["時間", "價格"])
df["時間"] = pd.to_datetime(df["時間"], unit="ms")
df.set_index("時間", inplace=True)
df["收盤價"] = df["價格"]
df["開盤價"] = df["收盤價"].shift(1)
df["最高價"] = df["收盤價"].rolling(window=3).max()
df["最低價"] = df["收盤價"].rolling(window=3).min()
df["成交量"] = [v[1] for v in data['total_volumes']]
df.dropna(inplace=True)

df["EMA10"] = ta.trend.ema_indicator(df["收盤價"], window=10).fillna(0)
df["EMA20"] = ta.trend.ema_indicator(df["收盤價"], window=20).fillna(0)
df["RSI"] = ta.momentum.rsi(df["收盤價"], window=14).fillna(0)
macd = ta.trend.macd(df["收盤價"])
df["MACD"] = macd.macd_diff().fillna(0)

signal = []
for i in range(len(df)):
    if df["EMA10"].iloc[i] > df["EMA20"].iloc[i] and df["RSI"].iloc[i] < 30:
        signal.append("📈 可能買入訊號")
    elif df["EMA10"].iloc[i] < df["EMA20"].iloc[i] and df["RSI"].iloc[i] > 70:
        signal.append("📉 可能賣出訊號")
    else:
        signal.append("")
df["交易提示"] = signal

latest_signal = df["交易提示"].iloc[-1]
if latest_signal:
    st.subheader(f"💡 最新交易提示：{latest_signal}")

# K棒圖
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df["開盤價"],
    high=df["最高價"],
    low=df["最低價"],
    close=df["收盤價"],
    name="K棒"
))
fig.add_trace(go.Scatter(x=df.index, y=df["EMA10"], name="EMA10", line=dict(color="blue")))
fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], name="EMA20", line=dict(color="orange")))
fig.update_layout(title=f"{coin_name} 過去 {days} 天 K棒圖", xaxis_title="時間", yaxis_title="價格（USD）", height=600)

st.plotly_chart(fig, use_container_width=True)
st.subheader("📊 RSI 與 MACD")
st.line_chart(df[["RSI", "MACD"]])
st.subheader("📋 最近 10 筆交易提示")
st.dataframe(df[["收盤價", "RSI", "MACD", "交易提示"]].tail(10))