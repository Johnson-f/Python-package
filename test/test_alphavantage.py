import os
import pytest
from unittest.mock import patch
from decimal import Decimal

from stonksapi.alpha_vantage.client import AlphaVantageClient, Interval, OutputSize
from stonksapi.alpha_vantage.models import (
    CompanyOverview,
    CryptoTimeSeries,
    DailyAdjustedTimeSeries,
    DailyTimeSeries,
    Earnings,
    ExchangeRateResponse,
    ForexTimeSeries,
    IntradayTimeSeries,
    MonthlyTimeSeries,
    QuoteResponse,
    SymbolSearchResponse,
    TechnicalIndicatorResponse,
    WeeklyTimeSeries,
)

# Mock API Key
TEST_API_KEY = "test_api_key"


@pytest.fixture
def client():
    """Fixture for AlphaVantageClient with mocked underlying library instances."""
    client_instance = AlphaVantageClient(api_key=TEST_API_KEY)
    with patch.object(client_instance, '_ts') as mock_ts, \
         patch.object(client_instance, '_fd') as mock_fd, \
         patch.object(client_instance, '_fx') as mock_fx, \
         patch.object(client_instance, '_crypto') as mock_crypto, \
         patch.object(client_instance, '_ti') as mock_ti:
        yield client_instance


def test_client_initialization_with_api_key():
    """Test client initialization with a direct API key."""
    client = AlphaVantageClient(api_key=TEST_API_KEY)
    assert client.api_key == TEST_API_KEY


def test_client_initialization_with_env_variable(monkeypatch):
    """Test client initialization with an environment variable."""
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", TEST_API_KEY)
    client = AlphaVantageClient()
    assert client.api_key == TEST_API_KEY


def test_client_initialization_missing_api_key(monkeypatch):
    """Test that ValueError is raised if no API key is provided."""
    monkeypatch.delenv("ALPHA_VANTAGE_API_KEY", raising=False)
    with pytest.raises(ValueError, match="API key must be provided"):
        AlphaVantageClient()


# ==================== Model Validator Tests ====================

def test_intraday_time_series_validator():
    """Test the custom validator for IntradayTimeSeries."""
    mock_data = {
        "Meta Data": {
            "1. Information": "Intraday (5min) open, high, low, close prices and volume",
            "2. Symbol": "IBM",
            "3. Last Refreshed": "2024-07-26 19:55:00",
            "4. Interval": "5min",
            "5. Output Size": "Compact",
            "6. Time Zone": "US/Eastern",
        },
        "Time Series (5min)": {
            "2024-07-26 19:55:00": {
                "1. open": "180.0000",
                "2. high": "180.0000",
                "3. low": "180.0000",
                "4. close": "180.0000",
                "5. volume": "100",
            }
        },
    }
    parsed = IntradayTimeSeries.model_validate(mock_data)
    assert isinstance(parsed, IntradayTimeSeries)
    assert "2024-07-26 19:55:00" in parsed.time_series
    assert parsed.time_series["2024-07-26 19:55:00"].close == Decimal("180.0000")


# ==================== Time Series Method Tests ====================


def test_get_intraday(client):
    """Test get_intraday method."""
    mock_data = {
        "Time Series (5min)": {
            "2024-07-26 20:00:00": {
                "1. open": "180.0", "2. high": "180.1", "3. low": "179.9", "4. close": "180.05", "5. volume": "1000"
            }
        }
    }
    mock_meta_data = {"2. Symbol": "IBM"}
    client._ts.get_intraday.return_value = (mock_data, mock_meta_data)
    
    result = client.get_intraday(symbol="IBM", interval=Interval.MIN_5)
    
    client._ts.get_intraday.assert_called_once_with(symbol="IBM", interval="5min", outputsize="compact")
    assert isinstance(result, IntradayTimeSeries)
    assert result.meta_data.symbol == "IBM"
    assert result.time_series["2024-07-26 20:00:00"].volume == 1000


def test_get_daily(client):
    """Test get_daily method."""
    mock_data = {
        "Time Series (Daily)": {
            "2024-07-26": {
                "1. open": "200.0", "2. high": "202.0", "3. low": "199.0", "4. close": "201.5", "5. volume": "50000000"
            }
        }
    }
    mock_meta_data = {"2. Symbol": "AAPL"}
    client._ts.get_daily.return_value = (mock_data, mock_meta_data)

    result = client.get_daily("AAPL")

    client._ts.get_daily.assert_called_once_with(symbol="AAPL", outputsize="compact")
    assert isinstance(result, DailyTimeSeries)
    assert result.meta_data.symbol == "AAPL"
    assert result.time_series["2024-07-26"].close == Decimal("201.5")

def test_get_quote(client):
    """Test get_quote method."""
    mock_quote_data = {
        "01. symbol": "AAPL", "02. open": "200.0", "03. high": "202.0", "04. low": "199.0",
        "05. price": "201.5", "06. volume": "50000000", "07. latest trading day": "2024-07-26",
        "08. previous close": "199.8", "09. change": "1.7", "10. change percent": "0.85%"
    }
    client._ts.get_quote_endpoint.return_value = (mock_quote_data, None)
    
    result = client.get_quote("AAPL")
    
    client._ts.get_quote_endpoint.assert_called_once_with(symbol="AAPL")
    assert isinstance(result, QuoteResponse)
    assert result.global_quote.symbol == "AAPL"
    assert result.global_quote.price == Decimal("201.5")


# ==================== Fundamental Data Method Tests ====================


def test_get_company_overview(client):
    """Test get_company_overview method."""
    mock_response = {"Symbol": "IBM", "Name": "International Business Machines Corporation", "PERatio": "20.5"}
    client._fd.get_company_overview.return_value = (mock_response, None)
    result = client.get_company_overview("IBM")
    client._fd.get_company_overview.assert_called_once_with(symbol="IBM")
    assert isinstance(result, CompanyOverview)
    assert result.symbol == "IBM"

# ==================== Forex Method Tests ====================

def test_get_currency_exchange_rate(client):
    """Test get_currency_exchange_rate method."""
    mock_exchange_data = {
        "1. From_Currency Code": "USD", "2. From_Currency Name": "United States Dollar",
        "3. To_Currency Code": "JPY", "4. To_Currency Name": "Japanese Yen",
        "5. Exchange Rate": "140.5", "6. Last Refreshed": "2024-07-27 10:00:00",
        "7. Time Zone": "UTC", "8. Bid Price": "140.49", "9. Ask Price": "140.51"
    }
    client._fx.get_currency_exchange_rate.return_value = (mock_exchange_data, None)
    
    result = client.get_currency_exchange_rate("USD", "JPY")
    
    client._fx.get_currency_exchange_rate.assert_called_once_with(from_currency="USD", to_currency="JPY")
    assert isinstance(result, ExchangeRateResponse)
    assert result.realtime_currency_exchange_rate.exchange_rate == Decimal("140.5")
    assert result.realtime_currency_exchange_rate.to_currency_code == "JPY"