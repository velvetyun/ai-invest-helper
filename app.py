import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

st.set_page_config(layout="wide")
st.title("📊 AI 投資助手 - 多幣 K 線 + EMA10/20 + 成交量")
st.markdown("資料來源：CoinGecko API")

coins = {
    "BTC-USD": "bitcoin",
    "ETH-USD": "ethereum",
    "BNB-USD": "binancecoin",
    "DOGE-USD": "dogecoin",
    "LTC-USD": "litecoin"
}

col1, col2 = st.columns([3, 1])
with col1:
    selected = st.multiselect("選擇幣種", options=list(coins.keys()), default=["BTC-USD"])
with col2:
    days = st.selectbox("選擇查詢天數", options=["7", "30", "90"], index=1)

for symbol in selected:
    coin_id = coins[symbol]
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
    try:
        res = requests.get(url).json()
        prices = res["prices"]
        volumes = res["total_volumes"]
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["volume"] = [v[1] for v in volumes]
        df["time"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("time", inplace=True)
        df["EMA10"] = df["price"].ewm(span=10).mean()
        df["EMA20"] = df["price"].ewm(span=20).mean()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df["price"], mode="lines", name="K 線"))
        fig.add_trace(go.Scatter(x=df.index, y=df["EMA10"], mode="lines", name="EMA10"))
        fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], mode="lines", name="EMA20"))
        fig.update_layout(title=f"{symbol} - 最近 {days} 天", xaxis_title="時間", yaxis_title="價格", height=500)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"{symbol} 資料讀取錯誤：{e}")