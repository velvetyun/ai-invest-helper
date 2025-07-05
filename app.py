import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI 投資助手 v6", layout="wide")
st.title("💹 AI 投資助手 v6")
st.caption("支援 HA、RSI、SR、FR 等多策略，進出場自動判斷 + 圖示分析")

# 選擇標的
symbol = st.selectbox("選擇標的", ["BTC-USD", "ETH-USD", "2330.TW", "AAPL", "VOO", "^GSPC"])

# 選擇時間週期
interval = st.radio("時間週期", ["1d", "1h", "4h"], horizontal=True)

# 選擇策略模組
strategy = st.multiselect("使用策略模組", ["HA (均化K線)", "RSI", "SR (支撐壓力)", "FR (費波南西)", "RD"], default=["RSI"])

# 下載資料
period = "3mo" if interval == "1d" else "1mo"
data = yf.download(symbol, period=period, interval=interval)

# 計算技術指標
data["MA7"] = data["Close"].rolling(7).mean()
data["MA30"] = data["Close"].rolling(30).mean()
data["RSI"] = 100 - (100 / (1 + data["Close"].pct_change().add(1).rolling(14).apply(lambda r: (r[r>0].mean() or 0) / abs(r[r<0].mean() or 1))))

# 顯示圖表：K 線圖 + RSI + MA
st.subheader("📊 價格與均線圖")
fig, ax = plt.subplots()
ax.plot(data.index, data["Close"], label="Close")
ax.plot(data.index, data["MA7"], label="MA7")
ax.plot(data.index, data["MA30"], label="MA30")
ax.set_ylabel("價格")
ax.legend()
fig.autofmt_xdate()
st.pyplot(fig)

# RSI 圖
if "RSI" in " ".join(strategy):
    st.subheader("📈 RSI 指標")
    fig2, ax2 = plt.subplots()
    ax2.plot(data.index, data["RSI"], label="RSI", color="orange")
    ax2.axhline(70, color='red', linestyle='--', label='超買')
    ax2.axhline(30, color='green', linestyle='--', label='超賣')
    ax2.set_ylabel("RSI")
    ax2.legend()
    fig2.autofmt_xdate()
    st.pyplot(fig2)

# 風控計算
st.subheader("⚙️ 策略判斷結果（Prototype）")

try:
    price_now = float(data["Close"].dropna().iloc[-1])
    entry = price_now
    stop_loss = entry * 0.95
    take_profit = entry * 1.10
    reward = take_profit - entry
    risk = entry - stop_loss
    risk_reward_ratio = round(reward / risk, 2)
    safe_leverage = round(1 / (risk / entry), 1)

    st.write(f"✅ 進場價：{entry:.2f}")
    st.write(f"🛡️ 止損點：{stop_loss:.2f}")
    st.write(f"🎯 止盈點：{take_profit:.2f}")
    st.write(f"📊 盈虧比：{risk_reward_ratio} 倍")
    st.write(f"🔐 安全槓桿建議：{safe_leverage}x")

except Exception as e:
    st.error("❌ 無法計算策略結果，可能是資料不足或錯誤")