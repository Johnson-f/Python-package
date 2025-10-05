# StonksAPI 📈

A unified Python library for fetching stock market data from multiple providers with a simple, consistent interface.

## 🚀 Features

- **Multiple Data Sources**: Integrate with YFinance, Alpha Vantage, Finnhub, Polygon.io, and Finance Query
- **Unified Interface**: Same methods work across different data providers
- **Automatic Fallbacks**: Smart switching between providers when API keys are unavailable
- **Type Safety**: Full Pydantic model validation for all data
- **Comprehensive Coverage**: Stock quotes, financial statements, news, market data, and more
- **Easy Setup**: Simple installation and configuration

## 📦 Installation

```bash
pip install stonksapi
```

Or for development:

```bash
git clone https://github.com/your-username/stonksapi.git
cd stonksapi
pip install -e .
```

## 🔑 API Keys Setup (Optional)

While StonksAPI works without API keys using free providers, you can enhance functionality by adding API keys:

```python
# Set environment variables
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
FINNHUB_API_KEY=your_finnhub_key  
POLYGON_API_KEY=your_polygon_key
```

Or pass them directly:

```python
from stonksapi import StonksApiClient

client = StonksApiClient(
    alpha_vantage_api_key="your_key",
    finnhub_api_key="your_key", 
    polygon_api_key="your_key"
)
```

## 🏁 Quick Start

```python
from stonksapi import StonksApiClient

# Initialize client (works without API keys)
client = StonksApiClient()

# Get stock quote
quote = client.get_quote("AAPL")
print(f"Apple stock price: ${quote.price}")

# Get historical data
history = client.get_historical_data("TSLA", range="1mo")
print(f"Got {len(history)} days of Tesla data")

# Get company information
info = client.get_ticker_info("MSFT")
print(f"Microsoft: {info.name} - {info.description}")
```

## 📊 Core Features

### Stock Quotes & Market Data

```python
# Real-time quotes
quote = client.get_quote("AAPL")
print(f"Price: ${quote.price}, Change: {quote.change_percent}%")

# Multiple quotes at once
quotes = client.get_fq_detailed_quotes(["AAPL", "GOOGL", "MSFT"])

# Market movers
gainers = client.get_market_movers("gainers")
losers = client.get_market_movers("losers") 
actives = client.get_market_movers("actives")
```

### Historical Data

```python
# Different time ranges
data_1d = client.get_historical_data("AAPL", range="1d", interval="1m")
data_1mo = client.get_historical_data("AAPL", range="1mo", interval="1d")
data_1yr = client.get_historical_data("AAPL", range="1y", interval="1d")

# Access OHLCV data
for day in data_1mo:
    print(f"{day.date}: Open=${day.open}, Close=${day.close}, Volume={day.volume}")
```

### Company Information

```python
# Basic company information
info = client.get_ticker_info("AAPL")
print(f"Company: {info.name}")
print(f"Sector: {info.sector}")  
print(f"Industry: {info.industry}")
print(f"Market Cap: {info.market_cap}")

# From different sources
info_yf = client.get_ticker_info("AAPL", source="yfinance")
info_av = client.get_ticker_info("AAPL", source="alpha_vantage")
```

### Financial Statements

```python
# Income statement
income = client.get_fq_income_statement("AAPL")
print(f"Total Revenue: {income.statement['0']['2024-09-30']}")

# Balance sheet  
balance = client.get_fq_balance_sheet("AAPL")

# Cash flow statement
cashflow = client.get_fq_cash_flow_statement("AAPL")

# Get quarterly vs annual data
quarterly_income = client.get_fq_income_statement("AAPL", frequency=Frequency.QUARTERLY)
annual_income = client.get_fq_income_statement("AAPL", frequency=Frequency.ANNUAL)
```

### News & Market Information

```python
# Stock-specific news
news = client.get_fq_stock_news("AAPL")
for article in news:
    print(f"{article.title} - {article.source}")

# General market news
market_news = client.get_market_news()

# From specific sources
finnhub_news = client.get_market_news(source="finnhub")
```

### Market Analysis

```python
# Sector performance
sectors = client.get_fq_all_sector_performance()
for sector in sectors:
    print(f"{sector.sector}: {sector.day_return} (day), {sector.year_return} (year)")

# Individual stock sector
apple_sector = client.get_fq_sector_performance("AAPL")

# Market indices
indices = client.get_fq_market_indices()
```

### Institutional Holdings

```python
# Major holders
major_holders = client.get_fq_major_holders("AAPL")

# Institutional holders
institutional = client.get_fq_institutional_holders("AAPL") 

# Insider transactions
insider_trans = client.get_fq_insider_transactions("AAPL")

# Unified holders analysis
all_holders = client.get_unified_holders_analysis("AAPL")
```

### Earnings & Transcripts

```python
# Earnings transcripts
transcript = client.get_fq_earnings_transcript("TSLA", quarter="Q3", year=2024)
print(transcript.transcripts[0].transcript[:500])  # First 500 chars

# YFinance earnings data
earnings = client.get_yf_earnings("AAPL")
```

## 🎯 Advanced Usage

### Multi-Source Data Comparison

```python
# Compare financial data from multiple sources
unified_financials = client.get_unified_financials("AAPL")
yf_data = unified_financials["yfinance"]
fq_data = unified_financials["finance_query"]

# Compare news from different sources  
unified_news = client.get_unified_news("AAPL")
```

### Error Handling

```python
try:
    quote = client.get_quote("INVALID_SYMBOL")
except Exception as e:
    print(f"Error fetching quote: {e}")

# Check API availability
if client.is_finnhub_available:
    news = client.get_market_news(source="finnhub")
else:
    news = client.get_market_news()  # Uses fallback
```

### Custom Configuration

```python
# Initialize with specific providers only
client = StonksApiClient(
    finnhub_api_key="your_key"  # Only Finnhub will be available
)

# Check which providers are available
print(f"Alpha Vantage: {client.is_alpha_vantage_available}")
print(f"Finnhub: {client.is_finnhub_available}")  
print(f"Polygon: {client.is_polygon_available}")
```

## 📋 Available Data Types

### Quote Data
- Real-time and delayed quotes
- Pre-market and after-hours pricing
- Price changes and percentage changes
- Trading volume and market cap

### Historical Data  
- Open, High, Low, Close, Volume (OHLCV)
- Adjustable time ranges and intervals
- Dividend and split adjusted data

### Fundamental Data
- Income statements (quarterly/annual)
- Balance sheets (quarterly/annual)  
- Cash flow statements (quarterly/annual)
- Key financial ratios

### Market Data
- Market movers (gainers, losers, most active)
- Sector performance
- Market indices (S&P 500, NASDAQ, etc.)
- Market hours and status

### News & Analysis
- Stock-specific news articles
- General market news
- Analyst recommendations
- Earnings transcripts

### Corporate Data
- Institutional holdings
- Insider transactions  
- Major shareholders
- Corporate actions (dividends, splits)

## 🔧 Data Sources

| Provider | Free Tier | API Key Required | Specialties |
|----------|-----------|------------------|-------------|
| **YFinance** | ✅ Yes | ❌ No | General stock data, financials |
| **Finance Query** | ✅ Yes | ❌ No | Real-time quotes, market data |
| **Alpha Vantage** | ⚠️ Limited | ✅ Yes | Technical indicators, forex |
| **Finnhub** | ⚠️ Limited | ✅ Yes | News, earnings, recommendations |
| **Polygon.io** | ⚠️ Limited | ✅ Yes | Real-time data, advanced analytics |

## 🚨 Rate Limits & Best Practices

- **Free APIs**: Respect rate limits (usually 5-100 requests/minute)
- **Batch Requests**: Use multi-symbol methods when available
- **Caching**: Cache responses for repeated requests
- **Error Handling**: Always handle API failures gracefully
- **API Keys**: Store keys securely in environment variables

## 🛠️ Development

```bash
# Clone the repository
git clone https://github.com/your-username/stonksapi.git
cd stonksapi

# Install in development mode
pip install -e .

# Run tests
pytest

# Run specific tests
pytest test/test_main_client_integration.py -v
```

## 📝 Examples

### Basic Trading Dashboard Data

```python
def get_portfolio_summary(symbols):
    client = StonksApiClient()
    
    portfolio = []
    for symbol in symbols:
        quote = client.get_quote(symbol)
        info = client.get_ticker_info(symbol)
        
        portfolio.append({
            'symbol': symbol,
            'name': info.name,
            'price': quote.price,
            'change': quote.change_percent,
            'sector': info.sector
        })
    
    return portfolio

# Usage
portfolio = get_portfolio_summary(['AAPL', 'GOOGL', 'TSLA', 'MSFT'])
for stock in portfolio:
    print(f"{stock['symbol']}: ${stock['price']} ({stock['change']}%)")
```

### Market Screener

```python
def screen_top_gainers():
    client = StonksApiClient()
    
    gainers = client.get_market_movers("gainers")
    
    # Filter for large companies (>$1B market cap)
    large_gainers = []
    for stock in gainers[:10]:  # Top 10
        try:
            info = client.get_ticker_info(stock.symbol)
            if info.market_cap and float(info.market_cap.replace('$', '').replace('B', '')) > 1:
                large_gainers.append({
                    'symbol': stock.symbol,
                    'name': stock.name,
                    'price': stock.price,
                    'change': stock.percent_change,
                    'market_cap': info.market_cap
                })
        except:
            continue
    
    return large_gainers
```

### Financial Analysis

```python
def analyze_financials(symbol):
    client = StonksApiClient()
    
    # Get latest financial data
    income = client.get_fq_income_statement(symbol)
    balance = client.get_fq_balance_sheet(symbol)
    
    # Extract key metrics
    latest_year = list(income.statement['0'].keys())[1]  # Skip 'Breakdown'
    revenue = income.statement['0'][latest_year]
    total_assets = balance.statement['0'][latest_year]
    
    return {
        'symbol': symbol,
        'revenue': revenue,
        'total_assets': total_assets,
        'year': latest_year
    }
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)  
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This library is for educational and research purposes. Not financial advice. Always verify data from multiple sources before making investment decisions.

## 🆘 Support

- 📧 Email: [your-email@example.com]
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/stonksapi/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/your-username/stonksapi/discussions)

---

**Happy Trading! 📈💰**