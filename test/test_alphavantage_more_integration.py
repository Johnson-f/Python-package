import os
import time
import pytest
from dotenv import load_dotenv
from stonksapi.alpha_vantage.client import AlphaVantageClient, Interval
from stonksapi.alpha_vantage.models import (
    IntradayTimeSeries,
    Earnings,
    SymbolSearchResponse,
    TechnicalIndicatorResponse,
)

# Load environment variables
load_dotenv()

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
def test_integration_get_intraday(client):
    """Tests get_intraday against the live API."""
    # Add a delay to respect API rate limits
    time.sleep(15)
    
    intraday_data = client.get_intraday("IBM", interval=Interval.MIN_5)
    assert isinstance(intraday_data, IntradayTimeSeries)
    assert intraday_data.meta_data.symbol == "IBM"
    assert len(intraday_data.time_series) > 0


@pytest.mark.integration
def test_integration_get_earnings(client):
    """Tests get_earnings against the live API."""
    time.sleep(15)
    
    earnings_data = client.get_earnings("IBM")
    assert isinstance(earnings_data, Earnings)
    assert earnings_data.symbol == "IBM"
    assert len(earnings_data.annual_earnings) > 0


@pytest.mark.integration
def test_integration_search_symbol(client):
    """Tests search_symbol against the live API."""
    time.sleep(15)
    
    search_results = client.search_symbol("BA")
    assert isinstance(search_results, SymbolSearchResponse)
    assert len(search_results.best_matches) > 0
    # Check if at least one result contains the search term
    assert any("BA" in match.symbol for match in search_results.best_matches)


@pytest.mark.integration
def test_integration_get_sma(client):
    """Tests get_sma against the live API."""
    time.sleep(15)
    
    sma_data = client.get_sma("IBM", interval=Interval.DAILY, time_period=60)
    assert isinstance(sma_data, TechnicalIndicatorResponse)
    assert sma_data.meta_data.symbol == "IBM"
    assert "SMA" in sma_data.meta_data.indicator
    assert len(sma_data.technical_analysis) > 0
