#!/bin/bash
echo "Starting trading bot..."
cd /home/ec2-user/trading-bot
source /home/ec2-user/.bashrc
python3 trading_bot.py > trading_log.txt 2>&1 &
echo "Trading bot started."
