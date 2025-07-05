import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI 投資助手", layout="wide")
st.title("💹 AI 投資助手")
st.caption("AI 幫你自動判斷進出場點，穩穩獲利")

symbol = st.selectbox("選擇標的", ["BTC-USD", "ETH-USD", "2330.TW"], index=0)

data = yf.download(symbol, period="3mo")
data["MA7"] = data["Close"].rolling(7).mean()
data["MA30"] = data["Close"].rolling(30).mean()

# 抓最近有價的收盤價
try:
    price_now = float(data["Close"].dropna().iloc[-1])
except Exception:
    price_now = None

try:
    ma7 = float(data["MA7"].dropna().iloc[-1])
except Exception:
    ma7 = None

try:
    ma30 = float(data["MA30"].dropna().iloc[-1])
except Exception:
    ma30 = None

# 顯示現價
if price_now is not None:
    st.subheader(f"現價：{price_now:.2f}")
else:
    st.warning("⚠️ 無法取得價格資料")

# 策略判斷
if (ma7 is not None) and (ma30 is not None) and (price_now is not None):
    if ma7 > ma30:
        direction = "做多 📈"
        entry = price_now
        stop = entry * 0.9
        take = entry * 1.15
        st.success("📈 建議：做多")
    elif ma7 < ma30:
        direction = "做空 📉"
        entry = price_now
        stop = entry * 1.05
        take = entry * 0.85
        st.error("📉 建議：做空")
    else:
        direction = "觀望"
        st.warning("⚠️ 建議：觀望")
else:
    direction = "觀望"
    st.warning("⚠️ 尚未形成完整均線判斷，請稍後再試")

if direction != "觀望" and price_now is not None:
    st.write(f"進場價位：{entry:.2f}")
    st.write(f"止損點：{stop:.2f}")
    st.write(f"出場點：{take:.2f}")

# 畫圖
st.subheader("價格走勢圖")
fig, ax = plt.subplots()
ax.plot(data.index, data["Close"], label="Close")
ax.plot(data.index, data["MA7"], label="MA7")
ax.plot(data.index, data["MA30"], label="MA30")
ax.legend()
st.pyplot(fig)