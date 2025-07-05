import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="AI 投資助手 v7", layout="wide")
st.title("📊 AI 投資助手 v7")
st.caption("依成交量與趨勢，推薦最適合的技術分析策略 + 專屬圖卡")

# 選擇標的與時間週期
symbol = st.selectbox("選擇標的", ["BTC-USD", "ETH-USD", "2330.TW", "AAPL", "TSLA", "VOO", "^GSPC"])
data = yf.download(symbol, period="3mo", interval="1d")

# 計算技術指標
data["EMA10"] = data["Close"].ewm(span=10).mean()
data["EMA20"] = data["Close"].ewm(span=20).mean()
data["VolumeMA"] = data["Volume"].rolling(5).mean()
data["RSI"] = 100 - (100 / (1 + data["Close"].pct_change().add(1).rolling(14).apply(lambda r: (r[r>0].mean() or 0) / abs(r[r<0].mean() or 1))))
data["MACD"] = data["Close"].ewm(span=12).mean() - data["Close"].ewm(span=26).mean()
data["MACD_Signal"] = data["MACD"].ewm(span=9).mean()

# 自動策略推薦
ema_diff = data["EMA10"].iloc[-1] - data["EMA20"].iloc[-1]
vol_now = data["Volume"].iloc[-1]
vol_ma = data["VolumeMA"].iloc[-1]

suggested_strategies = []

if vol_now > vol_ma:
    suggested_strategies.append("HA（成交量放大）")
if ema_diff > 0:
    suggested_strategies.extend(["RSI（上升趨勢）", "SR（支撐壓力）"])
elif ema_diff < 0:
    suggested_strategies.extend(["FR（下跌回撤）", "RD（風險區偵測）"])
if data["RSI"].iloc[-1] > 70 or data["RSI"].iloc[-1] < 30:
    suggested_strategies.append("RSI（超買超賣）")
if data["MACD"].iloc[-1] > data["MACD_Signal"].iloc[-1]:
    suggested_strategies.append("MACD（多頭交叉）")
else:
    suggested_strategies.append("MACD（空頭交叉）")

st.subheader("🤖 系統推薦策略")
for s in suggested_strategies:
    st.markdown(f"✔️ {s}")

# 顯示圖卡
st.subheader("🧭 策略圖卡")

if "RSI" in " ".join(suggested_strategies):
    st.markdown("### 📈 RSI 指標")
    fig, ax = plt.subplots()
    ax.plot(data.index, data["RSI"], label="RSI", color="orange")
    ax.axhline(70, color='red', linestyle='--', label='超買')
    ax.axhline(30, color='green', linestyle='--', label='超賣')
    ax.legend()
    fig.autofmt_xdate()
    st.pyplot(fig)

if "MACD（多頭交叉）" in suggested_strategies or "MACD（空頭交叉）" in suggested_strategies:
    st.markdown("### 📉 MACD 指標")
    fig, ax = plt.subplots()
    ax.plot(data.index, data["MACD"], label="MACD", color="blue")
    ax.plot(data.index, data["MACD_Signal"], label="Signal", color="gray")
    ax.fill_between(data.index, data["MACD"] - data["MACD_Signal"], color="skyblue", alpha=0.4)
    ax.axhline(0, color='black', linestyle='--')
    ax.legend()
    fig.autofmt_xdate()
    st.pyplot(fig)

if "HA（成交量放大）" in suggested_strategies:
    st.markdown("### 🧱 Heikin-Ashi 模擬（以平均 K 線展示）")
    ha_close = (data["Open"] + data["High"] + data["Low"] + data["Close"]) / 4
    fig, ax = plt.subplots()
    ax.plot(data.index, ha_close, label="HA Avg Close", color="purple")
    ax.plot(data.index, data["EMA10"], label="EMA10", linestyle="--")
    ax.plot(data.index, data["EMA20"], label="EMA20", linestyle="--")
    ax.legend()
    fig.autofmt_xdate()
    st.pyplot(fig)