import pytest
from unittest.mock import patch, MagicMock
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

@pytest.fixture
def client():
    """Fixture for FinanceQueryClient."""
    return FinanceQueryClient()

@patch('requests.get')
def test_get_market_hours(mock_get, client: FinanceQueryClient):
    """Tests get_market_hours with a mocked API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": "open",
        "reason": "Regular trading hours.",
        "timestamp": "2021-09-22T14:00:00.000Z"
    }
    mock_get.return_value = mock_response

    result = client.get_market_hours()

    assert isinstance(result, MarketHours)
    assert result.status == "open"
    mock_get.assert_called_once_with("https://finance-query.onrender.com/hours", params=None)

@patch('requests.get')
def test_get_detailed_quotes(mock_get, client: FinanceQueryClient):
    """Tests get_detailed_quotes with a mocked API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "price": "145.00",
            "change": "+1.00",
            "percentChange": "+0.69%"
        }
    ]
    mock_get.return_value = mock_response

    result = client.get_detailed_quotes(["AAPL"])

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], DetailedQuote)
    assert result[0].symbol == "AAPL"
    mock_get.assert_called_once_with("https://finance-query.onrender.com/v1/quotes", params={"symbols": "AAPL"})

@patch('requests.get')
def test_get_simple_quotes(mock_get, client: FinanceQueryClient):
    """Tests get_simple_quotes with a mocked API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"symbol": "TSLA", "name": "Tesla, Inc.", "price": "450.00", "change": "+5.00", "percentChange": "+1.12%"}
    ]
    mock_get.return_value = mock_response
    result = client.get_simple_quotes(["TSLA"])
    assert isinstance(result, list)
    assert isinstance(result[0], SimpleQuote)
    assert result[0].symbol == "TSLA"
    mock_get.assert_called_once_with("https://finance-query.onrender.com/v1/simple-quotes", params={"symbols": "TSLA"})

@patch('requests.get')
def test_get_similar_stocks(mock_get, client: FinanceQueryClient):
    """Tests get_similar_stocks with a mocked API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"symbol": "LCID", "name": "Lucid Group, Inc.", "price": "25.00", "change": "+0.50", "percentChange": "+2.04%"}
    ]
    mock_get.return_value = mock_response
    result = client.get_similar_stocks("TSLA", limit=1)
    assert isinstance(result, list)
    assert isinstance(result[0], SimilarStock)
    assert result[0].symbol == "LCID"
    mock_get.assert_called_once_with("https://finance-query.onrender.com/v1/similar", params={"symbol": "TSLA", "limit": 1})

@patch('requests.get')
def test_get_historical_data(mock_get, client: FinanceQueryClient):
    """Tests get_historical_data with a mocked API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "2025-10-03 16:00:00": {"open": 436, "high": 436, "low": 436, "close": 436, "volume": 0}
    }
    mock_get.return_value = mock_response
    result = client.get_historical_data("NVDA", "1d", "5m")
    assert isinstance(result, dict)
    assert isinstance(result["2025-10-03 16:00:00"], HistoricalDataPoint)
    mock_get.assert_called_once_with("https://finance-query.onrender.com/v1/historical", params={"symbol": "NVDA", "range": "1d", "interval": "5m"})

@patch('requests.get')
def test_get_actives(mock_get, client: FinanceQueryClient):
    """Tests get_actives with a mocked API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"symbol": "AMD", "name": "Advanced Micro Devices, Inc.", "price": "100.00", "change": "+2.00", "percentChange": "+2.04%"}
    ]
    mock_get.return_value = mock_response
    result = client.get_actives(limit=1)
    assert isinstance(result[0], MarketMover)
    mock_get.assert_called_once_with("https://finance-query.onrender.com/v1/actives?limit=1")

@patch('requests.get')
def test_get_gainers(mock_get, client: FinanceQueryClient):
    """Tests get_gainers with a mocked API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"symbol": "INTC", "name": "Intel Corporation", "price": "35.00", "change": "+3.00", "percentChange": "+9.38%"}
    ]
    mock_get.return_value = mock_response
    result = client.get_gainers(limit=1)
    assert isinstance(result[0], MarketMover)
    mock_get.assert_called_once_with("https://finance-query.onrender.com/v1/gainers?limit=1")

@patch('requests.get')
def test_get_losers(mock_get, client: FinanceQueryClient):
    """Tests get_losers with a mocked API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"symbol": "F", "name": "Ford Motor Company", "price": "12.00", "change": "-0.50", "percentChange": "-4.00%"}
    ]
    mock_get.return_value = mock_response
    result = client.get_losers(limit=1)
    assert isinstance(result[0], MarketMover)
    mock_get.assert_called_once_with("https://finance-query.onrender.com/v1/losers?limit=1")

@patch('requests.get')
def test_get_stock_news(mock_get, client: FinanceQueryClient):
    """Tests get_stock_news with a mocked API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"title": "Test News", "link": "http://test.com", "source": "Test Source", "img": "http://test.com/img.png", "time": "1 hour ago"}
    ]
    mock_get.return_value = mock_response
    result = client.get_stock_news("MSFT")
    assert isinstance(result[0], StockNews)
    mock_get.assert_called_once_with("https://finance-query.onrender.com/v1/news", params={"symbol": "MSFT"})

@patch('requests.get')
def test_search_symbols(mock_get, client: FinanceQueryClient):
    """Tests search_symbols with a mocked API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"name": "Tesla, Inc.", "symbol": "TSLA", "exchange": "NMS", "type": "stock"}
    ]
    mock_get.return_value = mock_response
    result = client.search_symbols("Tesla")
    assert isinstance(result[0], SymbolSearchResult)
    mock_get.assert_called_once_with("https://finance-query.onrender.com/v1/search", params={"query": "Tesla", "hits": 2, "yahoo": "true"})

@patch('requests.get')
def test_get_all_sector_performance(mock_get, client: FinanceQueryClient):
    """Tests get_all_sector_performance with a mocked API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"sector": "Technology", "dayReturn": "+0.50%", "ytdReturn": "+15.00%", "yearReturn": "+30.00%", "threeYearReturn": "+100.00%", "fiveYearReturn": "+200.00%"}
    ]
    mock_get.return_value = mock_response
    result = client.get_all_sector_performance()
    assert isinstance(result[0], SectorPerformance)
    mock_get.assert_called_once_with("https://finance-query.onrender.com/v1/sectors")

@patch('requests.get')
def test_get_sector_performance(mock_get, client: FinanceQueryClient):
    """Tests get_sector_performance with a mocked API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"sector": "Technology", "dayReturn": "+0.50%", "ytdReturn": "+15.00%", "yearReturn": "+30.00%", "threeYearReturn": "+100.00%", "fiveYearReturn": "+200.00%"}
    mock_get.return_value = mock_response
    result = client.get_sector_performance("AAPL")
    assert isinstance(result, SectorPerformance)
    mock_get.assert_called_once_with("https://finance-query.onrender.com/v1/sectors/symbol/AAPL")
