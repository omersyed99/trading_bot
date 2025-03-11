# config.py - Stores API Keys and Trading Settings

import alpaca_trade_api as tradeapi

ALPACA_API_KEY = "PKIUKFSPOV8LK2BTZA39"
ALPACA_SECRET_KEY = "K25oIyWegmOU3YVEbI870uPK7RllFkBzAgTmJDIi"
BASE_URL = "https://paper-api.alpaca.markets"  # Change this for live trading

# Initialize API
api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL, api_version='v2')

# Trading Settings
SYMBOL = "SPXL"
TRADE_QUANTITY = 100
STOP_LOSS_PERCENT = 0.02  # 2% stop loss
TAKE_PROFIT_PERCENT = 0.05  # 5% take profit
