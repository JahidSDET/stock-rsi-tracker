# Stock RSI Tracker

A Python-based stock monitoring tool that tracks Relative Strength Index (RSI) for multiple stocks and sends Telegram alerts when stocks become oversold (RSI < 30).

## Features

- 📊 Real-time RSI monitoring for multiple stocks
- 🚨 Telegram notifications for oversold conditions
- 📈 Hourly data analysis over the past month
- 🔧 Easy configuration for custom stock lists
- ⚡ Fast execution using yfinance and pandas-ta

## Prerequisites

- Python 3.7+
- Telegram Bot Token (get one from [@BotFather](https://t.me/botfather))
- Telegram Chat ID (your personal chat or group chat)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/stock-rsi-tracker.git
   cd stock-rsi-tracker
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### 1. Telegram Bot Setup

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot` command
3. Copy the bot token
4. Get your chat ID:
   - Send a message to your bot
   - Visit: `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
   - Copy the chat ID

### 2. Environment Variables

Set the following environment variables:

**For local development:**
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

**For GitHub Actions (GitHub Secrets):**
1. Go to your repository Settings → Secrets and variables → Actions
2. Add two new repository secrets:
   - `TELEGRAM_BOT_TOKEN`: Your bot token
   - `TELEGRAM_CHAT_ID`: Your chat ID

### 3. Customize Stock List

Edit the `stocks` list in `rsi_tracker.py` to include your preferred stocks:

```python
stocks = ["AAPL", "GOOGL", "MSFT", "TSLA"]  # Add your stocks here
```

## Usage

1. **Configure your Telegram bot token and chat ID** in the script
2. **Run the tracker:**
   ```bash
   python rsi_tracker.py
   ```

The script will:
- Download the latest hourly data for each stock
- Calculate RSI(14) for each stock
- Send a Telegram alert if RSI drops below 30
- Print alerts to console

## How It Works

1. **Data Fetching**: Downloads 1 month of hourly data for each stock using yfinance
2. **RSI Calculation**: Computes 14-period RSI using pandas-ta library
3. **Alert System**: Triggers when RSI < 30 (oversold condition)
4. **Notifications**: Sends instant Telegram messages with timestamp and RSI value

## RSI Interpretation

- **RSI > 70**: Overbought (potential sell signal)
- **RSI < 30**: Oversold (potential buy signal)
- **RSI 30-70**: Neutral zone

## Dependencies

- `yfinance` - Yahoo Finance data downloader
- `ta` - Technical analysis library
- `requests` - HTTP library for Telegram API

All dependencies are listed in `requirements.txt` with pinned versions for stability.

## Customization

### Change RSI Period
Modify the RSI length in the calculation:
```python
data['RSI'] = ta.rsi(data['Close'], length=21)  # Change from 14 to 21
```

### Adjust Alert Threshold
Change the oversold threshold:
```python
if latest_rsi < 25:  # More sensitive (was 30)
```

### Add Overbought Alerts
Add alerts for overbought conditions:
```python
if latest_rsi > 70:
    alert = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {stock} RSI is {latest_rsi:.2f} - Overbought!"
    print(alert)
    send_telegram_message(alert)
```

## Scheduling

### GitHub Actions (Recommended)

The repository includes a pre-configured GitHub Actions workflow (`.github/workflows/rsi_tracker.yml`) that will:

- Run automatically every hour
- Use your GitHub Secrets for Telegram credentials
- Send alerts when stocks become oversold

**To activate:**
1. Ensure you've added the repository secrets (`TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`)
2. Push the code to GitHub
3. The workflow will run automatically on schedule

**Manual runs:**
- Go to your repository → Actions tab
- Click "Stock RSI Tracker" workflow
- Click "Run workflow" button

```yaml
name: Stock RSI Tracker

on:
  schedule:
    # Run every hour at minute 0
    - cron: '0 * * * *'
  workflow_dispatch: # Allow manual runs

jobs:
  check-rsi:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install yfinance pandas_ta requests
        
    - name: Run RSI Tracker
      env:
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      run: python rsi_tracker.py
```

### Local Scheduling

To run automatically on your local machine:

**Linux/Mac (every hour):**
```bash
0 * * * * cd /path/to/stock-rsi-tracker && TELEGRAM_BOT_TOKEN=your_token TELEGRAM_CHAT_ID=your_id python rsi_tracker.py
```

**Windows Task Scheduler:**
- Create a new task
- Set trigger to "Daily" with repeat every 1 hour
- Action: Start a program → `python.exe rsi_tracker.py`
- Add environment variables in the task properties

## Disclaimer

This tool is for educational purposes only. Not financial advice. Always do your own research before making investment decisions. Past performance doesn't guarantee future results.

## License

MIT License - feel free to use and modify as needed.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

If you encounter issues:
1. Check your Telegram bot token and chat ID
2. Verify internet connection for data fetching
3. Ensure all dependencies are installed
4. Check console output for error messages