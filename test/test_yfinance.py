import pytest
from unittest.mock import patch, MagicMock, PropertyMock
import pandas as pd
from datetime import date

from stonksapi.yfinance.client import YFinanceClient
from stonksapi.yfinance.models import (
    TickerInfo,
    HistoricalData,
    Dividend,
    Split,
    FinancialStatement,
)

@pytest.fixture
def client():
    """Fixture for YFinanceClient."""
    return YFinanceClient()

@patch('yfinance.Ticker')
def test_get_ticker_info(mock_ticker, client):
    """Test the get_ticker_info method."""
    # Arrange: Create mock data for the .info dictionary
    mock_info_data = {
        'symbol': 'MSFT',
        'longName': 'Microsoft Corporation',
        'sector': 'Technology'
        'industry': 'Software—Infrastructure',
        'marketCap': 3000000000000,
        'website': 'https://www.microsoft.com',
        'trailingPE': 35.0,
        'volume': 20000000
    }
    
    # Configure the mock Ticker instance
    mock_instance = MagicMock()
    mock_instance.info = mock_info_data
    mock_ticker.return_value = mock_instance
    
    # Act: Call the method under test
    ticker_info = client.get_ticker_info('MSFT')
    
    # Assert
    # Ensure yfinance.Ticker was called with the correct symbol
    mock_ticker.assert_called_once_with('MSFT')
    
    # Ensure the returned object is the correct Pydantic model
    assert isinstance(ticker_info, TickerInfo)
    
    # Ensure the data was parsed correctly
    assert ticker_info.long_name == 'Microsoft Corporation'
    assert ticker_info.sector == 'Technology'
    assert ticker_info.market_cap == 3000000000000
    assert str(ticker_info.website) == 'https://www.microsoft.com/' # Pydantic converts to HttpUrl

@patch('yfinance.Ticker')
def test_get_multiple_ticker_info(mock_ticker, client):
    """Test the get_multiple_ticker_info method."""
    # Arrange: Create mock data for two different tickers
    mock_info_aapl = {
        'symbol': 'AAPL',
        'longName': 'Apple Inc.',
        'sector': 'Technology',
    }
    mock_info_goog = {
        'symbol': 'GOOG',
        'longName': 'Alphabet Inc.',
        'sector': 'Communication Services',
    }

    # Configure the mock to return different info based on the symbol
    def side_effect(symbol):
        mock_instance = MagicMock()
        if symbol == 'AAPL':
            mock_instance.info = mock_info_aapl
        elif symbol == 'GOOG':
            mock_instance.info = mock_info_goog
        else:
            mock_instance.info = {}
        return mock_instance

    mock_ticker.side_effect = side_effect
    
    # Act
    ticker_infos = client.get_multiple_ticker_info(['AAPL', 'GOOG'])
    
    # Assert
    assert len(ticker_infos) == 2
    assert isinstance(ticker_infos[0], TickerInfo)
    assert isinstance(ticker_infos[1], TickerInfo)
    
    assert ticker_infos[0].symbol == 'AAPL'
    assert ticker_infos[0].long_name == 'Apple Inc.'
    assert ticker_infos[1].symbol == 'GOOG'
    assert ticker_infos[1].long_name == 'Alphabet Inc.'
    
    # Check that yf.Ticker was called for each symbol
    assert mock_ticker.call_count == 2
    mock_ticker.assert_any_call('AAPL')
    mock_ticker.assert_any_call('GOOG')

@patch("yfinance.Ticker")
def test_get_history(mock_ticker, client):
    """Test the get_history method."""
    # Arrange
    mock_instance = MagicMock()
    hist_df = pd.DataFrame(
        {
            "Open": [100],
            "High": [101],
            "Low": [99],
            "Close": [100.5],
            "Volume": [1000],
            "Dividends": [0],
            "Stock Splits": [0.0],
        },
        index=pd.to_datetime(["2023-01-01"]),
    )
    hist_df.index.name = "Date"
    mock_instance.history.return_value = hist_df
    mock_ticker.return_value = mock_instance

    # Act
    history = client.get_history("AAPL", period="1d")

    # Assert
    mock_ticker.assert_called_once_with("AAPL")
    mock_instance.history.assert_called_once_with(period="1d")
    assert len(history) == 1
    assert isinstance(history[0], HistoricalData)
    assert history[0].date == date(2023, 1, 1)
    assert history[0].close == 100.5


@patch("yfinance.Ticker")
def test_get_dividends(mock_ticker, client):
    """Test the get_dividends method."""
    # Arrange
    mock_instance = MagicMock()
    div_series = pd.Series([0.5], index=pd.to_datetime(["2023-03-01"]))
    div_series.index.name = "Date"
    # Mock `dividends` as a property
    type(mock_instance).dividends = PropertyMock(return_value=div_series)
    mock_ticker.return_value = mock_instance

    # Act
    dividends = client.get_dividends("AAPL")

    # Assert
    mock_ticker.assert_called_once_with("AAPL")
    assert len(dividends) == 1
    assert isinstance(dividends[0], Dividend)
    assert dividends[0].date == date(2023, 3, 1)
    assert dividends[0].dividend == 0.5


@patch("yfinance.Ticker")
def test_get_splits(mock_ticker, client):
    """Test the get_splits method."""
    # Arrange
    mock_instance = MagicMock()
    split_series = pd.Series([2.0], index=pd.to_datetime(["2023-02-01"]))
    split_series.index.name = "Date"
    type(mock_instance).splits = PropertyMock(return_value=split_series)
    mock_ticker.return_value = mock_instance

    # Act
    splits = client.get_splits("AAPL")

    # Assert
    mock_ticker.assert_called_once_with("AAPL")
    assert len(splits) == 1
    assert isinstance(splits[0], Split)
    assert splits[0].date == date(2023, 2, 1)
    assert splits[0].stock_splits == 2.0


@patch("yfinance.Ticker")
def test_get_income_statement_annual(mock_ticker, client):
    """Test the get_income_statement method for annual data."""
    # Arrange
    mock_instance = MagicMock()
    fin_df = pd.DataFrame(
        {
            pd.Timestamp("2023-12-31"): {"Total Revenue": 1000, "Net Income": 100},
            pd.Timestamp("2022-12-31"): {"Total Revenue": 900, "Net Income": 90},
        }
    )
    type(mock_instance).financials = PropertyMock(return_value=fin_df)
    mock_ticker.return_value = mock_instance

    # Act
    statement = client.get_income_statement("AAPL")

    # Assert
    mock_ticker.assert_called_once_with("AAPL")
    assert isinstance(statement, FinancialStatement)
    assert len(statement.reports) == 2
    assert statement.reports[0].date == date(2023, 12, 31)
    assert statement.reports[0].metrics["Total Revenue"] == 1000


@patch("yfinance.Ticker")
def test_get_income_statement_quarterly(mock_ticker, client):
    """Test the get_income_statement method for quarterly data."""
    # Arrange
    mock_instance = MagicMock()
    fin_df = pd.DataFrame(
        {pd.Timestamp("2023-12-31"): {"Total Revenue": 300}}
    )
    type(mock_instance).quarterly_financials = PropertyMock(return_value=fin_df)
    mock_ticker.return_value = mock_instance

    # Act
    statement = client.get_income_statement("AAPL", quarterly=True)

    # Assert
    assert isinstance(statement, FinancialStatement)
    assert len(statement.reports) == 1
    assert statement.reports[0].metrics["Total Revenue"] == 300


@patch("yfinance.Ticker")
def test_get_balance_sheet(mock_ticker, client):
    """Test the get_balance_sheet method."""
    # Arrange
    mock_instance = MagicMock()
    bal_df = pd.DataFrame(
        {pd.Timestamp("2023-12-31"): {"Total Assets": 2000}}
    )
    type(mock_instance).balance_sheet = PropertyMock(return_value=bal_df)
    mock_ticker.return_value = mock_instance

    # Act
    statement = client.get_balance_sheet("AAPL")

    # Assert
    assert isinstance(statement, FinancialStatement)
    assert statement.reports[0].metrics["Total Assets"] == 2000


@patch("yfinance.Ticker")
def test_get_balance_sheet_quarterly(mock_ticker, client):
    """Test the get_balance_sheet method for quarterly data."""
    # Arrange
    mock_instance = MagicMock()
    bal_df = pd.DataFrame(
        {pd.Timestamp("2023-12-31"): {"Total Assets": 500}}
    )
    type(mock_instance).quarterly_balance_sheet = PropertyMock(return_value=bal_df)
    mock_ticker.return_value = mock_instance

    # Act
    statement = client.get_balance_sheet("AAPL", quarterly=True)

    # Assert
    assert isinstance(statement, FinancialStatement)
    assert statement.reports[0].metrics["Total Assets"] == 500


@patch("yfinance.Ticker")
def test_get_cash_flow(mock_ticker, client):
    """Test the get_cash_.flow method."""
    # Arrange
    mock_instance = MagicMock()
    cf_df = pd.DataFrame(
        {pd.Timestamp("2023-12-31"): {"Operating Cash Flow": 150}}
    )
    type(mock_instance).cashflow = PropertyMock(return_value=cf_df)
    mock_ticker.return_value = mock_instance

    # Act
    statement = client.get_cash_flow("AAPL")

    # Assert
    assert isinstance(statement, FinancialStatement)
    assert statement.reports[0].metrics["Operating Cash Flow"] == 150


@patch("yfinance.Ticker")
def test_get_cash_flow_quarterly(mock_ticker, client):
    """Test the get_cash_flow method for quarterly data."""
    # Arrange
    mock_instance = MagicMock()
    cf_df = pd.DataFrame(
        {pd.Timestamp("2023-12-31"): {"Operating Cash Flow": 40}}
    )
    type(mock_instance).quarterly_cashflow = PropertyMock(return_value=cf_df)
    mock_ticker.return_value = mock_instance

    # Act
    statement = client.get_cash_flow("AAPL", quarterly=True)

    # Assert
    assert isinstance(statement, FinancialStatement)
    assert statement.reports[0].metrics["Operating Cash Flow"] == 40