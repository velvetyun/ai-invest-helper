import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI 投資助手 v7.4.1", layout="wide")
st.title("📊 AI 投資助手 v7.4.1")
st.caption("修復 Volume Profile 錯誤 + 自動支撐壓力分析")

# ➤ 使用者輸入標的
symbol = st.text_input("輸入標的（如 BTC-USD、2330.TW、AAPL）", value="BTC-USD")

# ➤ 抓資料
try:
    df = yf.download(symbol, period="3mo", interval="1d")
except:
    st.error("資料載入失敗")
    st.stop()

# ➤ 技術指標
df["EMA10"] = df["Close"].ewm(span=10).mean()
df["EMA20"] = df["Close"].ewm(span=20).mean()

# =======================
# 📊 成交量分佈圖 (Volume Profile)
# =======================
st.subheader("📊 成交量分佈圖（Volume Profile）")

bin_size = st.slider("價格分箱數（區間分段）", 20, 100, 40)
price_min = df["Low"].min()
price_max = df["High"].max()
bins = np.linspace(price_min, price_max, bin_size)

# ✅ 修正版本：正確分箱與 Volume 加總
cut_bins = pd.cut(df["Close"], bins=bins)
volume_profile = pd.DataFrame({
    "bin": cut_bins,
    "volume": df["Volume"]
})
vol_dist = volume_profile.groupby("bin")["volume"].sum()

# 畫圖
fig, ax = plt.subplots(figsize=(5, 6))
labels = [f"{interval.left:.2f}-{interval.right:.2f}" for interval in vol_dist.index]
ax.barh(labels, vol_dist.values, color="skyblue")
ax.invert_yaxis()
ax.set_xlabel("成交量")
ax.set_ylabel("價格區間")
st.pyplot(fig)

# =======================
# 🧱 自動支撐壓力線（SR）
# =======================
st.subheader("🧱 自動偵測支撐與壓力線（SR）")

def detect_sr_levels(data, window=10, tolerance=0.01):
    support, resistance = [], []
    for i in range(window, len(data) - window):
        low = data["Low"].iloc[i]
        high = data["High"].iloc[i]

        is_support = all(low < data["Low"].iloc[i - j] for j in range(1, window)) and                      all(low < data["Low"].iloc[i + j] for j in range(1, window))
        is_resistance = all(high > data["High"].iloc[i - j] for j in range(1, window)) and                         all(high > data["High"].iloc[i + j] for j in range(1, window))

        if is_support:
            if not any(abs(low - s) < tolerance * s for s in support):
                support.append(low)
        if is_resistance:
            if not any(abs(high - r) < tolerance * r for r in resistance):
                resistance.append(high)

    return support, resistance

support, resistance = detect_sr_levels(df)

# ➤ 畫出 SR 水平線
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(df.index, df["Close"], label="Close", linewidth=1.5)

for s in support:
    ax2.axhline(s, color="green", linestyle="--", alpha=0.5)
for r in resistance:
    ax2.axhline(r, color="red", linestyle="--", alpha=0.5)

ax2.set_title(f"{symbol} 支撐（綠）與壓力（紅）線")
ax2.legend()
fig2.autofmt_xdate()
st.pyplot(fig2)