#!/usr/bin/env python3
"""
Token Launch Radar - make.fun competition entry
Predict new token market cap for make.fun competition

Based on stock analysis experience (2330, NVDA, etc.)
"""

import json
from datetime import datetime

def calculate_rsi(prices, period=14):
    """Calculate RSI (Relative Strength Index)"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def get_market_regime(data):
    """Determine market regime"""
    if len(data) < 50:
        return {}
    
    latest = data.iloc[-1]
    prev = data.iloc[-50]
    
    # Trend
    trend = 'uptrend' if latest['close'] > prev['close'] else 'downtrend'
    
    # Momentum
    momentum = 'strong' if latest['MACD'] > latest['MACD_signal'] else 'weak'
    
    # Volatility
    vol = latest['Volatility'] / latest['close']
    vol_regime = 'high' if vol > 0.05 else 'low'
    
    return {
        'trend': trend,
        'momentum': momentum,
        'volatility': vol_regime,
        'current_price': latest['close']
    }

def generate_forecast(ticker, history):
    """Generate forecast for next 24 hours"""
    regime = get_market_regime(history)
    
    # Simple forecasting model
    last_price = history['close'].iloc[-1]
    
    # Expected return based on trend and momentum
    if regime['trend'] == 'uptrend' and regime['momentum'] == 'strong':
        expected_return = 0.02
    elif regime['trend'] == 'downtrend':
        expected_return = -0.02
    else:
        expected_return = 0.005
    
    # Volatility-based confidence
    volatility = history['Volatility'].iloc[-1] / last_price
    confidence = max(0.3, min(0.9, 1.0 - volatility * 10))
    
    return {
        'symbol': ticker,
        'current_price': last_price,
        'expected_return': expected_return,
        'confidence': confidence,
        'regime': regime,
        'forecast_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def main():
    """Main function"""
    # Fetch data (placeholder)
    test_data = [
        {'symbol': 'BTC', 'price': 65000, 'volume': 50000, 'market_cap': 1200000000000},
        {'symbol': 'ETH', 'price': 3500, 'volume': 100000, 'market_cap': 60000000000},
        {'symbol': 'SOL', 'price': 180, 'volume': 20000, 'market_cap': 8000000000},
    ]
    
    results = []
    for item in test_data:
        forecast = generate_forecast(item['symbol'], item)
        forecast['market_cap'] = item['market_cap']
        results.append(forecast)
    
    output = {
        'timestamp': datetime.now().isoformat(),
        'forecast': results,
        'strategy': 'make.fun competition entry based on stock analysis experience'
    }
    
    with open('/output/forecast.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("Forecast generated successfully!")
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
