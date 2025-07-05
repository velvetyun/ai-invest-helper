import streamlit as st
from binance.client import Client
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(page_title="AI 投資助手 - 即時幣價版", layout="wide")
st.title("📈 AI 投資助手 - 即時幣價版（K線 + EMA10/EMA20 + 成交量）")

symbol = st.text_input("輸入幣種（如 BTCUSDT、ETHUSDT）", value="BTCUSDT")
client = Client()

# 取得最近 72 小時的 1H 資料
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=72)
klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1H, start_time.strftime('%d %b %Y %H:%M:%S'), end_time.strftime('%d %b %Y %H:%M:%S'))

df = pd.DataFrame(klines, columns=[
    'timestamp', 'Open', 'High', 'Low', 'Close', 'Volume',
    'close_time', 'quote_asset_volume', 'number_of_trades',
    'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
])

df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)
df = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)

df['EMA10'] = df['Close'].ewm(span=10).mean()
df['EMA20'] = df['Close'].ewm(span=20).mean()

fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=df.index, open=df['Open'], high=df['High'],
    low=df['Low'], close=df['Close'], name='K線'
))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA10'], line=dict(color='blue'), name='EMA10'))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], line=dict(color='purple'), name='EMA20'))
fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', yaxis='y2', marker=dict(color='lightgray')))

fig.update_layout(
    title=f"{symbol} 即時 K 線圖",
    xaxis_title='時間',
    yaxis_title='價格',
    yaxis2=dict(title='成交量', overlaying='y', side='right', showgrid=False),
    xaxis_rangeslider_visible=False,
    template='plotly_white',
    legend=dict(orientation="h")
)

st.plotly_chart(fig, use_container_width=True)
