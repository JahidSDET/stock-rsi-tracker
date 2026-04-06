import yfinance as yf
import pandas_ta as ta
import requests
from datetime import datetime
import os

# 1️⃣ Stocks to track
stocks = ["AMZN","SOFI","MARA","MSFT","PATH","XNET","PYPL",
          "ORCL","IBIT","BBAI","HIMS","SOUN","SMCI","BULL",
          "FUBO","META","UNH","NVDA","MSTR","S","PANW"]

# 2️⃣ Telegram bot info from environment variables
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

# Check if environment variables are set
if not bot_token or not chat_id:
    print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables must be set!")
    exit(1)

# 3️⃣ Function to send Telegram alert
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)

# 4️⃣ Check RSI for each stock
for stock in stocks:
    data = yf.download(stock, period="1mo", interval="1h")
    data['RSI'] = ta.rsi(data['Close'], length=14)
    
    latest_rsi = data['RSI'].iloc[-1]
    
    if latest_rsi < 30:
        alert = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {stock} RSI is {latest_rsi:.2f} - Oversold!"
        print(alert)
        send_telegram_message(alert)