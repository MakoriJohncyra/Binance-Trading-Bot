# Binance Futures Trading Bot for Beginners

A simple, beginner-friendly trading bot for Binance Futures **Testnet** (practice mode with fake money).  
Perfect for learning how futures trading works without risking any real funds.

## Features

- Market Orders — Buy or sell immediately at current market price
- Limit Orders — Place buy/sell orders at a specific target price
- Beginner-Friendly — Clear error messages and helpful guidance
- Safe Practice — 100% uses Binance Futures Testnet (no real money involved)
- Logging — Records all trades, errors and important events
- Input Validation — Checks commands before sending them to Binance

## Requirements

- Python 3.8 or higher
- Binance Futures Testnet account
- Internet connection

## Project Structure
```
trading_bot/
├── bot/
│   ├── client.py          # Binance API communication
│   ├── validators.py      # Input checks & safety rules
│   ├── logging_config.py  # Logging setup
│   └── __init__.py
├── cli.py                 # Command line interface
├── requirements.txt       # Dependencies list
├── .env.example           # API key template
└── README.md              # Explains about the project
```

## Setup (Step-by-Step)

### Step 1: Install Python

Make sure you have Python 3.8+ installed.

Check your version in terminal/command prompt:

```bash
python --version
# or
python3 --version
```

### Step 2: Create Binance Futures Testnet Account

-Go to: https://testnet.binancefuture.com

-Click Register (use email login — no KYC needed)

-After logging in → go to API Management (usually in profile or sidebar)   

-Click Create API Key

-Copy and securely save both:

        1.API Key
        
        2.Secret Key

### Step 3: Install the Bot
-Download or clone this repository to your computer
-Open a terminal / command prompt
-Navigate to the project folder:
```bash
cd path/to/trading_bot
```        
-Install required Python packages:
```bash
pip install -r requirements.txt
```
### Step 4: Add Your API Keys
-Create your configuration file:
```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```
- Open the new .env file in your text editor
- Paste your keys.
-Save and close the file.

### Basic Commands
## 1. Market Order (executes immediately)
```bash 
# Buy 0.003 BTC at current market price
python cli.py BTCUSDT BUY MARKET 0.003

# Sell 0.05 ETH right now
python cli.py ETHUSDT SELL MARKET 0.05
```
## 2. Limit Order (waits for a specific price)
```bash
# Buy 0.05 ETH only if price drops to 2200
python cli.py ETHUSDT BUY LIMIT 0.05 --price 2200

# Sell 0.003 BTC if price reaches 65000
python cli.py BTCUSDT SELL LIMIT 0.003 --price 65000
```

