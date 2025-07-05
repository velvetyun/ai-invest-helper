import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="AI 投資助手", layout="wide")

st.title("📈 AI 投資助手 - K 線圖 ＋ EMA10/EMA20 ＋ 成交量")
symbol = st.text_input("輸入幣種（如 BTC-USD、ETH-USD、2330.TW）", value="BTC-USD")

try:
    df = yf.download(symbol, period="30d", interval="1h", progress=False)
    if df.empty:
        raise ValueError("查無資料，請確認代碼格式是否正確，或該標的不支援 1 小時線。")
    df.dropna(subset=["Open", "High", "Low", "Close"], inplace=True)
    df["EMA10"] = df["Close"].ewm(span=10).mean()
    df["EMA20"] = df["Close"].ewm(span=20).mean()

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                    name="K線"))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA10"], line=dict(color='blue', width=1), name="EMA10"))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], line=dict(color='purple', width=1), name="EMA20"))

    fig.update_layout(title=f"{symbol} K 線圖 + EMA10/EMA20 + 成交量",
                      yaxis_title="價格", xaxis_rangeslider_visible=False)

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"資料讀取錯誤：{e}")
