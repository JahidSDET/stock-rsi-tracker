import yfinance as yf 
import pandas_ta as ta
import requests
from datetime import datetime
import os
import json

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

# 3️⃣ File to remember alerted stocks
ALERT_FILE = "alerted_stocks.json"

# Load previously alerted stocks
try:
    with open(ALERT_FILE, "r") as f:
        alerted = json.load(f)
except FileNotFoundError:
    alerted = {}

# 4️⃣ Function to send Telegram alert
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)

# 5️⃣ Check RSI for each stock
for stock in stocks:
    data = yf.download(stock, period="1mo", interval="1h", progress=False)
    data['RSI'] = ta.rsi(data['Close'], length=14)
    
    latest_rsi = data['RSI'].iloc[-1]
    
    # Send alert only if RSI < 30 and not already alerted
    if latest_rsi < 30 and not alerted.get(stock, False):
        alert = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {stock} RSI is {latest_rsi:.2f} - Oversold!"
        print(alert)
        send_telegram_message(alert)
        alerted[stock] = True
    
    # Reset alert if RSI goes back above 30
    if latest_rsi >= 30 and alerted.get(stock, False):
        alerted[stock] = False

# Save alert status
with open(ALERT_FILE, "w") as f:
    json.dump(alerted, f)