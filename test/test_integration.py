"""Integration tests for the marketdata_providers package"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from datetime import date, datetime, timedelta
from decimal import Decimal

from marketdata_providers import (
    MarketDataBrain,
    MarketDataConfig
)
from marketdata_providers.base import (
    MarketDataProvider,
    MarketDataType,
    StockQuote,
    HistoricalPrice,
    CompanyInfo
)
from marketdata_providers.data_formatter import DataFormattingService


class TestPackageIntegration:
    """Test full package integration and functionality"""
    
    def test_package_imports(self):
        """Test that all main package components can be imported"""
        # Test main imports work
        assert MarketDataBrain is not None
        assert MarketDataConfig is not None
        assert MarketDataProvider is not None
        assert MarketDataType is not None
        assert StockQuote is not None
        assert HistoricalPrice is not None
        assert CompanyInfo is not None
        assert DataFormattingService is not None
    
    def test_enum_integration(self):
        """Test that enums work correctly"""
        # Test MarketDataType enum
        assert MarketDataType.QUOTE.value == "quote"
        assert MarketDataType.HISTORICAL.value == "historical"
        assert MarketDataType.COMPANY_INFO.value == "company_info"
        
        # Test enum can be used in comparisons
        assert MarketDataType.QUOTE == MarketDataType.QUOTE
        assert MarketDataType.QUOTE != MarketDataType.HISTORICAL
    
    def test_config_creation(self):
        """Test configuration creation works"""
        # Test config can be created
        config = MarketDataConfig()
        assert config is not None
        
        # Test config has expected attributes
        assert hasattr(config, 'enable_caching')
        assert hasattr(config, 'cache_ttl_seconds')
        assert hasattr(config, 'alpha_vantage')
        assert hasattr(config, 'finnhub')
        assert hasattr(config, 'polygon')
        
        # Test methods work
        enabled_providers = config.get_enabled_providers()
        assert isinstance(enabled_providers, list)
    
    def test_brain_creation(self):
        """Test Brain creation and initialization"""
        # Create config first
        config = MarketDataConfig()
        
        # Test brain can be created with config
        brain = MarketDataBrain(config=config)
        assert brain is not None
        assert brain.config == config
        
        # Test brain methods exist
        assert hasattr(brain, 'get_quote')
        assert hasattr(brain, 'get_historical')
        assert hasattr(brain, 'get_company_info')
        assert hasattr(brain, 'get_multiple_quotes')
        
        # Test utility methods
        available_providers = brain.get_available_providers()
        assert isinstance(available_providers, list)
        
        provider_status = brain.get_provider_status()
        assert isinstance(provider_status, dict)
    
    def test_data_models_creation(self):
        """Test that data models can be created and work correctly"""
        # Test StockQuote
        quote = StockQuote(
            symbol="AAPL",
            price=Decimal("150.25"),
            change=Decimal("2.50"),
            change_percent=Decimal("1.69"),
            volume=1000000
        )
        assert quote.symbol == "AAPL"
        assert quote.price == Decimal("150.25")
        
        # Test model serialization
        quote_dict = quote.model_dump()
        assert isinstance(quote_dict, dict)
        assert quote_dict['symbol'] == "AAPL"
        
        # Test HistoricalPrice
        historical = HistoricalPrice(
            symbol="AAPL",
            date=date(2023, 1, 15),
            open=Decimal("148.00"),
            high=Decimal("151.00"),
            low=Decimal("147.50"),
            close=Decimal("150.25"),
            volume=1000000
        )
        assert historical.symbol == "AAPL"
        assert historical.date == date(2023, 1, 15)
        
        # Test CompanyInfo
        company = CompanyInfo(
            symbol="AAPL",
            name="Apple Inc.",
            description="Technology company",
            sector="Technology",
            industry="Consumer Electronics",
            market_cap=2500000000000,
            employees=164000
        )
        assert company.symbol == "AAPL"
        assert company.name == "Apple Inc."
    
    def test_data_formatter_integration(self):
        """Test data formatter integration with Brain"""
        # Create mock brain
        mock_brain = Mock()
        
        # Test formatter can be created
        formatter = DataFormattingService(brain=mock_brain)
        assert formatter is not None
        assert formatter.brain == mock_brain
        
        # Test formatter methods exist
        assert hasattr(formatter, 'format_quote_data')
        assert hasattr(formatter, 'format_historical_data')
        assert hasattr(formatter, 'format_company_info')
        assert hasattr(formatter, 'batch_format_quotes')
    
    @pytest.mark.asyncio
    async def test_brain_async_methods(self):
        """Test that Brain async methods work"""
        # Create brain with mock config
        config = MarketDataConfig()
        brain = MarketDataBrain(config=config)
        
        # Test initialize method (should not raise)
        await brain.initialize()
        
        # Test close method (should not raise)
        await brain.close()
    
    def test_provider_priority_system(self):
        """Test that provider priority system works"""
        from marketdata_providers.config import ProviderPriority
        
        # Test enum values
        assert ProviderPriority.HIGH.value == 1
        assert ProviderPriority.MEDIUM.value == 2
        assert ProviderPriority.LOW.value == 3
        
        # Test in config
        config = MarketDataConfig()
        
        # High priority providers
        assert config.finnhub.priority == ProviderPriority.HIGH
        assert config.polygon.priority == ProviderPriority.HIGH
        
        # Medium priority providers
        assert config.twelve_data.priority == ProviderPriority.MEDIUM
        assert config.fmp.priority == ProviderPriority.MEDIUM
        
        # Low priority providers
        assert config.alpha_vantage.priority == ProviderPriority.LOW
        assert config.tiingo.priority == ProviderPriority.LOW
    
    def test_cache_system_integration(self):
        """Test cache system works correctly"""
        config = MarketDataConfig()
        brain = MarketDataBrain(config=config)
        
        # Test cache settings
        assert brain.cache_ttl == config.cache_ttl_seconds
        assert isinstance(brain.cache, dict)
        
        # Test cache methods
        brain.clear_cache()
        assert len(brain.cache) == 0
        
        # Test cache key generation
        cache_key = brain._get_cache_key("quote", symbol="AAPL")
        assert isinstance(cache_key, str)
        assert "quote" in cache_key
        assert "AAPL" in cache_key
    
    def test_rate_limiting_system(self):
        """Test rate limiting system integration"""
        config = MarketDataConfig()
        brain = MarketDataBrain(config=config)
        
        # Test rate limiting attributes exist
        assert hasattr(brain, 'rate_limited_providers')
        assert isinstance(brain.rate_limited_providers, dict)
        
        # Test rate limiting methods
        assert hasattr(brain, '_is_provider_rate_limited')
        assert hasattr(brain, '_mark_provider_rate_limited')
        
        # Test marking provider as rate limited
        brain._mark_provider_rate_limited('test_provider')
        assert 'test_provider' in brain.rate_limited_providers
        
        # Test checking rate limit status
        is_limited = brain._is_provider_rate_limited('test_provider')
        assert is_limited is True
    
    def test_error_handling_integration(self):
        """Test error handling across the system"""
        from marketdata_providers.brain import FetchResult
        
        # Test FetchResult for errors
        error_result = FetchResult(
            data=None,
            provider="test_provider",
            success=False,
            error="Test error message"
        )
        
        assert error_result.success is False
        assert error_result.error == "Test error message"
        assert error_result.data is None
        
        # Test successful result
        success_result = FetchResult(
            data={"test": "data"},
            provider="test_provider",
            success=True
        )
        
        assert success_result.success is True
        assert success_result.error is None
        assert success_result.data == {"test": "data"}
    
    def test_package_version_and_metadata(self):
        """Test package metadata is accessible"""
        # Test that package can be imported
        import marketdata_providers
        
        # Test main exports
        assert hasattr(marketdata_providers, 'MarketDataBrain')
        assert hasattr(marketdata_providers, 'MarketDataConfig')
        assert hasattr(marketdata_providers, 'MarketDataType')
        
        # Test __all__ exists and is properly defined
        if hasattr(marketdata_providers, '__all__'):
            all_exports = marketdata_providers.__all__
            assert isinstance(all_exports, list)
            assert len(all_exports) > 0
    
    def test_decimal_precision_handling(self):
        """Test that Decimal precision is handled correctly throughout"""
        # Test in models
        quote = StockQuote(
            symbol="TEST",
            price=Decimal("123.456789"),
            change=Decimal("-0.000001"),
            change_percent=Decimal("0.123456"),
            volume=1000000
        )
        
        # Decimals should be preserved
        assert isinstance(quote.price, Decimal)
        assert isinstance(quote.change, Decimal)
        assert isinstance(quote.change_percent, Decimal)
        
        # Test precision is maintained
        assert str(quote.price) == "123.456789"
        assert str(quote.change) == "-0.000001"
        assert str(quote.change_percent) == "0.123456"
    
    def test_date_handling_integration(self):
        """Test date handling across the system"""
        from datetime import date, datetime
        
        # Test with HistoricalPrice
        test_date = date(2023, 6, 15)
        historical = HistoricalPrice(
            symbol="TEST",
            date=test_date,
            open=Decimal("100.00"),
            high=Decimal("101.00"),
            low=Decimal("99.00"),
            close=Decimal("100.50"),
            volume=1000000
        )
        
        assert historical.date == test_date
        assert isinstance(historical.date, date)
        
        # Test serialization preserves date format
        serialized = historical.model_dump()
        # Dates should be serialized properly by Pydantic
        assert 'date' in serialized


if __name__ == "__main__":
    pytest.main([__file__])
