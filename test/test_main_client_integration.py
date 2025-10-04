"""
Integration tests for the main StonksApiClient.
"""

import os
import time
import pytest
from dotenv import load_dotenv

from stonksapi.client import StonksApiClient
from stonksapi.models import TickerInfo, Quote, HistoricalData, NewsArticle, MarketMover

# Load environment variables
load_dotenv()

# API Keys
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

@pytest.fixture(scope="module")
def client():
    """Module-scoped fixture for the StonksApiClient."""
    return StonksApiClient(
        alpha_vantage_api_key=ALPHA_VANTAGE_API_KEY,
        finnhub_api_key=FINNHUB_API_KEY,
        polygon_api_key=POLYGON_API_KEY,
    )

@pytest.fixture(autouse=True)
def slow_down_tests():
    """Fixture to add a delay between each test to avoid rate limiting."""
    yield
    time.sleep(20) # 20-second delay between tests

# ==================== Test get_ticker_info ====================

def test_get_ticker_info_default(client: StonksApiClient):
    """Test get_ticker_info with the default source (yfinance)."""
    info = client.get_ticker_info("AAPL")
    assert isinstance(info, TickerInfo)
    assert info.symbol == "AAPL"
    assert info.source == "yfinance"

@pytest.mark.skipif(not ALPHA_VANTAGE_API_KEY, reason="ALPHA_VANTAGE_API_KEY not set")
def test_get_ticker_info_alpha_vantage(client: StonksApiClient):
    """Test get_ticker_info with alpha_vantage source."""
    info = client.get_ticker_info("IBM", source="alpha_vantage")
    assert isinstance(info, TickerInfo)
    assert info.symbol == "IBM"
    assert info.source == "alpha_vantage"

@pytest.mark.skipif(not FINNHUB_API_KEY, reason="FINNHUB_API_KEY not set")
def test_get_ticker_info_finnhub(client: StonksApiClient):
    """Test get_ticker_info with finnhub source."""
    info = client.get_ticker_info("MSFT", source="finnhub")
    assert isinstance(info, TickerInfo)
    assert info.symbol == "MSFT"
    assert info.source == "finnhub"

@pytest.mark.skipif(not POLYGON_API_KEY, reason="POLYGON_API_KEY not set")
def test_get_ticker_info_polygon(client: StonksApiClient):
    """Test get_ticker_info with polygon source."""
    info = client.get_ticker_info("GOOG", source="polygon")
    assert isinstance(info, TickerInfo)
    assert info.symbol == "GOOG"
    assert info.source == "polygon"

# ==================== Test get_quote ====================

def test_get_quote_auto_fallback(client: StonksApiClient):
    """Test get_quote with automatic fallback."""
    quote = client.get_quote("TSLA")
    assert isinstance(quote, Quote)
    assert quote.symbol == "TSLA"
    assert quote.price > 0

@pytest.mark.skipif(not FINNHUB_API_KEY, reason="FINNHUB_API_KEY not set")
def test_get_quote_finnhub(client: StonksApiClient):
    """Test get_quote with finnhub source."""
    quote = client.get_quote("NVDA", source="finnhub")
    assert isinstance(quote, Quote)
    assert quote.symbol == "NVDA"
    assert quote.source == "finnhub"

@pytest.mark.skipif(not ALPHA_VANTAGE_API_KEY, reason="ALPHA_VANTAGE_API_KEY not set")
def test_get_quote_alpha_vantage(client: StonksApiClient):
    """Test get_quote with alpha_vantage source."""
    quote = client.get_quote("IBM", source="alpha_vantage")
    assert isinstance(quote, Quote)
    assert quote.symbol == "IBM"
    assert quote.source == "alpha_vantage"

@pytest.mark.xfail(reason="Requires paid polygon plan")
@pytest.mark.skipif(not POLYGON_API_KEY, reason="POLYGON_API_KEY not set")
def test_get_quote_polygon(client: StonksApiClient):
    """Test get_quote with polygon source."""
    quote = client.get_quote("GOOG", source="polygon")
    assert isinstance(quote, Quote)
    assert quote.symbol == "GOOG"
    assert quote.source == "polygon"

def test_get_quote_finance_query(client: StonksApiClient):
    """Test get_quote with finance_query source."""
    quote = client.get_quote("F", source="finance_query")
    assert isinstance(quote, Quote)
    assert quote.symbol == "F"
    assert quote.source == "finance_query"

# ==================== Test get_historical_data ====================

def test_get_historical_data(client: StonksApiClient):
    """Test get_historical_data from finance_query."""
    history = client.get_historical_data("AMZN", range="1mo", interval="1d")
    assert isinstance(history, list)
    assert len(history) > 0
    assert isinstance(history[0], HistoricalData)
    assert history[0].source == "finance_query"

# ==================== Test get_market_movers ====================

def test_get_market_movers_actives(client: StonksApiClient):
    """Test get_market_movers with actives category."""
    movers = client.get_market_movers(category="actives")
    assert isinstance(movers, list)
    assert len(movers) > 0
    assert isinstance(movers[0], MarketMover)

def test_get_market_movers_gainers(client: StonksApiClient):
    """Test get_market_movers with gainers category."""
    movers = client.get_market_movers(category="gainers")
    assert isinstance(movers, list)
    assert len(movers) > 0
    assert isinstance(movers[0], MarketMover)

def test_get_market_movers_losers(client: StonksApiClient):
    """Test get_market_movers with losers category."""
    movers = client.get_market_movers(category="losers")
    assert isinstance(movers, list)
    assert len(movers) > 0
    assert isinstance(movers[0], MarketMover)

# ==================== Test get_market_news ====================

@pytest.mark.xfail(reason="Network flakiness")
def test_get_market_news_auto_fallback(client: StonksApiClient):
    """Test get_market_news with automatic fallback."""
    news = client.get_market_news("general")
    assert isinstance(news, list)
    if news:
        assert isinstance(news[0], NewsArticle)

@pytest.mark.skipif(not FINNHUB_API_KEY, reason="FINNHUB_API_KEY not set")
def test_get_market_news_finnhub(client: StonksApiClient):
    """Test get_market_news with finnhub source."""
    news = client.get_market_news(source="finnhub")
    assert isinstance(news, list)
    if news:
        assert isinstance(news[0], NewsArticle)
        assert news[0].provider == "finnhub"

@pytest.mark.xfail(reason="Rate limiting issues")
@pytest.mark.skipif(not POLYGON_API_KEY, reason="POLYGON_API_KEY not set")
def test_get_market_news_polygon(client: StonksApiClient):
    """Test get_market_news with polygon source."""
    news = client.get_market_news(source="polygon")
    assert isinstance(news, list)
    if news:
        assert isinstance(news[0], NewsArticle)
        assert news[0].provider == "polygon"

def test_get_market_news_finance_query(client: StonksApiClient):
    """Test get_market_news with finance_query source."""
    news = client.get_market_news("AAPL", source="finance_query")
    assert isinstance(news, list)
    if news:
        assert isinstance(news[0], NewsArticle)
        assert news[0].provider == "finance_query"

# ==================== Test Error Handling ====================

def test_get_ticker_info_missing_key(monkeypatch):
    """Test ValueError for get_ticker_info with missing API key."""
    monkeypatch.delenv("ALPHA_VANTAGE_API_KEY", raising=False)
    client = StonksApiClient(alpha_vantage_api_key=None)
    with pytest.raises(ValueError, match="API key must be provided"):
        client.get_ticker_info("IBM", source="alpha_vantage")

def test_get_quote_missing_key(monkeypatch):
    """Test ValueError for get_quote with missing API key."""
    monkeypatch.delenv("FINNHUB_API_KEY", raising=False)
    client = StonksApiClient(finnhub_api_key=None)
    with pytest.raises(ValueError, match="API key must be provided"):
        client.get_quote("NVDA", source="finnhub")

def test_get_market_news_missing_key(monkeypatch):
    """Test ValueError for get_market_news with missing API key."""
    monkeypatch.delenv("POLYGON_API_KEY", raising=False)
    client = StonksApiClient(polygon_api_key=None)
    with pytest.raises(ValueError, match="API key must be provided"):
        client.get_market_news(source="polygon")