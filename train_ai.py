import pandas as pd
import numpy as np
import gym
from gym import spaces
from stable_baselines3 import PPO  # Using PPO instead of DQN (supports Discrete(3))
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.monitor import Monitor
import os
from trading_bot import SPXLTradingEnv


# ✅ Load Data
print("📊 Loading SPXL stock data...")
file_path = "spxl_data.csv"  # Ensure this file exists
df = pd.read_csv(file_path)

# ✅ Process Data
print("🔄 Processing data...")
df.rename(columns={
    "Date": "Date",
    "Close/Last": "Close",
    "Open": "Open",
    "High": "High",
    "Low": "Low",
    "Volume": "Volume"
}, inplace=True)

# Convert Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
df.set_index('Date', inplace=True)

# Convert numeric columns to float
df['Close'] = df['Close'].astype(float)
df['Open'] = df['Open'].astype(float)
df['High'] = df['High'].astype(float)
df['Low'] = df['Low'].astype(float)
df['Volume'] = df['Volume'].astype(int)

# ✅ Add Technical Indicators
df['SMA_50'] = df['Close'].rolling(window=50).mean()
df['SMA_200'] = df['Close'].rolling(window=200).mean()
df['RSI'] = 100 - (100 / (1 + df['Close'].pct_change().rolling(14).mean() / df['Close'].pct_change().rolling(14).std()))
df['ATR'] = df['High'].rolling(14).max() - df['Low'].rolling(14).min()

# Drop rows with NaN values
df.dropna(inplace=True)
df.to_csv("spxl_data_updated.csv")  # Save cleaned data
print("✅ Data processed & saved as 'spxl_data_updated.csv'")

# ✅ Define Trading Environment
class SPXLTradingEnv(gym.Env):
    def __init__(self, df):
        super(SPXLTradingEnv, self).__init__()

        self.df = df
        self.current_step = 0
        self.balance = 100000  # Starting cash
        self.shares_held = 0
        self.total_profit = 0

        # ✅ Use PPO-compatible action space (Buy, Sell, Hold)
        self.action_space = spaces.Discrete(3)  # 0 = Hold, 1 = Buy, 2 = Sell

        # ✅ Observation space: [Close, SMA_50, SMA_200, RSI, ATR]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(5,), dtype=np.float32)

    def _next_observation(self):
        """Return the next observation"""
        return np.array([
            self.df.iloc[self.current_step]['Close'],
            self.df.iloc[self.current_step]['SMA_50'],
            self.df.iloc[self.current_step]['SMA_200'],
            self.df.iloc[self.current_step]['RSI'],
            self.df.iloc[self.current_step]['ATR']
        ])

    def _take_action(self, action):
        """Execute the given action"""
        if action == 1:  # Buy
            self.shares_held += 1
        elif action == 2 and self.shares_held > 0:  # Sell
            self.shares_held -= 1

    def step(self, action):
        """Execute one step in the environment"""
        self._take_action(action)
        self.current_step += 1

        if self.current_step >= len(self.df) - 1:
            done = True
        else:
            done = False

        obs = self._next_observation()
        reward = self.df.iloc[self.current_step]['Close'] - self.df.iloc[self.current_step - 1]['Close']  # Reward based on price change

        return obs, reward, done, False, {}

    def reset(self, seed=None, options=None):
        """Reset environment"""
        self.current_step = 0
        return self._next_observation(), {}


# ✅ Train the AI Model
print("🚀 Training AI model...")

env = DummyVecEnv([lambda: Monitor(SPXLTradingEnv(df))])
model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.0005, n_steps=2048)

model.learn(total_timesteps=100000)

# ✅ Save the trained model
model.save("spxl_trained_model")
print("🎉 Training complete! Model saved as 'spxl_trained_model'.")
