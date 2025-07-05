
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# 下載 BTC-USD 1 小時資料
df = yf.download('BTC-USD', interval='1h', period='7d')
df['EMA10'] = df['Close'].ewm(span=10).mean()
df['EMA20'] = df['Close'].ewm(span=20).mean()

# 建立圖表
fig = go.Figure()

# K 棒
fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Open'], high=df['High'],
                             low=df['Low'], close=df['Close'],
                             name='K線'))

# EMA 線
fig.add_trace(go.Scatter(x=df.index, y=df['EMA10'], line=dict(color='blue', width=1), name='EMA10'))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], line=dict(color='purple', width=1), name='EMA20'))

# 成交量圖
fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='成交量', yaxis='y2', marker_color='lightgray'))

# 雙軸設定
fig.update_layout(
    title='BTC-USD 1小時K線圖 (含EMA10/20 + 成交量)',
    xaxis=dict(domain=[0, 1]),
    yaxis=dict(title='價格'),
    yaxis2=dict(title='成交量', overlaying='y', side='right', showgrid=False),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# 匯出為 HTML
fig.write_html("btc_chart.html")
print("✅ 已完成：btc_chart.html 匯出成功，可用瀏覽器開啟查看圖表。")
