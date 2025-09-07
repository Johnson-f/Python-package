# MarketData Providers

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive Python package for fetching market data from multiple financial data providers with intelligent failover, caching, and standardized data models.

## 🚀 Features

### 📊 Multi-Provider Support
- **Alpha Vantage**: Real-time and historical stock data, technical indicators
- **Finnhub**: Comprehensive market data, company fundamentals, news
- **Polygon**: High-quality market data, options chains, economic indicators
- **Twelve Data**: International markets, forex, cryptocurrency data
- **Financial Modeling Prep**: Detailed fundamental analysis, SEC filings
- **Tiingo**: EOD prices, news, fundamental data
- **API Ninjas**: Economic indicators, motivational quotes
- **FRED**: Federal Reserve economic data
- **News APIs**: NewsAPI, Currents API, MediaStack, GNews
- **Yahoo Finance**: Broad market coverage (optional)

### 🧠 Intelligent Data Management
- **Auto-Failover**: Seamless switching between providers when one fails
- **Rate Limit Management**: Automatic handling of API rate limits
- **Data Standardization**: Consistent data models across all providers
- **Caching System**: Built-in caching to minimize API calls
- **Error Handling**: Comprehensive error classification and recovery

### 📈 Data Types Supported
- Real-time quotes and historical prices
- Options chains and derivatives
- Company fundamentals and financial statements
- Economic indicators and calendar events
- Earnings data and analyst estimates
- News and sentiment analysis
- Technical indicators
- Market status and holidays

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install marketdata-providers
```

### From Source
```bash
git clone https://github.com/johnsonnifemi/marketdata-providers.git
cd marketdata-providers
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/johnsonnifemi/marketdata-providers.git
cd marketdata-providers
pip install -e ".[dev]"
```

## 🔧 Quick Start

### 1. Environment Setup

Create a `.env` file in your project root:

```env
# Required API Keys (get from respective providers)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
FINNHUB_API_KEY=your_finnhub_key
POLYGON_API_KEY=your_polygon_key
TWELVE_DATA_API_KEY=your_twelve_data_key
FMP_API_KEY=your_fmp_key
TIINGO_API_KEY=your_tiingo_key

# Optional API Keys
API_NINJAS_API_KEY=your_api_ninjas_key
FRED_API_KEY=your_fred_key
NEWSAPI_KEY=your_newsapi_key
CURRENTS_API_KEY=your_currents_key
MEDIASTACK_API_KEY=your_mediastack_key
GNEWS_API_KEY=your_gnews_key
```

### 2. Basic Usage

```python
import asyncio
from marketdata_providers import MarketDataBrain

async def main():
    # Initialize the brain (automatically configures all providers)
    brain = MarketDataBrain()
    
    # Get a stock quote with automatic provider selection and failover
    result = await brain.get_quote("AAPL")
    
    if result.success:
        quote = result.data
        print(f"AAPL: ${quote.price} ({quote.change_percent:+.2f}%)")
        print(f"Provider: {quote.provider}")
    else:
        print(f"Error: {result.error}")
    
    # Get historical data
    historical_result = await brain.get_historical(
        "TSLA", 
        start_date="2024-01-01", 
        end_date="2024-12-31"
    )
    
    if historical_result.success:
        prices = historical_result.data
        print(f"Retrieved {len(prices)} historical records")
    
    # Get company information
    company_result = await brain.get_company_info("GOOGL")
    if company_result.success:
        company = company_result.data
        print(f"{company.name}: {company.description[:100]}...")

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Advanced Usage

```python
import asyncio
from datetime import date, timedelta
from marketdata_providers import MarketDataBrain, MarketDataConfig

async def advanced_example():
    # Custom configuration
    config = MarketDataConfig()
    config.cache_enabled = True
    config.cache_ttl_seconds = 300  # 5 minutes
    
    brain = MarketDataBrain(config=config)
    
    # Batch processing
    symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
    quotes = await brain.get_multiple_quotes(symbols)
    
    for symbol, result in quotes.items():
        if result.success:
            quote = result.data
            print(f"{symbol}: ${quote.price:,.2f}")
        else:
            print(f"{symbol}: Error - {result.error}")
    
    # Options chain
    options_result = await brain.get_options_chain("AAPL")
    if options_result.success:
        options = options_result.data
        print(f"Found {len(options)} option contracts")
    
    # Economic events
    events_result = await brain.get_economic_events(
        countries=["US"], 
        importance=3,  # High importance only
        limit=10
    )
    
    if events_result.success:
        events = events_result.data
        for event in events:
            print(f"{event.event_name}: {event.actual} (forecast: {event.forecast})")

if __name__ == "__main__":
    asyncio.run(advanced_example())
```

## 🏗️ Architecture

### MarketDataBrain
The central orchestrator that manages all providers:
- Automatic provider selection based on data type and availability
- Intelligent failover when providers fail or hit rate limits
- Built-in caching and performance optimization
- Comprehensive error handling and logging

### Data Models
All data is returned using standardized Pydantic models:
- `StockQuote`: Real-time stock prices and metrics
- `HistoricalPrice`: Historical price data with OHLCV
- `OptionQuote`: Options pricing and Greeks
- `CompanyInfo`: Fundamental company information
- `EconomicEvent`: Economic calendar events
- `NewsArticle`: Financial news and sentiment

### Provider System
Each provider is implemented as a separate class inheriting from `MarketDataProvider`:
- Consistent interface across all providers
- Built-in rate limiting and error handling
- Automatic data validation and transformation
- Provider-specific optimizations

## 🛠️ Configuration

### Provider Priorities
Configure provider preferences in your environment:

```python
from marketdata_providers import MarketDataConfig, ProviderPriority

config = MarketDataConfig()
config.finnhub.priority = ProviderPriority.HIGH
config.polygon.priority = ProviderPriority.HIGH
config.alpha_vantage.priority = ProviderPriority.LOW
```

### Rate Limiting
Each provider has automatic rate limiting:
- Free tier limits are pre-configured
- Automatic backoff when limits are reached
- Provider rotation to maximize throughput

### Caching
Built-in caching system:
```python
config = MarketDataConfig()
config.cache_enabled = True
config.cache_ttl_seconds = 300  # 5 minutes
config.max_cache_size = 1000    # Maximum cached items
```

## 📊 Supported Data Types

| Data Type | Providers | Description |
|-----------|-----------|-------------|
| Real-time Quotes | All | Current stock prices, volume, change |
| Historical Prices | All | OHLCV data with adjustments |
| Options Chains | Polygon, Finnhub | Options pricing and Greeks |
| Company Info | Multiple | Fundamentals, financials, metrics |
| Economic Events | API Ninjas, FRED | Economic calendar and indicators |
| Earnings Data | FMP, Finnhub | Earnings reports and estimates |
| News & Sentiment | News APIs | Financial news with sentiment |
| Technical Indicators | Alpha Vantage | RSI, MACD, moving averages |

## 🔒 Error Handling

The package provides comprehensive error handling:

```python
from marketdata_providers import MarketDataBrain

async def error_handling_example():
    brain = MarketDataBrain()
    
    result = await brain.get_quote("INVALID_SYMBOL")
    
    if not result.success:
        print(f"Error Type: {result.error_type}")
        print(f"Error Message: {result.error}")
        print(f"Provider Used: {result.provider_used}")
        print(f"Providers Tried: {result.providers_tried}")
```

Error types include:
- `INVALID_SYMBOL`: Symbol not found
- `RATE_LIMIT`: API rate limit exceeded  
- `API_ERROR`: Provider API error
- `NETWORK_ERROR`: Connection issues
- `VALIDATION_ERROR`: Data validation failed

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest test/test_brain.py -v
```

## 📈 Performance

### Benchmarks
- Average response time: 200-500ms per request
- Cache hit ratio: 85%+ with proper configuration
- Concurrent request support: 50+ simultaneous requests
- Memory usage: ~50MB baseline + cache

### Optimization Tips
1. Enable caching for frequently accessed data
2. Use batch requests when possible
3. Configure provider priorities based on your needs
4. Monitor rate limits and adjust request patterns

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/johnsonnifemi/marketdata-providers.git
cd marketdata-providers
pip install -e ".[dev]"
pre-commit install
```

### Code Style
We use:
- [Black](https://github.com/psf/black) for code formatting
- [isort](https://github.com/PyCQA/isort) for import sorting
- [flake8](https://github.com/PyCQA/flake8) for linting
- [mypy](https://github.com/python/mypy) for type checking

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- All the financial data providers for their excellent APIs
- The Python community for amazing libraries like `aiohttp` and `pydantic`
- Contributors and users who help improve this package

## 🔗 Links

- [Documentation](https://github.com/johnsonnifemi/marketdata-providers#readme)
- [PyPI Package](https://pypi.org/project/marketdata-providers/)
- [Issue Tracker](https://github.com/johnsonnifemi/marketdata-providers/issues)
- [Changelog](CHANGELOG.md)

---

Made with ❤️ for the financial data community