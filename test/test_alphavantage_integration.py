import os
import time
import pytest
from stonksapi.alpha_vantage.client import AlphaVantageClient
from stonksapi.alpha_vantage.models import (
    QuoteResponse,
    DailyTimeSeries,
    CompanyOverview,
    ExchangeRateResponse,
    CryptoTimeSeries,
)

# Check if the API key is available. If not, all tests in this file will be skipped.
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

pytestmark = pytest.mark.skipif(
    not API_KEY or API_KEY == "1M8BWT7", reason="ALPHA_VANTAGE_API_KEY not set or is demo key"
)


@pytest.fixture(scope="module")
def client():
    """Module-scoped fixture for a real AlphaVantageClient."""
    return AlphaVantageClient(api_key=API_KEY)


@pytest.mark.integration
def test_integration_get_quote(client):
    """Tests get_quote against the live API."""
    # Add a delay to respect API rate limits
    time.sleep(15)
    
    quote = client.get_quote("AAPL")
    assert isinstance(quote, QuoteResponse)
    assert quote.global_quote.symbol == "AAPL"
    assert quote.global_quote.price > 0


@pytest.mark.integration
def test_integration_get_daily(client):
    """Tests get_daily against the live API."""
    time.sleep(15)
    
    daily_data = client.get_daily("TSLA")
    assert isinstance(daily_data, DailyTimeSeries)
    assert daily_data.meta_data.symbol == "TSLA"
    assert len(daily_data.time_series) > 0


@pytest.mark.integration
def test_integration_get_company_overview(client):
    """Tests get_company_overview against the live API."""
    time.sleep(15)
    
    overview = client.get_company_overview("MSFT")
    assert isinstance(overview, CompanyOverview)
    assert overview.symbol == "MSFT"
    assert overview.name == "Microsoft Corporation"


@pytest.mark.integration
def test_integration_get_currency_exchange_rate(client):
    """Tests get_currency_exchange_rate against the live API."""
    time.sleep(15)
    
    exchange_rate = client.get_currency_exchange_rate("USD", "EUR")
    assert isinstance(exchange_rate, ExchangeRateResponse)
    assert exchange_rate.realtime_currency_exchange_rate.from_currency_code == "USD"
    assert exchange_rate.realtime_currency_exchange_rate.to_currency_code == "EUR"
    assert exchange_rate.realtime_currency_exchange_rate.exchange_rate > 0


@pytest.mark.integration
def test_integration_get_crypto_daily(client):
    """Tests get_crypto_daily against the live API."""
    time.sleep(15)
    
    crypto_data = client.get_crypto_daily("BTC", "USD")
    assert isinstance(crypto_data, CryptoTimeSeries)
    assert crypto_data.meta_data.digital_currency_code == "BTC"
    assert crypto_data.meta_data.market_code == "USD"
    assert len(crypto_data.time_series) > 0