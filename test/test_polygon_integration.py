import os
import pytest
import time
from dotenv import load_dotenv
from stonksapi.polygon import PolygonClient
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
from datetime import date, timedelta

# Load environment variables from .env file
load_dotenv()

@pytest.fixture(scope="module")
def api_key() -> str:
    """Fixture to provide the Polygon API key and skip tests if it's not available."""
    key = os.getenv("POLYGON_API_KEY")
    if not key:
        pytest.skip("POLYGON_API_KEY environment variable not set, skipping integration tests.")
    return key

@pytest.fixture(scope="module")
def client(api_key: str) -> PolygonClient:
    """Fixture to create a PolygonClient instance for integration tests."""
    return PolygonClient(api_key=api_key)

# This test should run even without an API key.
def test_client_init_no_api_key():
    """Test that PolygonClient raises ValueError if no API key is provided."""
    original_key = os.environ.pop("POLYGON_API_KEY", None)
    try:
        with pytest.raises(ValueError, match="API key must be provided"):
            PolygonClient()
    finally:
        if original_key:
            os.environ["POLYGON_API_KEY"] = original_key

# --- Integration Tests (require API key) ---

@pytest.fixture(autouse=True)
def slow_down_tests():
    """Fixture to add a delay between each test to avoid rate limiting."""
    yield
    time.sleep(20) # 3 calls per minute

def test_get_ticker_details_integration(client: PolygonClient):
    """Tests get_ticker_details with a real API call."""
    details = client.get_ticker_details("AAPL")
    assert isinstance(details, TickerDetails)
    assert details.ticker == "AAPL"
    assert details.name == "Apple Inc."

def test_get_aggregates_integration(client: PolygonClient):
    """Tests get_aggregates with a real API call."""
    today = date.today()
    yesterday = today - timedelta(days=1)
    aggs = client.get_aggregates("AAPL", 1, "day", yesterday.isoformat(), today.isoformat())
    assert isinstance(aggs, list)
    if aggs:
        assert isinstance(aggs[0], Aggregate)

@pytest.mark.xfail(reason="Requires a paid plan with access to daily open/close data.")
def test_get_daily_open_close_integration(client: PolygonClient):
    """Tests get_daily_open_close with a real API call."""
    day = date.today() - timedelta(days=1)
    daily_oc = client.get_daily_open_close("AAPL", day.isoformat())
    assert isinstance(daily_oc, DailyOpenClose)
    assert daily_oc.symbol == "AAPL"

@pytest.mark.xfail(reason="Requires a paid plan with access to last quote data.")
def test_get_last_quote_integration(client: PolygonClient):
    """Tests get_last_quote with a real API call."""
    quote = client.get_last_quote("AAPL")
    assert isinstance(quote, LastQuote)
    assert quote.T == "AAPL"

@pytest.mark.xfail(reason="API is frequently rate-limiting this endpoint.")
def test_get_market_news_integration(client: PolygonClient):
    """Tests get_market_news with a real API call."""
    news = client.get_market_news(limit=5)
    assert isinstance(news, list)
    assert len(news) <= 5
    if news:
        assert isinstance(news[0], NewsArticle)

def test_get_sma_integration(client: PolygonClient):
    """Tests get_sma with a real API call."""
    sma = client.get_sma("AAPL", timespan="day", window=20, timestamp_lt=date.today().isoformat())
    assert isinstance(sma, list)
    if sma:
        assert isinstance(sma[0], IndicatorValue)

def test_get_ema_integration(client: PolygonClient):
    """Tests get_ema with a real API call."""
    ema = client.get_ema("AAPL", timespan="day", window=20, timestamp_lt=date.today().isoformat())
    assert isinstance(ema, list)
    if ema:
        assert isinstance(ema[0], IndicatorValue)

def test_get_macd_integration(client: PolygonClient):
    """Tests get_macd with a real API call."""
    macd = client.get_macd("AAPL", timespan="day", timestamp_lt=date.today().isoformat())
    assert isinstance(macd, list)
    if macd:
        assert isinstance(macd[0], MACDValue)

def test_get_rsi_integration(client: PolygonClient):
    """Tests get_rsi with a real API call."""
    rsi = client.get_rsi("AAPL", timespan="day", timestamp_lt=date.today().isoformat())
    assert isinstance(rsi, list)
    if rsi:
        assert isinstance(rsi[0], IndicatorValue)

@pytest.mark.xfail(reason="API is frequently rate-limiting this endpoint.")
def test_list_option_contracts_and_get_quote_integration(client: PolygonClient):
    """Tests listing option contracts and getting a quote for one with real API calls."""
    expiration_date_gt = date.today().isoformat()
    contracts = client.list_option_contracts(
        "AAPL", 
        limit=1, 
        expiration_date_gt=expiration_date_gt
    )
    assert isinstance(contracts, list)
    if not contracts:
        pytest.skip("No active option contracts found for AAPL to test.")

    assert len(contracts) == 1
    assert isinstance(contracts[0], OptionContract)

    # This second call in the same test is problematic for rate limiting
    option_ticker = contracts[0].ticker
    quote = client.get_last_quote_for_option(option_ticker)
    
    assert isinstance(quote, LastQuoteForOption)
    assert quote.ticker == option_ticker

@pytest.mark.xfail(reason="May fail with free tier due to data limitations/delays.")
def test_get_stock_financials_integration(client: PolygonClient):
    """Tests get_stock_financials with a real API call."""
    financials = client.get_stock_financials("AAPL", limit=1)
    assert isinstance(financials, list)
    if financials:
        assert len(financials) == 1
        assert isinstance(financials[0], StockFinancial)
        assert financials[0].cik is not None