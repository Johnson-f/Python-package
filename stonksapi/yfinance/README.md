# Yahoo Finance Module (stonksapi)

A comprehensive, type-safe Python wrapper for the `yfinance` library with Pydantic models.


## Features

- **Type-safe**: All data is returned as Pydantic models with proper type annotations
- **Comprehensive**: Covers ALL yfinance functionality including advanced features
- **Easy to use**: Simple, intuitive API
- **Well-documented**: Full docstring coverage
- **Complete Coverage**: Earnings, analyst data, ESG, news, SEC filings, and more

## Installation

```bash
pip install yfinance pydantic
```

## Quick Start

```python
from stonksapi.yfinance import YFinanceClient

# Create a client
client = YFinanceClient()

# Get ticker information
info = client.get_ticker_info("AAPL")
print(f"Company: {info.long_name}")
print(f"Market Cap: ${info.market_cap:,}")
print(f"Sector: {info.sector}")

# Get fast info (key metrics quickly)
fast_info = client.get_fast_info("AAPL")
print(f"Last Price: ${fast_info.last_price}")
print(f"Market Cap: ${fast_info.market_cap:,}")

# Get historical data
history = client.get_history("AAPL", period="1mo")
for day in history:
    print(f"{day.date}: ${day.close:.2f}")

# Get earnings data
earnings = client.get_earnings("AAPL")
for earning in earnings:
    print(f"{earning.date}: Earnings ${earning.earnings}")

# Get analyst recommendations
recommendations = client.get_recommendations("AAPL")
for rec in recommendations:
    print(f"Strong Buy: {rec.strong_buy}, Buy: {rec.buy}, Hold: {rec.hold}")

# Get news
news = client.get_news("AAPL")
for article in news:
    print(f"{article.title} - {article.publisher}")
