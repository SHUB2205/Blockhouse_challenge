# Blockhouse_challenge

# TWAP Strategy Backtesting Simulator

A Python implementation of a basic backtesting framework focused on Time-Weighted Average Price (TWAP) execution strategy.

## Implementation Approach

### Core Components

1. **Order Book Simulation**
```python
class OrderBook:
    def __init__(self, initial_mid_price, avg_spread=0.02, volatility=0.0002):
        self.mid_price = initial_mid_price
        self.avg_spread = avg_spread
        self.volatility = volatility
```
- Simulates market microstructure using random walk for price evolution
- Models bid-ask spread with normal distribution
- Allows configuration of volatility and average spread

2. **TWAP Strategy**
```python
class TWAPStrategy:
    def __init__(self, order_size, start_time, end_time, n_slices):
        self.total_size = order_size
        self.slice_size = order_size / n_slices
        self.time_points = [
            start_time + timedelta(seconds=i * total_seconds / n_slices)
            for i in range(n_slices)
        ]
```
- Divides order into equal-sized child orders
- Schedules executions at regular intervals
- Maintains execution timeline

3. **Market Data Generation**
```python
def simulate_market(order_book, start_time, end_time, interval_seconds=1):
    # Generate synthetic data with realistic properties
    prices = order_book.get_prices(current_time)
    volume = np.random.exponential(100)  # Random volume
```
- Creates synthetic time series of prices and volumes
- Uses exponential distribution for volumes
- Maintains temporal consistency

4. **Trade Execution**
```python
def execute_twap(strategy, market_data, slippage_std=0.0001):
    # Execute strategy and record trades
    slippage = np.random.normal(0, slippage_std)
    executed_price = market_snapshot['ask'] * (1 + slippage)
```
- Models execution with random slippage
- Records trade details and timing
- Tracks execution prices

### Performance Metrics

```python
def calculate_metrics(trades, market_data):
    # Calculate VWAP benchmark
    vwap = market_data['value'].sum() / market_data['volume'].sum()
    
    # Calculate execution metrics
    metrics = {
        'execution_cost_bps': (avg_exec_price/vwap - 1) * 10000,
        'avg_slippage_bps': trades['slippage'].mean() * 10000,
        'slippage_std_bps': trades['slippage'].std() * 10000
    }
```
- Uses VWAP as benchmark price
- Reports execution costs in basis points
- Analyzes slippage statistics

## Sample Results

For a 30-minute simulation with following parameters:
- Initial price: $100
- Order size: 1,000 units
- Number of TWAP slices: 6
- Average spread: 0.02%
- Volatility: 0.02%

Typical output:
```
Execution Results:
VWAP (benchmark): $100.1234
Average Execution Price: $100.1456
Execution Cost vs VWAP: 2.21 bps
Average Slippage: 0.95 bps
Slippage Std Dev: 0.87 bps
Total Volume Executed: 1000
```

## Usage

Run the simulator using:
```bash
python backtest_simulator.py
```

## Dependencies

- numpy
- pandas

## Key Features

1. **Realistic Market Simulation**
   - Random walk price evolution
   - Configurable volatility and spread
   - Volume generation using exponential distribution

2. **Flexible TWAP Implementation** 
   - Configurable number of slices
   - Adjustable execution window
   - Slippage modeling

3. **Comprehensive Metrics**
   - Implementation shortfall calculation
   - Slippage analysis
   - VWAP benchmark comparison

## Limitations

1. **Simplified Market Impact**
   - Does not model price impact of trades
   - Assumes infinite liquidity

2. **Basic Order Types**
   - Only implements market orders
   - No limit order functionality

3. **Single Venue**
   - No cross-venue execution
   - No venue selection logic