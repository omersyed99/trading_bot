# trading_bot.py - Main Trading Bot Script

import time
import numpy as np
from market_utils import is_market_open, get_latest_stock_price
from config import api, SYMBOL, TRADE_QUANTITY, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT

def execute_trade(action):
    """Executes buy or sell orders with stop-loss & take-profit."""
    if action == "BUY":
        price = get_latest_stock_price()
        if price:
            stop_loss = round(price * (1 - STOP_LOSS_PERCENT), 2)
            take_profit = round(price * (1 + TAKE_PROFIT_PERCENT), 2)

            try:
                api.submit_order(symbol=SYMBOL, qty=TRADE_QUANTITY, side="buy", type="market", time_in_force="gtc")
                print(f"BUY ORDER EXECUTED at ${price}")

                api.submit_order(symbol=SYMBOL, qty=TRADE_QUANTITY, side="sell", type="stop", stop_price=stop_loss, time_in_force="gtc")
                print(f"STOP-LOSS SET at ${stop_loss}")

                api.submit_order(symbol=SYMBOL, qty=TRADE_QUANTITY, side="sell", type="limit", limit_price=take_profit, time_in_force="gtc")
                print(f"TAKE-PROFIT SET at ${take_profit}")

            except Exception as e:
                print(f"Error executing trade: {e}")

    elif action == "SELL":
        try:
            api.submit_order(symbol=SYMBOL, qty=TRADE_QUANTITY, side="sell", type="market", time_in_force="gtc")
            print("SELL ORDER EXECUTED")
        except Exception as e:
            print(f"Error executing trade: {e}")

def main():
    """Main trading loop that runs during market hours."""
    while True:
        if is_market_open():
            print("Market is open. Running trading strategy...")
            execute_trade("BUY")
            time.sleep(60)  # Check for new opportunities every minute
        else:
            print("Market is closed. Sleeping...")
            time.sleep(900)  # Sleep for 15 minutes before checking again

if __name__ == "__main__":
    main()
