import streamlit as st
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pycoingecko import CoinGeckoAPI

st.set_page_config(page_title="AI 投資助手 - K棒圖 + EMA10/20 + RSI + MACD + 成交量", layout="wide")
st.title("📈 AI 投資助手 - K棒圖 + EMA10/20 + RSI + MACD + 成交量")

cg = CoinGeckoAPI()

symbol_dict = {
    "比特幣 BTC": "bitcoin",
    "以太幣 ETH": "ethereum",
    "瑞波幣 XRP": "ripple",
    "萊特幣 LTC": "litecoin"
}

days_options = ["1", "3", "7", "14", "30", "60", "90"]
symbol_name = st.selectbox("選擇幣種", list(symbol_dict.keys()))
days = st.selectbox("查詢天數", days_options)
vs_currency = "usd"

try:
    coin_id = symbol_dict[symbol_name]
    data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency=vs_currency, days=days)
    prices = data["prices"]
    volumes = data["total_volumes"]

    df = pd.DataFrame(prices, columns=["時間", "收盤價"])
    df["成交量"] = [v[1] for v in volumes]
    df["時間"] = pd.to_datetime(df["時間"], unit="ms")
    df.set_index("時間", inplace=True)
    df["收盤價"] = pd.to_numeric(df["收盤價"], errors="coerce")
    df["成交量"] = pd.to_numeric(df["成交量"], errors="coerce")
    df["EMA10"] = ta.ema(df["收盤價"], length=10)
    df["EMA20"] = ta.ema(df["收盤價"], length=20)
    df["RSI"] = ta.rsi(df["收盤價"], length=14)
    macd = df.ta.macd()
    df["MACD"] = macd["MACD_12_26_9"]
    df["MACD_signal"] = macd["MACDs_12_26_9"]

    # 交易提示
    signal = ""
    if df["EMA10"].iloc[-1] > df["EMA20"].iloc[-1]:
        signal = "📈 建議：短期上揚，考慮進場"
    elif df["EMA10"].iloc[-1] < df["EMA20"].iloc[-1]:
        signal = "📉 建議：短期走弱，考慮觀望"

    st.success(signal)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["收盤價"], mode="lines", name="K棒", line=dict(color="lightgray")))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA10"], mode="lines", name="EMA10", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], mode="lines", name="EMA20", line=dict(color="purple")))
    fig.update_layout(title=f"{symbol_name} 過去 {days} 天", yaxis_title="價格")

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📉 RSI / MACD")
    st.line_chart(df[["RSI"]])
    st.line_chart(df[["MACD", "MACD_signal"]])

    st.subheader("📊 成交量")
    st.bar_chart(df["成交量"])

except Exception as e:
    st.error(f"資料讀取錯誤：{e}")