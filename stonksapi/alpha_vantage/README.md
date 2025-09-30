# Alpha Vantage Module (stonksapi)

A comprehensive, type-safe Python wrapper for the Alpha Vantage API with Pydantic models.

**Part of the `stonksapi` package.**

## Features

- ✅ **Strongly Typed**: Full Pydantic model support for all API responses
- ✅ **Comprehensive Coverage**: Stocks, Forex, Crypto, Technical Indicators, Fundamentals
- ✅ **Easy to Use**: Clean, intuitive API with excellent IDE autocomplete
- ✅ **Well Documented**: Extensive docstrings and examples
- ✅ **Production Ready**: Built on top of the official alpha-vantage library

## Installation

This package is part of the `stonksapi` package. Install it with:

```bash
uv add alpha-vantage pydantic
```

## Quick Start

### 1. Get Your API Key

Get a free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).

### 2. Basic Usage

```python
from alpha_vantage import AlphaVantageClient

# Initialize client (API key from environment or parameter)
client = AlphaVantageClient(api_key="your_api_key")

# Get real-time quote
quote = client.get_quote("AAPL")
print(f"Current Price: ${quote.global_quote.price}")
print(f"Change: {quote.global_quote.change_percent}")
```

## Examples

### Stock Data

#### Get Intraday Data

```python
from stonksapi.alpha_vantage import AlphaVantageClient, Interval, OutputSize

client = AlphaVantageClient()

# Get 5-minute intraday data
data = client.get_intraday(
    symbol="AAPL",
    interval=Interval.MIN_5,
    outputsize=OutputSize.COMPACT
)

# Access the data with full type safety
print(f"Symbol: {data.meta_data.symbol}")
for timestamp, ohlcv in list(data.time_series.items())[:5]:
    print(f"{timestamp}:")
    print(f"  Open: ${ohlcv.open}")
    print(f"  High: ${ohlcv.high}")
    print(f"  Low: ${ohlcv.low}")
    print(f"  Close: ${ohlcv.close}")
    print(f"  Volume: {ohlcv.volume:,}")
```

#### Get Daily Data

```python
# Get daily data (compact = last 100 days)
daily = client.get_daily("MSFT", outputsize=OutputSize.COMPACT)

# Get adjusted daily data (includes splits and dividends)
adjusted = client.get_daily_adjusted("MSFT")

for date, data in list(adjusted.time_series.items())[:5]:
    print(f"{date}:")
    print(f"  Close: ${data.close}")
    print(f"  Adjusted Close: ${data.adjusted_close}")
    if data.dividend_amount:
        print(f"  Dividend: ${data.dividend_amount}")
```

#### Get Weekly/Monthly Data

```python
# Get weekly data
weekly = client.get_weekly("GOOGL")
print(f"Total weeks of data: {len(weekly.time_series)}")

# Get monthly data
monthly = client.get_monthly("GOOGL")
print(f"Total months of data: {len(monthly.time_series)}")
```

### Symbol Search

```python
# Search for symbols
results = client.search_symbols("Apple")

for match in results.best_matches[:5]:
    print(f"{match.symbol}: {match.name}")
    print(f"  Type: {match.type}")
    print(f"  Region: {match.region}")
    print(f"  Match Score: {match.match_score}")
```

### Fundamental Data

#### Company Overview

```python
# Get comprehensive company information
overview = client.get_company_overview("AAPL")

print(f"Company: {overview.name}")
print(f"Sector: {overview.sector}")
print(f"Industry: {overview.industry}")
print(f"Market Cap: ${overview.market_capitalization}")
print(f"P/E Ratio: {overview.pe_ratio}")
print(f"EPS: ${overview.eps}")
print(f"Dividend Yield: {overview.dividend_yield}")
print(f"52-Week High: ${overview.week_52_high}")
print(f"52-Week Low: ${overview.week_52_low}")

# All fields are strongly typed with IDE autocomplete!
```

#### Earnings Data

```python
# Get earnings data
earnings = client.get_earnings("AAPL")

print("Quarterly Earnings:")
for quarter in earnings.quarterly_earnings[:4]:
    print(f"{quarter.fiscal_date_ending}:")
    print(f"  Reported EPS: ${quarter.reported_eps}")
    print(f"  Estimated EPS: ${quarter.estimated_eps}")
    print(f"  Surprise: {quarter.surprise_percentage}%")

print("\nAnnual Earnings:")
for year in earnings.annual_earnings[:5]:
    print(f"{year.fiscal_date_ending}: EPS ${year.reported_eps}")
```

### Foreign Exchange (Forex)

#### Real-time Exchange Rate

```python
# Get current exchange rate
rate = client.get_currency_exchange_rate("USD", "EUR")
exchange = rate.realtime_currency_exchange_rate

print(f"1 {exchange.from_currency_code} = {exchange.exchange_rate} {exchange.to_currency_code}")
print(f"Bid: {exchange.bid_price}")
print(f"Ask: {exchange.ask_price}")
print(f"Last Refreshed: {exchange.last_refreshed}")
```

#### Forex Time Series

```python
# Get intraday forex data
forex_data = client.get_forex_intraday(
    from_symbol="EUR",
    to_symbol="USD",
    interval=Interval.MIN_5
)

for timestamp, ohlc in list(forex_data.time_series.items())[:10]:
    print(f"{timestamp}: {ohlc.close}")
```

### Cryptocurrency

#### Crypto Intraday Data

```python
# Get Bitcoin intraday data
crypto = client.get_crypto_intraday("BTC", market="USD")

print(f"Latest Bitcoin prices:")
for timestamp, data in list(crypto.time_series.items())[:5]:
    print(f"{timestamp}:")
    print(f"  Price: ${data.close}")
    print(f"  Volume: {data.volume}")
```

#### Crypto Daily Data

```python
# Get daily crypto data
btc_daily = client.get_crypto_daily("BTC", market="USD")
eth_daily = client.get_crypto_daily("ETH", market="USD")

print(f"BTC latest: ${list(btc_daily.time_series.values())[0].close}")
print(f"ETH latest: ${list(eth_daily.time_series.values())[0].close}")
```

### Technical Indicators

#### Simple Moving Average (SMA)

```python
# Get 20-day SMA
sma = client.get_sma("AAPL", time_period=20)

print("20-Day SMA:")
for timestamp, values in list(sma.technical_analysis.items())[:10]:
    print(f"{timestamp}: {values['SMA']}")
```

#### Exponential Moving Average (EMA)

```python
# Get 12-day EMA
ema = client.get_ema("AAPL", time_period=12)

print("12-Day EMA:")
for timestamp, values in list(ema.technical_analysis.items())[:10]:
    print(f"{timestamp}: {values['EMA']}")
```

#### Relative Strength Index (RSI)

```python
# Get RSI (default 14 periods)
rsi = client.get_rsi("AAPL")

print("RSI Values:")
for timestamp, values in list(rsi.technical_analysis.items())[:10]:
    rsi_value = float(values['RSI'])
    signal = "Overbought" if rsi_value > 70 else "Oversold" if rsi_value < 30 else "Neutral"
    print(f"{timestamp}: RSI={rsi_value:.2f} ({signal})")
```

#### MACD

```python
# Get MACD
macd = client.get_macd("AAPL")

print("MACD Values:")
for timestamp, values in list(macd.technical_analysis.items())[:10]:
    print(f"{timestamp}:")
    print(f"  MACD: {values['MACD']}")
    print(f"  Signal: {values['MACD_Signal']}")
    print(f"  Histogram: {values['MACD_Hist']}")
```

#### Bollinger Bands

```python
# Get Bollinger Bands
bbands = client.get_bbands("AAPL", time_period=20)

print("Bollinger Bands:")
for timestamp, values in list(bbands.technical_analysis.items())[:10]:
    print(f"{timestamp}:")
    print(f"  Upper: {values['Real Upper Band']}")
    print(f"  Middle: {values['Real Middle Band']}")
    print(f"  Lower: {values['Real Lower Band']}")
```

## Environment Variables

You can set your API key as an environment variable instead of passing it directly:

```bash
export ALPHA_VANTAGE_API_KEY="your_api_key"
```

Then initialize the client without parameters:

```python
client = AlphaVantageClient()  # Reads from environment
```

## Type Safety

All responses are fully typed with Pydantic models, giving you:

- **IDE Autocomplete**: Your IDE knows all available fields
- **Type Checking**: Catch errors before runtime
- **Validation**: Automatic data validation from API responses
- **Documentation**: Inline documentation for all fields

```python
# Your IDE will show you all available fields!
quote = client.get_quote("AAPL")
price = quote.global_quote.price  # Decimal type
volume = quote.global_quote.volume  # int type
change = quote.global_quote.change_percent  # str type
```

## Available Intervals

```python
from alpha_vantage import Interval

Interval.MIN_1   # 1 minute
Interval.MIN_5   # 5 minutes
Interval.MIN_15  # 15 minutes
Interval.MIN_30  # 30 minutes
Interval.MIN_60  # 60 minutes
```

## Available Output Sizes

```python
from alpha_vantage import OutputSize

OutputSize.COMPACT  # Last 100 data points
OutputSize.FULL     # Full historical data
```

## API Rate Limits

Alpha Vantage free tier includes:

- **5 API calls per minute**
- **100 API calls per day**

Consider upgrading to a premium plan for higher limits if needed.

## Error Handling

```python
from alpha_vantage import AlphaVantageClient
from pydantic import ValidationError

try:
    client = AlphaVantageClient(api_key="your_api_key")
    quote = client.get_quote("AAPL")
    print(f"Price: ${quote.global_quote.price}")
    
except ValueError as e:
    print(f"Configuration error: {e}")
    
except ValidationError as e:
    print(f"Data validation error: {e}")
    
except Exception as e:
    print(f"API error: {e}")
```

## Advanced Usage

### Custom Response Processing

```python
# Get raw data and process with Pydantic model
data = client.get_daily("AAPL")

# Convert to pandas DataFrame
import pandas as pd

df = pd.DataFrame([
    {
        "date": date,
        "open": float(ohlcv.open),
        "high": float(ohlcv.high),
        "low": float(ohlcv.low),
        "close": float(ohlcv.close),
        "volume": ohlcv.volume,
    }
    for date, ohlcv in data.time_series.items()
])

print(df.head())
```

### Batch Processing

```python
# Get data for multiple symbols
symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]

quotes = {}
for symbol in symbols:
    try:
        quote = client.get_quote(symbol)
        quotes[symbol] = {
            "price": float(quote.global_quote.price),
            "change": quote.global_quote.change_percent,
            "volume": quote.global_quote.volume,
        }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

# Display results
for symbol, data in quotes.items():
    print(f"{symbol}: ${data['price']:.2f} ({data['change']})")
```

## Contributing

This package is part of the larger `stonksapi` project. See the main README for contribution guidelines.

## License

This package follows the license of the parent `stonksapi` project.

## Support

- **Documentation**: https://www.alphavantage.co/documentation/
- **API Key**: https://www.alphavantage.co/support/#api-key
- **Issues**: Please report issues in the main stonksapi repository

## Additional Resources

- [Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
