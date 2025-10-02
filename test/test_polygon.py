import os
import pytest
from unittest.mock import patch, MagicMock

from stonksapi.polygon.client import PolygonClient
from stonksapi.polygon.models import (
    TickerDetails,
    Aggregate,
    DailyOpenClose,
    LastQuote,
    NewsArticle,
    IndicatorValue,
    MACDValue,
    OptionContract,
    LastQuoteForOption,
    StockFinancial,
)
from typing import List

# Mock API Key
TEST_API_KEY = "test_polygon_api_key"


@pytest.fixture
def client():
    """Fixture for PolygonClient with a mocked RESTClient."""
    with patch("polygon.RESTClient") as mock_rest_client:
        client_instance = PolygonClient(api_key=TEST_API_KEY)
        client_instance._client = mock_rest_client.return_value
        yield client_instance


def test_client_initialization_with_api_key():
    """Test client initialization with a direct API key."""
    with patch("polygon.RESTClient"):
        client = PolygonClient(api_key=TEST_API_KEY)
        assert client.api_key == TEST_API_KEY


def test_client_initialization_with_env_variable(monkeypatch):
    """Test client initialization with an environment variable."""
    monkeypatch.setenv("POLYGON_API_KEY", TEST_API_KEY)
    with patch("polygon.RESTClient"):
        client = PolygonClient()
        assert client.api_key == TEST_API_KEY


def test_client_initialization_missing_api_key(monkeypatch):
    """Test that ValueError is raised if no API key is provided."""
    monkeypatch.delenv("POLYGON_API_KEY", raising=False)
    with pytest.raises(ValueError, match="API key must be provided"):
        PolygonClient()


def test_get_ticker_details(client):
    """Test the get_ticker_details method."""
    # Arrange
    mock_response = {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "market": "stocks",
        "locale": "us",
        "primary_exchange": "XNAS",
        "type": "CS",
        "active": True,
        "currency_name": "usd",
        "cik": "0000320193",
        "composite_figi": "BBG000B9XRY4",
        "share_class_figi": "BBG001S5N8V8",
        "last_updated_utc": "2024-01-01T00:00:00Z",
    }

    client._client.get_ticker_details.return_value = mock_response

    # Act
    ticker_details = client.get_ticker_details("AAPL")

    # Assert
    client._client.get_ticker_details.assert_called_once_with("AAPL")
    assert isinstance(ticker_details, TickerDetails)
    assert ticker_details.ticker == "AAPL"
    assert ticker_details.name == "Apple Inc."


def test_get_aggregates(client):
    """Test the get_aggregates method."""
    # Arrange
    mock_agg = {
        "o": 100,
        "h": 102,
        "l": 99,
        "c": 101,
        "v": 10000,
        "vw": 100.5,
        "t": 1672531200000,
        "n": 100,
    }

    client._client.get_aggs.return_value = [mock_agg]

    # Act
    aggregates = client.get_aggregates("AAPL", 1, "day", "2023-01-01", "2023-01-01")

    # Assert
    client._client.get_aggs.assert_called_once_with(
        "AAPL", 1, "day", "2023-01-01", "2023-01-01"
    )
    assert isinstance(aggregates, list)
    assert len(aggregates) == 1
    assert isinstance(aggregates[0], Aggregate)
    assert aggregates[0].open == 100


def test_get_daily_open_close(client):
    """Test the get_daily_open_close method."""
    # Arrange
    mock_response = {
        "status": "OK",
        "from": "2023-01-09",
        "symbol": "AAPL",
        "open": 130.47,
        "high": 133.41,
        "low": 129.89,
        "close": 130.15,
        "volume": 70790813,
        "afterHours": 130.2,
        "preMarket": 130.4,
    }
    client._client.get_daily_open_close.return_value = mock_response

    # Act
    daily_open_close = client.get_daily_open_close("AAPL", "2023-01-09")

    # Assert
    client._client.get_daily_open_close.assert_called_once_with("AAPL", "2023-01-09")
    assert isinstance(daily_open_close, DailyOpenClose)
    assert daily_open_close.symbol == "AAPL"
    assert daily_open_close.open == 130.47


def test_get_last_quote(client):
    """Test the get_last_quote method."""
    # Arrange
    mock_last = {
        "T": "AAPL",
        "S": 10,
        "P": 150.0,
        "X": 1,
        "s": 12,
        "p": 150.05,
        "x": 2,
        "t": 1672531200000,
    }

    mock_response = MagicMock()
    mock_response.last = mock_last

    client._client.get_last_quote.return_value = mock_response

    # Act
    last_quote = client.get_last_quote("AAPL")

    # Assert
    client._client.get_last_quote.assert_called_once_with("AAPL")
    assert isinstance(last_quote, LastQuote)
    assert last_quote.ticker == "AAPL"
    assert last_quote.bid_price == 150.0


def test_get_market_news(client):
    """Test the get_market_news method."""
    # Arrange
    mock_news = {
        "id": "some-id",
        "publisher": {"name": "The Motley Fool"},
        "title": "Some News Title",
        "author": "John Doe",
        "published_utc": "2024-01-01T00:00:00Z",
        "article_url": "https://www.fool.com/some-article",
        "tickers": ["AAPL"],
    }

    client._client.get_news.return_value = [mock_news]

    # Act
    news = client.get_market_news(limit=1)

    # Assert
    client._client.get_news.assert_called_once_with(limit=1)
    assert isinstance(news, list)
    assert len(news) == 1
    assert isinstance(news[0], NewsArticle)
    assert news[0].title == "Some News Title"


def test_get_sma(client):
    """Test the get_sma method."""
    # Arrange
    mock_value = {
        "timestamp": 1672531200000,
        "value": 150.0,
    }

    mock_response = MagicMock()
    mock_response.values = [mock_value]

    client._client.get_sma.return_value = mock_response

    # Act
    sma = client.get_sma("AAPL", "2023-01-01", "day", 14)

    # Assert
    client._client.get_sma.assert_called_once_with(
        "AAPL",
        timestamp="2023-01-01",
        timespan="day",
        window=14,
        series_type="close",
        expand_underlying=False,
    )
    assert isinstance(sma, list)
    assert len(sma) == 1
    assert isinstance(sma[0], IndicatorValue)
    assert sma[0].value == 150.0


def test_get_ema(client):
    """Test the get_ema method."""
    # Arrange
    mock_value = {
        "timestamp": 1672531200000,
        "value": 155.0,
    }

    mock_response = MagicMock()
    mock_response.values = [mock_value]

    client._client.get_ema.return_value = mock_response

    # Act
    ema = client.get_ema("AAPL", "2023-01-01", "day", 14)

    # Assert
    client._client.get_ema.assert_called_once_with(
        "AAPL",
        timestamp="2023-01-01",
        timespan="day",
        window=14,
        series_type="close",
        expand_underlying=False,
    )
    assert isinstance(ema, list)
    assert len(ema) == 1
    assert isinstance(ema[0], IndicatorValue)
    assert ema[0].value == 155.0


def test_get_macd(client):
    """Test the get_macd method."""
    # Arrange
    mock_value = {
        "timestamp": 1672531200000,
        "value": 1.0,
        "signal": 0.8,
        "histogram": 0.2,
    }

    mock_response = MagicMock()
    mock_response.values = [mock_value]

    client._client.get_macd.return_value = mock_response

    # Act
    macd = client.get_macd("AAPL", "2023-01-01", "day")

    # Assert
    client._client.get_macd.assert_called_once_with(
        "AAPL",
        timestamp="2023-01-01",
        timespan="day",
        short_window=12,
        long_window=26,
        signal_window=9,
        series_type="close",
        expand_underlying=False,
    )
    assert isinstance(macd, list)
    assert len(macd) == 1
    assert isinstance(macd[0], MACDValue)
    assert macd[0].value == 1.0


def test_get_rsi(client):
    """Test the get_rsi method."""
    # Arrange
    mock_value = {
        "timestamp": 1672531200000,
        "value": 70.0,
    }

    mock_response = MagicMock()
    mock_response.values = [mock_value]

    client._client.get_rsi.return_value = mock_response

    # Act
    rsi = client.get_rsi("AAPL", "2023-01-01", "day")

    # Assert
    client._client.get_rsi.assert_called_once_with(
        "AAPL",
        timestamp="2023-01-01",
        timespan="day",
        window=14,
        series_type="close",
        expand_underlying=False,
    )
    assert isinstance(rsi, list)
    assert len(rsi) == 1
    assert isinstance(rsi[0], IndicatorValue)
    assert rsi[0].value == 70.0


def test_list_option_contracts(client):
    """Test the list_option_contracts method."""
    # Arrange
    mock_contract = {
        "ticker": "O:AAPL240119C00150000",
        "underlying_ticker": "AAPL",
        "strike_price": 150.0,
        "expiration_date": "2024-01-19",
        "contract_type": "call",
    }

    client._client.list_options_contracts.return_value = [mock_contract]

    # Act
    options = client.list_option_contracts("AAPL")

    # Assert
    client._client.list_options_contracts.assert_called_once_with(
        underlying_ticker="AAPL", limit=1000
    )
    assert isinstance(options, list)
    assert len(options) == 1
    assert isinstance(options[0], OptionContract)
    assert options[0].ticker == "O:AAPL240119C00150000"


def test_get_last_quote_for_option(client):
    """Test the get_last_quote_for_option method."""
    # Arrange
    mock_last = {
        "ticker": "O:AAPL240119C00150000",
        "bid": 1.0,
        "bid_size": 10,
        "ask": 1.05,
        "ask_size": 12,
        "last_price": 1.02,
        "last_size": 1,
        "timestamp": 1672531200000,
    }

    mock_response = MagicMock()
    mock_response.last = mock_last

    client._client.get_last_quote_for_option_contract.return_value = mock_response

    # Act
    quote = client.get_last_quote_for_option("O:AAPL240119C00150000")

    # Assert
    client._client.get_last_quote_for_option_contract.assert_called_once_with(
        "O:AAPL240119C00150000"
    )
    assert isinstance(quote, LastQuoteForOption)
    assert quote.ticker == "O:AAPL240119C00150000"
    assert quote.last_price == 1.02


def test_get_stock_financials(client):
    """Test the get_stock_financials method."""
    # Arrange
    mock_financial = {
        "cik": "0000320193",
        "company_name": "Apple Inc.",
        "end_date": "2023-09-30",
        "filing_date": "2023-10-26",
        "financials": {
            "balance_sheet": {"equity": {"value": 1000}},
            "cash_flow_statement": {"net_cash_flow": {"value": 200}},
            "income_statement": {"revenues": {"value": 5000}},
            "comprehensive_income": {
                "comprehensive_income_loss": {"value": 100}
            },
        },
        "fiscal_period": "Q4",
        "fiscal_year": "2023",
        "source_filing_file_url": "some_url",
        "source_filing_url": "some_url",
        "start_date": "2023-07-01",
    }

    client._client.get_stock_financials.return_value = [mock_financial]

    # Act
    financials = client.get_stock_financials("AAPL")

    # Assert
    client._client.get_stock_financials.assert_called_once_with("AAPL", limit=100)
    assert isinstance(financials, list)
    assert len(financials) == 1
    assert isinstance(financials[0], StockFinancial)
    assert financials[0].company_name == "Apple Inc."