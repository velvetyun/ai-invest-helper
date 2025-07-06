import pyttsx3

def speak_alert(rsi, macd_signal):
    engine = pyttsx3.init()
    message = ""
    if rsi > 70:
        message += "警告：RSI 過熱，請注意風險。"
    if macd_signal == "golden_cross":
        message += "MACD 出現金叉，趨勢可能轉多。"
    if message:
        engine.say(message)
        engine.runAndWait()