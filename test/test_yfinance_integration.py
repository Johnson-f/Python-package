import pytest
import time
from stonksapi.yfinance.client import YFinanceClient
from stonksapi.yfinance.models import (
    TickerInfo,
    HistoricalData,
    Dividend,
    Split,
    FinancialStatement,
)

# Mark all tests in this file as integration tests
pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def client():
    """Module-scoped fixture for a real YFinanceClient."""
    return YFinanceClient()


def test_integration_get_ticker_info(client):
    """Tests get_ticker_info against the live API."""
    time.sleep(5)
    info = client.get_ticker_info("AAPL")
    assert isinstance(info, TickerInfo)
    assert info.symbol == "AAPL"
    assert info.long_name == "Apple Inc."


def test_integration_get_multiple_ticker_info(client):
    """Tests get_multiple_ticker_info against the live API."""
    time.sleep(5)
    infos = client.get_multiple_ticker_info(["MSFT", "GOOG"])
    assert len(infos) == 2
    assert isinstance(infos[0], TickerInfo)
    assert infos[0].symbol == "MSFT"
    assert isinstance(infos[1], TickerInfo)
    assert infos[1].symbol == "GOOG"


def test_integration_get_history(client):
    """Tests get_history against the live API."""
    time.sleep(5)
    history = client.get_history("TSLA", period="1mo")
    assert isinstance(history, list)
    assert len(history) > 0
    assert isinstance(history[0], HistoricalData)


def test_integration_get_dividends(client):
    """Tests get_dividends against the live API."""
    time.sleep(5)
    # Use a stock known for dividends
    dividends = client.get_dividends("KO")  # Coca-Cola
    assert isinstance(dividends, list)
    if len(dividends) > 0:
        assert isinstance(dividends[0], Dividend)


def test_integration_get_splits(client):
    """Tests get_splits against the live API."""
    time.sleep(5)
    # Use a stock known for splits
    splits = client.get_splits("AAPL")
    assert isinstance(splits, list)
    assert len(splits) > 0
    assert isinstance(splits[0], Split)


def test_integration_get_income_statement(client):
    """Tests get_income_statement against the live API."""
    time.sleep(5)
    statement = client.get_income_statement("MSFT")
    assert isinstance(statement, FinancialStatement)
    assert len(statement.reports) > 0
    assert "Total Revenue" in statement.reports[0].metrics


def test_integration_get_balance_sheet_quarterly(client):
    """Tests get_balance_sheet (quarterly) against the live API."""
    time.sleep(5)
    statement = client.get_balance_sheet("MSFT", quarterly=True)
    assert isinstance(statement, FinancialStatement)
    assert len(statement.reports) > 0
    assert "Total Assets" in statement.reports[0].metrics


def test_integration_get_cash_flow(client):
    """Tests get_cash_flow against the live API."""
    time.sleep(5)
    statement = client.get_cash_flow("MSFT")
    assert isinstance(statement, FinancialStatement)
    assert len(statement.reports) > 0
    assert "Operating Cash Flow" in statement.reports[0].metrics
