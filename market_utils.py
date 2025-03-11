import numpy as np
import pytz
from datetime import datetime
from config import api, SYMBOL


def is_market_open():
    """Check if NYSE market is open."""
    est = pytz.timezone("America/New_York")
    now = datetime.now(est)
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)

    if now.weekday() in [5, 6]:  # Saturday (5) or Sunday (6)
        return False
    return market_open <= now <= market_close

def get_market_data():
    """Fetches live market data and ensures correct shape"""
    try:
        if not is_market_open():
            print("Market is closed. Returning default values.")
            return np.zeros(5, dtype=np.float32)

        trade = api.get_latest_trade(SYMBOL)
        stock_price = float(trade.price)
        bars = api.get_bars(SYMBOL, timeframe="1Day", limit=200).df

        sma_50 = float(bars["close"].rolling(window=50).mean().iloc[-1])
        sma_200 = float(bars["close"].rolling(window=200).mean().iloc[-1])
        rsi = 100 - (100 / (1 + stock_price / sma_50))  # Approximate RSI
        atr = float(bars["high"].rolling(14).max().iloc[-1] - bars["low"].rolling(14).min().iloc[-1])

        obs = np.array([stock_price, sma_50, sma_200, rsi, atr], dtype=np.float32)

        if obs.shape != (5,):
            print(f"Warning: Observation shape is {obs.shape}, expected (5,). Fixing...")
            obs = obs.flatten()  # Ensure shape is (5,)

        return obs

    except Exception as e:
        print(f"Market data error: {e}")
        return np.zeros(5, dtype=np.float32)  # Return default values if API fails


