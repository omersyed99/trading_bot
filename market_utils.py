# market_utils.py - Handles market status & API connections

from datetime import datetime
import pytz
import alpaca_trade_api as tradeapi
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL, SYMBOL

# Initialize Alpaca API
api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL, api_version='v2')

def is_market_open():
    """Check if the US stock market is open (NYSE trading hours)."""
    est = pytz.timezone("America/New_York")
    now = datetime.now(est)

    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)

    if now.weekday() in [5, 6]:  # Saturday (5) or Sunday (6)
        return False

    return market_open <= now <= market_close

def get_latest_stock_price():
    """Fetch the latest stock price from Alpaca API."""
    try:
        trade = api.get_latest_trade(SYMBOL)
        return float(trade.price)
    except Exception as e:
        print(f"Error retrieving live price: {e}")
        return None
