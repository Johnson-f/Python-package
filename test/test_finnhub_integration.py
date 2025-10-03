import os
import pytest
from dotenv import load_dotenv
from stonksapi.finnhub.client import FinnhubClient
from stonksapi.finnhub.models import (
    CompanyProfile,
    Quote,
    MarketNews,
)

# Load environment variables from .env file
load_dotenv()

@pytest.fixture(scope="module")
def api_key() -> str:
    """Fixture to provide the Finnhub API key and skip tests if it's not available."""
    key = os.getenv("FINNHUB_API_KEY")
    if not key:
        pytest.skip("FINNHUB_API_KEY environment variable not set, skipping integration tests.")
    return key

@pytest.fixture(scope="module")
def client(api_key: str) -> FinnhubClient:
    """Fixture to create a FinnhubClient instance for integration tests."""
    return FinnhubClient(api_key=api_key)

# This test should run even without an API key.
def test_client_init_no_api_key():
    """Test that FinnhubClient raises ValueError if no API key is provided."""
    original_key = os.environ.pop("FINNHUB_API_KEY", None)
    try:
        with pytest.raises(ValueError, match="API key must be provided"):
            FinnhubClient()
    finally:
        if original_key:
            os.environ["FINNHUB_API_KEY"] = original_key

# --- Integration Tests (require API key) ---

def test_get_company_profile_integration(client: FinnhubClient):
    """Tests get_company_profile with a real API call."""
    profile = client.get_company_profile("AAPL")
    assert isinstance(profile, CompanyProfile)
    assert profile.ticker == "AAPL"

def test_get_quote_integration(client: FinnhubClient):
    """Tests get_quote with a real API call."""
    quote = client.get_quote("AAPL")
    assert isinstance(quote, Quote)
    assert quote.current_price is not None

def test_get_market_news_integration(client: FinnhubClient):
    """Tests get_market_news with a real API call."""
    news = client.get_market_news("general")
    assert isinstance(news, list)
    if news:
        assert isinstance(news[0], MarketNews)
