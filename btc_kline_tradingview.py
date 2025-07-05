import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 下載 BTC 資料（1小時K線）
btc = yf.download("BTC-USD", interval="1h", period="30d")

# 計算 EMA
btc["EMA10"] = btc["Close"].ewm(span=10).mean()
btc["EMA20"] = btc["Close"].ewm(span=20).mean()

# 畫圖
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, 
                              gridspec_kw={'height_ratios': [3, 1]})
ax.plot(btc.index, btc["Close"], label="Close", color="black", linewidth=1)
ax.plot(btc.index, btc["EMA10"], label="EMA 10", color="blue", linewidth=1)
ax.plot(btc.index, btc["EMA20"], label="EMA 20", color="purple", linewidth=1)
ax.set_title("BTC/USD 1H Chart with EMA10 & EMA20", fontsize=14)
ax.legend()
ax.grid(True)

# 成交量
ax2.bar(btc.index, btc["Volume"], color="gray")
ax2.set_ylabel("Volume")
ax2.grid(True)

# x軸日期格式
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d
%H:%M'))
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("btc_chart.png", dpi=300)
plt.show()
