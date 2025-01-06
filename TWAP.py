import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class OrderBook:
    def __init__(self, initial_mid_price, avg_spread=0.02, volatility=0.0002):
        self.mid_price = initial_mid_price
        self.avg_spread = avg_spread
        self.volatility = volatility
    
    def get_prices(self, timestamp):
        # Simulate price movement with random walk
        noise = np.random.normal(0, self.volatility)
        self.mid_price *= (1 + noise)
        spread = np.random.normal(self.avg_spread, self.avg_spread/10)
        
        return {
            'bid': self.mid_price * (1 - spread/2),
            'ask': self.mid_price * (1 + spread/2),
            'mid': self.mid_price
        }

class TWAPStrategy:
    def __init__(self, order_size, start_time, end_time, n_slices):
        self.total_size = order_size
        self.start_time = start_time
        self.end_time = end_time
        self.n_slices = n_slices
        self.slice_size = order_size / n_slices
        
        # Calculate time points for slices
        total_seconds = (end_time - start_time).total_seconds()
        self.time_points = [
            start_time + timedelta(seconds=i * total_seconds / n_slices)
            for i in range(n_slices)
        ]

def simulate_market(order_book, start_time, end_time, interval_seconds=1):
    timestamps = []
    current_time = start_time
    
    prices_data = []
    volumes_data = []
    
    while current_time <= end_time:
        prices = order_book.get_prices(current_time)
        volume = np.random.exponential(100)  # Random volume with mean 100
        
        prices_data.append({
            'timestamp': current_time,
            'bid': prices['bid'],
            'ask': prices['ask'],
            'mid': prices['mid'],
            'volume': volume
        })
        
        current_time += timedelta(seconds=interval_seconds)
    
    return pd.DataFrame(prices_data)

def execute_twap(strategy, market_data, slippage_std=0.0001):
    trades = []
    
    for i, target_time in enumerate(strategy.time_points):
        # Find closest market data point
        market_snapshot = market_data.iloc[(market_data['timestamp'] - target_time).abs().argsort()[0]]
        
        # Simulate execution with random slippage
        slippage = np.random.normal(0, slippage_std)
        executed_price = market_snapshot['ask'] * (1 + slippage)
        
        trades.append({
            'timestamp': target_time,
            'size': strategy.slice_size,
            'price': executed_price,
            'mid_price': market_snapshot['mid'],
            'slippage': slippage
        })
    
    return pd.DataFrame(trades)

def calculate_metrics(trades, market_data):
    #Calculate execution metrics
    # Calculate VWAP from market data as benchmark
    market_data['value'] = market_data['mid'] * market_data['volume']
    vwap = market_data['value'].sum() / market_data['volume'].sum()
    
    # Calculate average execution price
    avg_exec_price = (trades['price'] * trades['size']).sum() / trades['size'].sum()
    
    # Calculate metrics
    metrics = {
        'vwap': vwap,
        'avg_execution_price': avg_exec_price,
        'execution_cost_bps': (avg_exec_price/vwap - 1) * 10000,  # In basis points
        'avg_slippage_bps': trades['slippage'].mean() * 10000,
        'slippage_std_bps': trades['slippage'].std() * 10000,
        'total_volume': trades['size'].sum()
    }
    
    return metrics

def main():
    # Simulation parameters
    initial_price = 100.0
    order_size = 1000
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=30)
    n_slices = 6  # Execute every 5 minutes
    
    # Initialize components
    order_book = OrderBook(initial_price)
    strategy = TWAPStrategy(order_size, start_time, end_time, n_slices)
    
    # Generate market data
    market_data = simulate_market(order_book, start_time, end_time)
    
    # Execute strategy
    trades = execute_twap(strategy, market_data)
    
    # Calculate and display metrics
    metrics = calculate_metrics(trades, market_data)
    
    print("\nExecution Results:")
    print(f"VWAP (benchmark): ${metrics['vwap']:.4f}")
    print(f"Average Execution Price: ${metrics['avg_execution_price']:.4f}")
    print(f"Execution Cost vs VWAP: {metrics['execution_cost_bps']:.2f} bps")
    print(f"Average Slippage: {metrics['avg_slippage_bps']:.2f} bps")
    print(f"Slippage Std Dev: {metrics['slippage_std_bps']:.2f} bps")
    print(f"Total Volume Executed: {metrics['total_volume']:.0f}")
    
    return market_data, trades, metrics

if __name__ == "__main__":
    market_data, trades, metrics = main()