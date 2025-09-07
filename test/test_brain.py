"""Tests for MarketDataBrain - the central orchestrator"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, date, timedelta
from decimal import Decimal

from marketdata_providers.brain import MarketDataBrain, FetchResult
from marketdata_providers.config import MarketDataConfig
from marketdata_providers.base import (
    StockQuote,
    HistoricalPrice,
    OptionQuote,
    CompanyInfo,
    MarketDataProvider,
    MarketDataType
)


class MockProvider(MarketDataProvider):
    """Mock provider for testing"""
    
    def __init__(self, name: str, api_key: str):
        self.name = name
        self.api_key = api_key
        self.fail_next = False
        self.rate_limited = False
    
    async def get_quote(self, symbol: str) -> StockQuote:
        if self.fail_next:
            raise Exception("Provider failed")
        if self.rate_limited:
            raise Exception("Rate limit exceeded - 429")
        
        return StockQuote(
            symbol=symbol,
            price=Decimal("100.00"),
            change=Decimal("2.50"),
            change_percent=Decimal("2.56"),
            volume=1000000
        )
    
    async def get_historical(self, symbol: str, start_date: date, end_date: date, interval: str = "1d"):
        if self.fail_next:
            raise Exception("Provider failed")
        if self.rate_limited:
            raise Exception("Rate limit exceeded")
        
        return [
            HistoricalPrice(
                symbol=symbol,
                date=start_date,
                open=Decimal("98.00"),
                high=Decimal("102.00"),
                low=Decimal("97.00"),
                close=Decimal("100.00"),
                volume=1000000
            )
        ]
    
    async def get_company_info(self, symbol: str) -> CompanyInfo:
        if self.fail_next:
            raise Exception("Provider failed")
        if self.rate_limited:
            raise Exception("Too many requests")
        
        return CompanyInfo(
            symbol=symbol,
            name=f"{symbol} Company",
            description="Test company",
            sector="Technology",
            industry="Software",
            market_cap=1000000000,
            employees=10000
        )


class TestFetchResult:
    """Test FetchResult container"""
    
    def test_fetch_result_success(self):
        """Test successful FetchResult"""
        data = {"test": "data"}
        result = FetchResult(data=data, provider="test_provider")
        
        assert result.data == data
        assert result.provider == "test_provider"
        assert result.success is True
        assert result.error is None
        assert isinstance(result.timestamp, datetime)
    
    def test_fetch_result_failure(self):
        """Test failed FetchResult"""
        result = FetchResult(
            data=None, 
            provider="test_provider", 
            success=False, 
            error="Test error"
        )
        
        assert result.data is None
        assert result.provider == "test_provider"
        assert result.success is False
        assert result.error == "Test error"


class TestMarketDataBrain:
    """Test MarketDataBrain functionality"""
    
    @pytest.fixture
    def mock_config(self):
        """Create a mock configuration"""
        config = Mock(spec=MarketDataConfig)
        config.cache_ttl_seconds = 300
        config.enable_caching = True
        config.get_enabled_providers.return_value = ['mock_provider_1', 'mock_provider_2']
        
        # Mock provider configs
        mock_provider_config = Mock()
        mock_provider_config.enabled = True
        mock_provider_config.api_key = "test_key"
        
        config.alpha_vantage = mock_provider_config
        config.finnhub = mock_provider_config
        config.polygon = mock_provider_config
        config.twelve_data = mock_provider_config
        config.fmp = mock_provider_config
        config.tiingo = mock_provider_config
        config.api_ninjas = mock_provider_config
        config.fiscal = mock_provider_config
        config.fred = mock_provider_config
        config.newsapi = mock_provider_config
        config.newsapi_ai = mock_provider_config
        config.currents_api = mock_provider_config
        config.mediastack = mock_provider_config
        config.gnews = mock_provider_config
        
        return config
    
    @pytest.fixture
    def brain_with_mocks(self, mock_config):
        """Create brain with mock providers"""
        brain = MarketDataBrain(config=mock_config)
        
        # Replace providers with mocks
        brain.providers = {
            'mock_provider_1': MockProvider("MockProvider1", "key1"),
            'mock_provider_2': MockProvider("MockProvider2", "key2")
        }
        
        return brain
    
    def test_brain_initialization(self, mock_config):
        """Test brain initialization"""
        brain = MarketDataBrain(config=mock_config)
        
        assert brain.config == mock_config
        assert isinstance(brain.providers, dict)
        assert isinstance(brain.rate_limited_providers, dict)
        assert isinstance(brain.cache, dict)
        assert brain.cache_ttl == mock_config.cache_ttl_seconds
    
    def test_brain_initialization_without_config(self):
        """Test brain initialization without config (uses env)"""
        with patch('marketdata_providers.brain.MarketDataConfig.from_env') as mock_from_env:
            mock_config = Mock()
            mock_config.cache_ttl_seconds = 300
            mock_config.enable_caching = True
            mock_config.get_enabled_providers.return_value = []
            
            # Mock all provider configs
            mock_provider_config = Mock()
            mock_provider_config.enabled = False
            mock_provider_config.api_key = None
            
            for provider_name in ['alpha_vantage', 'finnhub', 'polygon', 'twelve_data', 
                                'fmp', 'tiingo', 'api_ninjas', 'fiscal', 'fred', 
                                'newsapi', 'newsapi_ai', 'currents_api', 'mediastack', 'gnews']:
                setattr(mock_config, provider_name, mock_provider_config)
            
            mock_from_env.return_value = mock_config
            
            brain = MarketDataBrain()
            assert brain.config == mock_config
    
    @pytest.mark.asyncio
    async def test_get_quote_success(self, brain_with_mocks):
        """Test successful quote fetching"""
        result = await brain_with_mocks.get_quote("AAPL")
        
        assert result.success is True
        assert result.provider == 'mock_provider_1'
        assert isinstance(result.data, StockQuote)
        assert result.data.symbol == "AAPL"
        assert result.data.price == Decimal("100.00")
    
    @pytest.mark.asyncio
    async def test_get_quote_with_fallback(self, brain_with_mocks):
        """Test quote fetching with provider fallback"""
        # Make first provider fail
        brain_with_mocks.providers['mock_provider_1'].fail_next = True
        
        result = await brain_with_mocks.get_quote("AAPL")
        
        assert result.success is True
        assert result.provider == 'mock_provider_2'  # Fallback provider
        assert isinstance(result.data, StockQuote)
    
    @pytest.mark.asyncio
    async def test_get_quote_all_providers_fail(self, brain_with_mocks):
        """Test quote fetching when all providers fail"""
        # Make all providers fail
        for provider in brain_with_mocks.providers.values():
            provider.fail_next = True
        
        result = await brain_with_mocks.get_quote("AAPL")
        
        assert result.success is False
        assert result.provider == "none"
        assert result.data is None
        assert "All providers failed" in result.error
    
    @pytest.mark.asyncio
    async def test_rate_limiting_detection(self, brain_with_mocks):
        """Test rate limiting detection and provider marking"""
        # Make first provider rate limited
        brain_with_mocks.providers['mock_provider_1'].rate_limited = True
        
        result = await brain_with_mocks.get_quote("AAPL")
        
        # Should succeed with second provider
        assert result.success is True
        assert result.provider == 'mock_provider_2'
        
        # First provider should be marked as rate limited
        assert 'mock_provider_1' in brain_with_mocks.rate_limited_providers
    
    @pytest.mark.asyncio
    async def test_caching_functionality(self, brain_with_mocks):
        """Test caching functionality"""
        # First call - should hit provider
        result1 = await brain_with_mocks.get_quote("AAPL")
        assert result1.success is True
        
        # Make provider fail for next call
        for provider in brain_with_mocks.providers.values():
            provider.fail_next = True
        
        # Second call - should return cached result
        result2 = await brain_with_mocks.get_quote("AAPL")
        assert result2.success is True  # Should still succeed due to cache
        assert result2.data.symbol == "AAPL"
    
    @pytest.mark.asyncio
    async def test_cache_expiration(self, brain_with_mocks):
        """Test cache expiration"""
        # Set very short cache TTL
        brain_with_mocks.cache_ttl = 0.1
        
        # First call
        result1 = await brain_with_mocks.get_quote("AAPL")
        assert result1.success is True
        
        # Wait for cache to expire
        await asyncio.sleep(0.2)
        
        # Make provider fail
        for provider in brain_with_mocks.providers.values():
            provider.fail_next = True
        
        # Second call - cache should be expired, so this should fail
        result2 = await brain_with_mocks.get_quote("AAPL")
        assert result2.success is False
    
    @pytest.mark.asyncio
    async def test_get_historical_data(self, brain_with_mocks):
        """Test historical data fetching"""
        start_date = date(2023, 1, 1)
        end_date = date(2023, 1, 31)
        
        result = await brain_with_mocks.get_historical("AAPL", start_date, end_date)
        
        assert result.success is True
        assert isinstance(result.data, list)
        assert len(result.data) > 0
        assert isinstance(result.data[0], HistoricalPrice)
    
    @pytest.mark.asyncio
    async def test_get_company_info(self, brain_with_mocks):
        """Test company info fetching"""
        result = await brain_with_mocks.get_company_info("AAPL")
        
        assert result.success is True
        assert isinstance(result.data, CompanyInfo)
        assert result.data.symbol == "AAPL"
        assert result.data.name == "AAPL Company"
    
    @pytest.mark.asyncio
    async def test_multiple_quotes(self, brain_with_mocks):
        """Test fetching multiple quotes concurrently"""
        symbols = ["AAPL", "GOOGL", "MSFT"]
        results = await brain_with_mocks.get_multiple_quotes(symbols)
        
        assert len(results) == 3
        for symbol in symbols:
            assert symbol in results
            assert results[symbol].success is True
            assert results[symbol].data.symbol == symbol
    
    @pytest.mark.asyncio
    async def test_multiple_historical(self, brain_with_mocks):
        """Test fetching multiple historical data concurrently"""
        symbols = ["AAPL", "GOOGL"]
        start_date = date(2023, 1, 1)
        end_date = date(2023, 1, 31)
        
        results = await brain_with_mocks.get_multiple_historical(
            symbols, start_date, end_date
        )
        
        assert len(results) == 2
        for symbol in symbols:
            assert symbol in results
            assert results[symbol].success is True
            assert isinstance(results[symbol].data, list)
    
    def test_cache_key_generation(self, brain_with_mocks):
        """Test cache key generation"""
        key1 = brain_with_mocks._get_cache_key("quote", symbol="AAPL")
        key2 = brain_with_mocks._get_cache_key("quote", symbol="GOOGL")
        key3 = brain_with_mocks._get_cache_key("quote", symbol="AAPL")
        
        assert key1 != key2  # Different symbols should have different keys
        assert key1 == key3  # Same parameters should have same key
        assert "quote" in key1
        assert "AAPL" in key1
    
    def test_cache_validity_check(self, brain_with_mocks):
        """Test cache validity checking"""
        # Create recent result
        recent_result = FetchResult(data="test", provider="test")
        assert brain_with_mocks._is_cache_valid(recent_result) is True
        
        # Create old result
        old_result = FetchResult(data="test", provider="test")
        old_result.timestamp = datetime.now() - timedelta(seconds=brain_with_mocks.cache_ttl + 100)
        assert brain_with_mocks._is_cache_valid(old_result) is False
        
        # Test with caching disabled
        brain_with_mocks.config.enable_caching = False
        assert brain_with_mocks._is_cache_valid(recent_result) is False
    
    def test_rate_limit_recovery(self, brain_with_mocks):
        """Test rate limit recovery after time period"""
        provider_name = 'mock_provider_1'
        
        # Mark provider as rate limited
        brain_with_mocks._mark_provider_rate_limited(provider_name)
        assert brain_with_mocks._is_provider_rate_limited(provider_name) is True
        
        # Simulate time passing (mock the datetime)
        with patch('marketdata_providers.brain.datetime') as mock_datetime:
            # Set current time to 2 hours after rate limiting
            rate_limit_time = brain_with_mocks.rate_limited_providers[provider_name]
            future_time = rate_limit_time + timedelta(hours=2)
            mock_datetime.now.return_value = future_time
            
            # Provider should be recovered
            assert brain_with_mocks._is_provider_rate_limited(provider_name) is False
            assert provider_name not in brain_with_mocks.rate_limited_providers
    
    def test_clear_cache(self, brain_with_mocks):
        """Test cache clearing"""
        # Add something to cache
        brain_with_mocks.cache["test_key"] = FetchResult(data="test", provider="test")
        assert len(brain_with_mocks.cache) > 0
        
        # Clear cache
        brain_with_mocks.clear_cache()
        assert len(brain_with_mocks.cache) == 0
    
    def test_get_available_providers(self, brain_with_mocks):
        """Test getting available providers"""
        providers = brain_with_mocks.get_available_providers()
        assert "mock_provider_1" in providers
        assert "mock_provider_2" in providers
    
    @pytest.mark.asyncio
    async def test_initialize_method(self, brain_with_mocks):
        """Test initialize method (compatibility)"""
        # Should not raise any exceptions
        await brain_with_mocks.initialize()
    
    @pytest.mark.asyncio
    async def test_close_method(self, brain_with_mocks):
        """Test close method"""
        # Add close method to mock providers
        for provider in brain_with_mocks.providers.values():
            provider.close = AsyncMock()
        
        await brain_with_mocks.close()
        
        # Verify close was called on all providers
        for provider in brain_with_mocks.providers.values():
            provider.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_close_method_with_error(self, brain_with_mocks):
        """Test close method handles provider errors gracefully"""
        # Make one provider's close method raise an exception
        brain_with_mocks.providers['mock_provider_1'].close = AsyncMock(side_effect=Exception("Close failed"))
        brain_with_mocks.providers['mock_provider_2'].close = AsyncMock()
        
        # Should not raise exception despite provider error
        await brain_with_mocks.close()
        
        # Second provider should still be closed
        brain_with_mocks.providers['mock_provider_2'].close.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
