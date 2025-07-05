# AI 投資助手｜TradingView 風格 BTC-USD 技術圖腳本

這是一個使用 Python 製作的 K 線技術分析腳本，模擬 TradingView 的顯示風格，支援以下功能：

## 📈 功能說明

- 抓取 BTC-USD（1 小時線）歷史 K 線資料（從 Yahoo Finance）
- 計算並繪製：
  - EMA10 指數移動平均線（藍色）
  - EMA20 指數移動平均線（紫色）
  - 成交量（Volume Bar）
- 匯出為高畫質圖片（PNG／PDF）

## 🚀 執行方式

### 1. 安裝套件

請先安裝相依套件（使用 `pip`）：

```bash
pip install yfinance pandas matplotlib
```

### 2. 執行主程式

```bash
python btc_kline_tradingview.py
```

> ✅ 執行後會自動產生圖表並儲存為 `btc_chart.png`

## 📦 檔案結構

```
ai-invest-helper/
├── btc_kline_tradingview.py      # 主程式
├── README.md                      # 說明文件
```

## 🖼️ 圖表範例

- 綠紅 K 棒（收高/收低）
- 成交量柱狀圖
- EMA10 / EMA20 線條
- 與 TradingView 相似的時間軸與價格刻度

---

© 2025 [velvetyun](https://github.com/velvetyun)｜本程式僅供學術與技術研究使用
