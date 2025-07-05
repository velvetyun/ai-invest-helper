
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 下載 BTC/USD 1H 資料（用 Binance K 線模擬）
url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"
response = requests.get(url)
data = response.json()

# 轉換為 DataFrame
df = pd.DataFrame(data, columns=[
    "Open Time", "Open", "High", "Low", "Close", "Volume",
    "Close Time", "Quote Asset Volume", "Number of Trades",
    "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore"
])
df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms")
df["Close"] = df["Close"].astype(float)
df["Volume"] = df["Volume"].astype(float)

# 計算 EMA
df["EMA10"] = df["Close"].ewm(span=10, adjust=False).mean()
df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()

# 畫圖
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df["Open Time"], df["Close"], label="Close Price", color="black")
ax.plot(df["Open Time"], df["EMA10"], label="EMA10", color="blue", linestyle="--")
ax.plot(df["Open Time"], df["EMA20"], label="EMA20", color="purple", linestyle="--")
ax.set_title("BTC/USDT 1H K線 + EMA10/20")
ax.set_xlabel("Time")
ax.set_ylabel("Price (USDT)")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
plt.xticks(rotation=45)
ax.legend()
plt.tight_layout()
plt.savefig("btc_kline.png")
plt.show()
