import pytest
from unittest.mock import MagicMock, patch
from stonksapi.finnhub.client import FinnhubClient
from stonksapi.finnhub.models import (
    CompanyProfile,
    Quote,
    MarketNews,
)

@pytest.fixture
def mock_finnhub_client():
    """Fixture to mock the finnhub.Client."""
    with patch('finnhub.Client') as mock_client:
        yield mock_client

@pytest.fixture
def client(mock_finnhub_client) -> FinnhubClient:
    """Fixture to create a FinnhubClient instance with a mocked finnhub.Client."""
    return FinnhubClient(api_key="test_key")

def test_get_company_profile(client: FinnhubClient, mock_finnhub_client):
    """Tests get_company_profile with a mocked API response."""
    mock_response = {
        'country': 'US',
        'currency': 'USD',
        'exchange': 'NASDAQ/NMS (GLOBAL MARKET)',
        'finnhubIndustry': 'Technology',
        'ipo': '1980-12-12',
        'logo': 'https://static.finnhub.io/logo/aapl.svg',
        'marketCapitalization': 2000000,
        'name': 'Apple Inc',
        'phone': '14089961010',
        'shareOutstanding': 16000,
        'ticker': 'AAPL',
        'weburl': 'https://www.apple.com/'
    }
    client._client.company_profile2.return_value = mock_response

    profile = client.get_company_profile("AAPL")

    assert isinstance(profile, CompanyProfile)
    assert profile.ticker == "AAPL"
    client._client.company_profile2.assert_called_once_with(symbol="AAPL")

def test_get_quote(client: FinnhubClient, mock_finnhub_client):
    """Tests get_quote with a mocked API response."""
    mock_response = {
        'c': 200.0,
        'h': 205.0,
        'l': 198.0,
        'o': 201.0,
        'pc': 199.0,
        't': 1640995200
    }
    client._client.quote.return_value = mock_response

    quote = client.get_quote("AAPL")

    assert isinstance(quote, Quote)
    assert quote.current_price == 200.0
    client._client.quote.assert_called_once_with(symbol="AAPL")

def test_get_market_news(client: FinnhubClient, mock_finnhub_client):
    """Tests get_market_news with a mocked API response."""
    mock_response = [
        {
            'category': 'general',
            'datetime': 1640995200,
            'headline': 'Test headline',
            'id': 12345,
            'image': '',
            'related': 'AAPL',
            'source': 'Test Source',
            'summary': 'Test summary',
            'url': ''
        }
    ]
    client._client.general_news.return_value = mock_response

    news = client.get_market_news("general")

    assert isinstance(news, list)
    assert len(news) == 1
    assert isinstance(news[0], MarketNews)
    assert news[0].id == 12345
    client._client.general_news.assert_called_once_with("general", min_id=0)
