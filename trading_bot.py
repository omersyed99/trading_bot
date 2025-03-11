from config import api, SYMBOL, TRADE_QUANTITY, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT
from market_utils import is_market_open, get_market_data
from stable_baselines3 import DQN
import numpy as np
import time

# Load trained AI model
model = DQN.load("spxl_trained_model.zip")

def execute_trade(action):
    """Executes buy or sell orders with stop-loss & take-profit."""
    price = get_market_data()[0]  # Extract stock price from observation
    if price == 0:
        print("No market data. Skipping trade.")
        return

    stop_loss = round(price * (1 - STOP_LOSS_PERCENT), 2)
    take_profit = round(price * (1 + TAKE_PROFIT_PERCENT), 2)

    if action == 1:
        try:
            api.submit_order(symbol=SYMBOL, qty=TRADE_QUANTITY, side="buy", type="market", time_in_force="gtc")
            print(f"BUY ORDER EXECUTED at ${price}")

            api.submit_order(symbol=SYMBOL, qty=TRADE_QUANTITY, side="sell", type="stop", stop_price=stop_loss, time_in_force="gtc")
            print(f"STOP-LOSS SET at ${stop_loss}")

            api.submit_order(symbol=SYMBOL, qty=TRADE_QUANTITY, side="sell", type="limit", limit_price=take_profit, time_in_force="gtc")
            print(f"TAKE-PROFIT SET at ${take_profit}")

        except Exception as e:
            print(f"Error executing trade: {e}")

    elif action == 2:
        try:
            api.submit_order(symbol=SYMBOL, qty=TRADE_QUANTITY, side="sell", type="market", time_in_force="gtc")
            print("SELL ORDER EXECUTED")
        except Exception as e:
            print(f"Error executing trade: {e}")

while True:
    if is_market_open():
        obs = get_market_data()
        action, _ = model.predict(obs)
        execute_trade(action)

    time.sleep(60)  # Wait 1 minute before checking again
