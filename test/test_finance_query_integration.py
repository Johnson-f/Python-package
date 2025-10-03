import pytest
from stonksapi.finance_query.client import FinanceQueryClient
from stonksapi.finance_query.models import (
    MarketHours,
    DetailedQuote,
    SimpleQuote,
    SimilarStock,
    HistoricalDataPoint,
    MarketMover,
    StockNews,
    SymbolSearchResult,
    SectorPerformance,
)

@pytest.fixture(scope="module")
def client():
    """Module-scoped fixture for the FinanceQueryClient."""
    return FinanceQueryClient()

@pytest.mark.integration
def test_get_market_hours(client: FinanceQueryClient):
    """Tests get_market_hours against the live API."""
    result = client.get_market_hours()
    assert isinstance(result, MarketHours)
    assert result.status is not None

@pytest.mark.integration
def test_get_detailed_quotes(client: FinanceQueryClient):
    """Tests get_detailed_quotes against the live API."""
    result = client.get_detailed_quotes(["AAPL", "GOOG"])
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], DetailedQuote)
    assert result[0].symbol == "AAPL"

@pytest.mark.integration
def test_get_simple_quotes(client: FinanceQueryClient):
    """Tests get_simple_quotes against the live API."""
    result = client.get_simple_quotes(["TSLA"])
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], SimpleQuote)
    assert result[0].symbol == "TSLA"

@pytest.mark.integration
def test_get_similar_stocks(client: FinanceQueryClient):
    """Tests get_similar_stocks against the live API."""
    result = client.get_similar_stocks("TSLA", limit=5)
    assert isinstance(result, list)
    assert len(result) <= 5
    if result:
        assert isinstance(result[0], SimilarStock)

@pytest.mark.integration
def test_get_historical_data(client: FinanceQueryClient):
    """Tests get_historical_data against the live API."""
    result = client.get_historical_data("NVDA", "1d", "5m")
    assert isinstance(result, dict)
    if result:
        first_key = next(iter(result))
        assert isinstance(result[first_key], HistoricalDataPoint)

@pytest.mark.integration
def test_get_actives(client: FinanceQueryClient):
    """Tests get_actives against the live API."""
    result = client.get_actives()
    assert isinstance(result, list)
    assert len(result) > 0
    if result:
        assert isinstance(result[0], MarketMover)

@pytest.mark.integration
def test_get_gainers(client: FinanceQueryClient):
    """Tests get_gainers against the live API."""
    result = client.get_gainers()
    assert isinstance(result, list)
    assert len(result) > 0
    if result:
        assert isinstance(result[0], MarketMover)

@pytest.mark.integration
def test_get_losers(client: FinanceQueryClient):
    """Tests get_losers against the live API."""
    result = client.get_losers()
    assert isinstance(result, list)
    assert len(result) > 0
    if result:
        assert isinstance(result[0], MarketMover)

@pytest.mark.integration
def test_get_stock_news(client: FinanceQueryClient):
    """Tests get_stock_news against the live API."""
    result = client.get_stock_news("MSFT")
    assert isinstance(result, list)
    if result:
        assert isinstance(result[0], StockNews)

@pytest.mark.integration
def test_search_symbols(client: FinanceQueryClient):
    """Tests search_symbols against the live API."""
    result = client.search_symbols("Tesla")
    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], SymbolSearchResult)

@pytest.mark.integration
def test_get_all_sector_performance(client: FinanceQueryClient):
    """Tests get_all_sector_performance against the live API."""
    result = client.get_all_sector_performance()
    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], SectorPerformance)

@pytest.mark.integration
def test_get_sector_performance(client: FinanceQueryClient):
    """Tests get_sector_performance against the live API."""
    result = client.get_sector_performance("AAPL")
    assert isinstance(result, SectorPerformance)
    assert result.sector is not None

@pytest.mark.integration
def test_api_request_fails(client: FinanceQueryClient):
    """Tests that a request to a non-existent endpoint raises a ConnectionError."""
    original_url = client.base_url
    client.base_url = "http://localhost:12345"  # A non-existent URL
    with pytest.raises(ConnectionError):
        client.get_market_hours()
    client.base_url = original_url
