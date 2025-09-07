"""Tests for DataFormattingService"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, date, timedelta
from decimal import Decimal

from marketdata_providers.data_formatter import DataFormattingService
from marketdata_providers.brain import MarketDataBrain, FetchResult
from marketdata_providers.base import (
    StockQuote,
    HistoricalPrice,
    OptionQuote,
    CompanyInfo,
    EarningsCalendar,
    EarningsCallTranscript,
    MarketStatus,
    EconomicEvent
)


class TestDataFormattingService:
    """Test DataFormattingService functionality"""
    
    @pytest.fixture
    def mock_brain(self):
        """Create a mock brain"""
        brain = Mock(spec=MarketDataBrain)
        return brain
    
    @pytest.fixture
    def formatter(self, mock_brain):
        """Create formatter with mock brain"""
        return DataFormattingService(brain=mock_brain)
    
    @pytest.fixture
    def sample_stock_quote(self):
        """Sample StockQuote for testing"""
        return StockQuote(
            symbol="AAPL",
            price=Decimal("150.25"),
            change=Decimal("2.50"),
            change_percent=Decimal("1.69"),
            volume=1000000,
            open=Decimal("148.00"),
            high=Decimal("151.00"),
            low=Decimal("147.50"),
            previous_close=Decimal("147.75"),
            timestamp=datetime(2023, 1, 15, 16, 0, 0),
            provider="test_provider"
        )
    
    @pytest.fixture
    def sample_historical_price(self):
        """Sample HistoricalPrice for testing"""
        return HistoricalPrice(
            symbol="AAPL",
            date=date(2023, 1, 15),
            open=Decimal("148.00"),
            high=Decimal("151.00"),
            low=Decimal("147.50"),
            close=Decimal("150.25"),
            volume=1000000,
            adjusted_close=Decimal("150.25"),
            dividend=Decimal("0.23"),
            split=Decimal("1.0"),
            provider="test_provider"
        )
    
    @pytest.fixture
    def sample_company_info(self):
        """Sample CompanyInfo for testing"""
        return CompanyInfo(
            symbol="AAPL",
            name="Apple Inc.",
            exchange="NASDAQ",
            sector="Technology",
            industry="Consumer Electronics",
            market_cap=2500000000000,
            employees=164000,
            description="Technology company",
            website="https://apple.com",
            ceo="Tim Cook",
            headquarters="Cupertino, CA",
            founded=1976,
            provider="test_provider"
        )
    
    def test_formatter_initialization_with_brain(self, mock_brain):
        """Test formatter initialization with provided brain"""
        formatter = DataFormattingService(brain=mock_brain)
        assert formatter.brain == mock_brain
    
    def test_formatter_initialization_without_brain(self):
        """Test formatter initialization without brain (creates default)"""
        with patch('marketdata_providers.data_formatter.MarketDataBrain') as mock_brain_class:
            mock_brain_instance = Mock()
            mock_brain_class.return_value = mock_brain_instance
            
            formatter = DataFormattingService()
            assert formatter.brain == mock_brain_instance
            mock_brain_class.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_format_quote_data_success(self, formatter, mock_brain, sample_stock_quote):
        """Test successful quote data formatting"""
        # Mock successful result
        mock_result = FetchResult(
            data=sample_stock_quote,
            provider="test_provider",
            success=True
        )
        mock_brain.get_quote = AsyncMock(return_value=mock_result)
        
        result = await formatter.format_quote_data("AAPL")
        
        assert result['success'] is True
        assert result['provider'] == "test_provider"
        assert result['symbol'] == "AAPL"
        assert 'data' in result
        
        # Check data structure
        data = result['data']
        assert data['symbol'] == "AAPL"
        assert data['price'] == 150.25
        assert data['change'] == 2.50
        assert data['change_percent'] == 1.69
        assert data['volume'] == 1000000
        assert data['open'] == 148.00
        assert data['high'] == 151.00
        assert data['low'] == 147.50
        assert data['previous_close'] == 147.75
        assert data['provider'] == "test_provider"
        assert 'timestamp' in data
        assert 'created_at' in data
    
    @pytest.mark.asyncio
    async def test_format_quote_data_failure(self, formatter, mock_brain):
        """Test quote data formatting when fetch fails"""
        # Mock failed result
        mock_result = FetchResult(
            data=None,
            provider="test_provider",
            success=False,
            error="Rate limit exceeded"
        )
        mock_brain.get_quote = AsyncMock(return_value=mock_result)
        
        result = await formatter.format_quote_data("AAPL")
        
        assert result['success'] is False
        assert result['error'] == "Rate limit exceeded"
        assert result['provider'] == "test_provider"
        assert result['symbol'] == "AAPL"
    
    @pytest.mark.asyncio
    async def test_format_historical_data_success(self, formatter, mock_brain, sample_historical_price):
        """Test successful historical data formatting"""
        # Mock successful result
        mock_result = FetchResult(
            data=[sample_historical_price],
            provider="test_provider",
            success=True
        )
        mock_brain.get_historical = AsyncMock(return_value=mock_result)
        
        result = await formatter.format_historical_data("AAPL", days_back=30)
        
        assert result['success'] is True
        assert result['provider'] == "test_provider"
        assert result['count'] == 1
        assert 'data' in result
        
        # Check data structure
        data = result['data'][0]
        assert data['symbol'] == "AAPL"
        assert data['date'] == "2023-01-15"
        assert data['open'] == 148.00
        assert data['high'] == 151.00
        assert data['low'] == 147.50
        assert data['close'] == 150.25
        assert data['volume'] == 1000000
        assert data['adjusted_close'] == 150.25
        assert data['dividend'] == 0.23
        assert data['split'] == 1.0
        assert data['provider'] == "test_provider"
        assert 'interval' in data
        assert 'created_at' in data
    
    @pytest.mark.asyncio
    async def test_format_company_info_success(self, formatter, mock_brain, sample_company_info):
        """Test successful company info formatting"""
        # Mock successful result
        mock_result = FetchResult(
            data=sample_company_info,
            provider="test_provider",
            success=True
        )
        mock_brain.get_company_info = AsyncMock(return_value=mock_result)
        
        result = await formatter.format_company_info("AAPL")
        
        assert result['success'] is True
        assert result['provider'] == "test_provider"
        assert 'data' in result
        
        # Check data structure
        data = result['data']
        assert data['symbol'] == "AAPL"
        assert data['name'] == "Apple Inc."
        assert data['exchange'] == "NASDAQ"
        assert data['sector'] == "Technology"
        assert data['industry'] == "Consumer Electronics"
        assert data['market_cap'] == 2500000000000
        assert data['employees'] == 164000
        assert data['description'] == "Technology company"
        assert data['website'] == "https://apple.com"
        assert data['ceo'] == "Tim Cook"
        assert data['headquarters'] == "Cupertino, CA"
        assert data['founded'] == 1976
        assert data['provider'] == "test_provider"
        assert 'created_at' in data
    
    @pytest.mark.asyncio
    async def test_format_fundamentals_success(self, formatter, mock_brain):
        """Test successful fundamentals formatting"""
        # Mock fundamentals data
        mock_fundamentals = {
            'market_cap': 2500000000000,
            'pe_ratio': 25.5,
            'pb_ratio': 12.3,
            'roe': 0.85,
            'debt_to_equity': 1.73,
            'revenue': 394328000000,
            'net_income': 99803000000,
            'eps': 6.15,
            'dividend_yield': 0.0047,
            'beta': 1.2
        }
        
        mock_result = FetchResult(
            data=mock_fundamentals,
            provider="test_provider",
            success=True
        )
        mock_brain.get_fundamentals = AsyncMock(return_value=mock_result)
        
        result = await formatter.format_fundamentals("AAPL")
        
        assert result['success'] is True
        assert result['provider'] == "test_provider"
        assert 'data' in result
        
        # Check data structure
        data = result['data']
        assert data['symbol'] == "AAPL"
        assert data['market_cap'] == 2500000000000
        assert data['pe_ratio'] == 25.5
        assert data['pb_ratio'] == 12.3
        assert data['roe'] == 0.85
        assert data['debt_to_equity'] == 1.73
        assert data['revenue'] == 394328000000
        assert data['net_income'] == 99803000000
        assert data['eps'] == 6.15
        assert data['dividend_yield'] == 0.0047
        assert data['beta'] == 1.2
        assert data['provider'] == "test_provider"
        assert 'created_at' in data
    
    @pytest.mark.asyncio
    async def test_batch_format_quotes(self, formatter, mock_brain, sample_stock_quote):
        """Test batch formatting of multiple quotes"""
        # Mock successful results for multiple symbols
        symbols = ["AAPL", "GOOGL", "MSFT"]
        
        def create_quote(symbol):
            quote = StockQuote(
                symbol=symbol,
                price=Decimal("100.00"),
                change=Decimal("1.00"),
                change_percent=Decimal("1.00"),
                volume=1000000,
                timestamp=datetime.now(),
                provider="test_provider"
            )
            return FetchResult(data=quote, provider="test_provider", success=True)
        
        mock_brain.get_quote = AsyncMock(side_effect=lambda symbol: create_quote(symbol))
        
        results = await formatter.batch_format_quotes(symbols)
        
        assert len(results) == 3
        for symbol in symbols:
            assert symbol in results
            assert results[symbol]['success'] is True
            assert results[symbol]['symbol'] == symbol
    
    def test_format_for_upsert_functions_quote(self, formatter):
        """Test formatting data for PostgreSQL upsert functions - quote"""
        quote_data = {
            'success': True,
            'data': {
                'symbol': 'AAPL',
                'price': 150.25,
                'change': 2.50,
                'change_percent': 1.69,
                'volume': 1000000,
                'open': 148.00,
                'high': 151.00,
                'low': 147.50,
                'previous_close': 147.75,
                'timestamp': '2023-01-15T16:00:00',
                'provider': 'test_provider'
            }
        }
        
        result = formatter.format_for_upsert_functions(quote_data, 'quote')
        
        assert result['p_symbol'] == 'AAPL'
        assert result['p_exchange_id'] == 1
        assert result['p_price'] == 150.25
        assert result['p_change_amount'] == 2.50
        assert result['p_change_percent'] == 1.69
        assert result['p_volume'] == 1000000
        assert result['p_open_price'] == 148.00
        assert result['p_high_price'] == 151.00
        assert result['p_low_price'] == 147.50
        assert result['p_previous_close'] == 147.75
        assert result['p_quote_timestamp'] == '2023-01-15T16:00:00'
        assert result['p_data_provider'] == 'test_provider'
    
    def test_format_for_upsert_functions_historical(self, formatter):
        """Test formatting data for PostgreSQL upsert functions - historical"""
        historical_data = {
            'success': True,
            'data': [{
                'symbol': 'AAPL',
                'date': '2023-01-15',
                'open': 148.00,
                'high': 151.00,
                'low': 147.50,
                'close': 150.25,
                'volume': 1000000,
                'adjusted_close': 150.25,
                'dividend': 0.23,
                'split': 1.0,
                'provider': 'test_provider'
            }]
        }
        
        result = formatter.format_for_upsert_functions(historical_data, 'historical')
        
        assert isinstance(result, list)
        assert len(result) == 1
        
        record = result[0]
        assert record['p_symbol'] == 'AAPL'
        assert record['p_exchange_id'] == 1
        assert record['p_date'] == '2023-01-15'
        assert record['p_open'] == 148.00
        assert record['p_high'] == 151.00
        assert record['p_low'] == 147.50
        assert record['p_close'] == 150.25
        assert record['p_volume'] == 1000000
        assert record['p_adjusted_close'] == 150.25
        assert record['p_dividend'] == 0.23
        assert record['p_split_ratio'] == 1.0
        assert record['p_data_provider'] == 'test_provider'
    
    def test_format_for_upsert_functions_company(self, formatter):
        """Test formatting data for PostgreSQL upsert functions - company"""
        company_data = {
            'success': True,
            'data': {
                'symbol': 'AAPL',
                'name': 'Apple Inc.',
                'exchange': 'NASDAQ',
                'sector': 'Technology',
                'industry': 'Consumer Electronics',
                'market_cap': 2500000000000,
                'employees': 164000,
                'description': 'Technology company',
                'website': 'https://apple.com',
                'ceo': 'Tim Cook',
                'headquarters': 'Cupertino, CA',
                'founded': 1976,
                'provider': 'test_provider'
            }
        }
        
        result = formatter.format_for_upsert_functions(company_data, 'company')
        
        assert result['p_symbol'] == 'AAPL'
        assert result['p_name'] == 'Apple Inc.'
        assert result['p_exchange'] == 'NASDAQ'
        assert result['p_sector'] == 'Technology'
        assert result['p_industry'] == 'Consumer Electronics'
        assert result['p_market_cap'] == 2500000000000
        assert result['p_employees'] == 164000
        assert result['p_description'] == 'Technology company'
        assert result['p_website'] == 'https://apple.com'
        assert result['p_ceo'] == 'Tim Cook'
        assert result['p_headquarters'] == 'Cupertino, CA'
        assert result['p_founded'] == 1976
        assert result['p_data_provider'] == 'test_provider'
    
    def test_format_for_upsert_functions_failed_data(self, formatter):
        """Test formatting failed data returns as-is"""
        failed_data = {
            'success': False,
            'error': 'Rate limit exceeded',
            'provider': 'test_provider'
        }
        
        result = formatter.format_for_upsert_functions(failed_data, 'quote')
        assert result == failed_data
    
    @pytest.mark.asyncio
    async def test_get_formatted_data_summary(self, formatter, mock_brain):
        """Test getting formatted data summary for multiple symbols"""
        symbols = ["AAPL", "GOOGL"]
        
        # Mock successful results for all data types
        def mock_get_quote(symbol):
            return FetchResult(
                data=StockQuote(
                    symbol=symbol,
                    price=Decimal("100.00"),
                    change=Decimal("1.00"),
                    change_percent=Decimal("1.00"),
                    volume=1000000,
                    timestamp=datetime.now(),
                    provider="test_provider"
                ),
                provider="test_provider",
                success=True
            )
        
        def mock_get_historical(symbol, start_date, end_date, interval):
            return FetchResult(
                data=[HistoricalPrice(
                    symbol=symbol,
                    date=date.today(),
                    open=Decimal("100.00"),
                    high=Decimal("101.00"),
                    low=Decimal("99.00"),
                    close=Decimal("100.50"),
                    volume=1000000,
                    provider="test_provider"
                )],
                provider="test_provider",
                success=True
            )
        
        def mock_get_company_info(symbol):
            return FetchResult(
                data=CompanyInfo(
                    symbol=symbol,
                    name=f"{symbol} Company",
                    description="Test company",
                    sector="Technology",
                    industry="Software",
                    market_cap=1000000000,
                    employees=10000,
                    provider="test_provider"
                ),
                provider="test_provider",
                success=True
            )
        
        mock_brain.get_quote = AsyncMock(side_effect=mock_get_quote)
        mock_brain.get_historical = AsyncMock(side_effect=mock_get_historical)
        mock_brain.get_company_info = AsyncMock(side_effect=mock_get_company_info)
        
        summary = await formatter.get_formatted_data_summary(symbols)
        
        assert summary['symbols_processed'] == 2
        assert summary['quotes_success'] == 2
        assert summary['historical_success'] == 2
        assert summary['company_info_success'] == 2
        assert summary['errors'] == 0
        assert 'test_provider' in summary['providers_used']
    
    @pytest.mark.asyncio
    async def test_format_options_data_success(self, formatter, mock_brain):
        """Test successful options data formatting"""
        sample_option = OptionQuote(
            symbol="AAPL240315C00150000",
            underlying_symbol="AAPL",
            strike=Decimal("150.00"),
            expiration=date(2024, 3, 15),
            option_type="call",
            bid=Decimal("5.20"),
            ask=Decimal("5.40"),
            last_price=Decimal("5.30"),
            volume=1000,
            open_interest=5000,
            timestamp=datetime.now(),
            provider="test_provider"
        )
        
        mock_result = FetchResult(
            data=[sample_option],
            provider="test_provider",
            success=True
        )
        mock_brain.get_options_chain = AsyncMock(return_value=mock_result)
        
        result = await formatter.format_options_data("AAPL", "2024-03-15")
        
        assert result['success'] is True
        assert result['provider'] == "test_provider"
        assert result['count'] == 1
        assert 'data' in result
        
        option_data = result['data'][0]
        assert option_data['symbol'] == "AAPL240315C00150000"
        assert option_data['underlying_symbol'] == "AAPL"
        assert option_data['strike'] == 150.00
        assert option_data['expiration'] == "2024-03-15"
        assert option_data['option_type'] == "call"


if __name__ == "__main__":
    pytest.main([__file__])
