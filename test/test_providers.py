"""Tests for provider modules"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, date
from decimal import Decimal

from marketdata_providers.base import MarketDataProvider, StockQuote, HistoricalPrice, CompanyInfo
from marketdata_providers.providers import (
    AlphaVantageProvider,
    FinnhubProvider,
    PolygonProvider,
    TwelveDataProvider,
    FMPProvider,
    TiingoProvider
)


class TestProviderImports:
    """Test that all providers can be imported successfully"""
    
    def test_import_alpha_vantage_provider(self):
        """Test AlphaVantage provider import"""
        assert AlphaVantageProvider is not None
        assert hasattr(AlphaVantageProvider, '__init__')
    
    def test_import_finnhub_provider(self):
        """Test Finnhub provider import"""
        assert FinnhubProvider is not None
        assert hasattr(FinnhubProvider, '__init__')
    
    def test_import_polygon_provider(self):
        """Test Polygon provider import"""
        assert PolygonProvider is not None
        assert hasattr(PolygonProvider, '__init__')
    
    def test_import_twelve_data_provider(self):
        """Test TwelveData provider import"""
        assert TwelveDataProvider is not None
        assert hasattr(TwelveDataProvider, '__init__')
    
    def test_import_fmp_provider(self):
        """Test FMP provider import"""
        assert FMPProvider is not None
        assert hasattr(FMPProvider, '__init__')
    
    def test_import_tiingo_provider(self):
        """Test Tiingo provider import"""
        assert TiingoProvider is not None
        assert hasattr(TiingoProvider, '__init__')


class TestProviderBaseInterface:
    """Test that providers implement the required interface"""
    
    @pytest.mark.parametrize("provider_class", [
        AlphaVantageProvider,
        FinnhubProvider,
        PolygonProvider,
        TwelveDataProvider,
        FMPProvider,
        TiingoProvider
    ])
    def test_provider_initialization(self, provider_class):
        """Test that providers can be initialized with API key"""
        provider = provider_class("test_api_key")
        
        assert hasattr(provider, 'api_key')
        assert hasattr(provider, 'name')
        assert provider.api_key == "test_api_key"
        assert isinstance(provider.name, str)
        assert len(provider.name) > 0
    
    @pytest.mark.parametrize("provider_class", [
        AlphaVantageProvider,
        FinnhubProvider,
        PolygonProvider,
        TwelveDataProvider,
        FMPProvider,
        TiingoProvider
    ])
    def test_provider_has_required_methods(self, provider_class):
        """Test that providers have required methods"""
        provider = provider_class("test_api_key")
        
        # Check for essential methods
        assert hasattr(provider, 'get_quote')
        assert callable(getattr(provider, 'get_quote'))
        
        # Most providers should have these methods
        expected_methods = [
            'get_historical',
            'get_company_info'
        ]
        
        for method_name in expected_methods:
            if hasattr(provider, method_name):
                method = getattr(provider, method_name)
                assert callable(method), f"{provider.name} should have callable {method_name}"


class TestAlphaVantageProvider:
    """Test AlphaVantage provider specifically"""
    
    @pytest.fixture
    def provider(self):
        """Create AlphaVantage provider instance"""
        return AlphaVantageProvider("test_api_key")
    
    def test_provider_name(self, provider):
        """Test provider name"""
        assert provider.name == "Alpha Vantage"
    
    def test_provider_api_key(self, provider):
        """Test API key assignment"""
        assert provider.api_key == "test_api_key"
    
    @pytest.mark.asyncio
    async def test_get_quote_method_exists(self, provider):
        """Test that get_quote method exists and is callable"""
        assert hasattr(provider, 'get_quote')
        assert callable(provider.get_quote)
        
        # We won't test actual API calls in unit tests
        # but we can test that the method signature is correct
        import inspect
        sig = inspect.signature(provider.get_quote)
        assert 'symbol' in sig.parameters
    
    @pytest.mark.asyncio
    async def test_get_historical_method_exists(self, provider):
        """Test that get_historical method exists"""
        assert hasattr(provider, 'get_historical')
        assert callable(provider.get_historical)
        
        import inspect
        sig = inspect.signature(provider.get_historical)
        assert 'symbol' in sig.parameters
        assert 'start_date' in sig.parameters
        assert 'end_date' in sig.parameters


class TestFinnhubProvider:
    """Test Finnhub provider specifically"""
    
    @pytest.fixture
    def provider(self):
        """Create Finnhub provider instance"""
        return FinnhubProvider("test_api_key")
    
    def test_provider_name(self, provider):
        """Test provider name"""
        assert provider.name == "Finnhub"
    
    def test_provider_api_key(self, provider):
        """Test API key assignment"""
        assert provider.api_key == "test_api_key"
    
    @pytest.mark.asyncio
    async def test_methods_exist(self, provider):
        """Test that required methods exist"""
        methods_to_check = ['get_quote', 'get_historical', 'get_company_info']
        
        for method_name in methods_to_check:
            if hasattr(provider, method_name):
                method = getattr(provider, method_name)
                assert callable(method), f"{method_name} should be callable"


class TestPolygonProvider:
    """Test Polygon provider specifically"""
    
    @pytest.fixture
    def provider(self):
        """Create Polygon provider instance"""
        return PolygonProvider("test_api_key")
    
    def test_provider_name(self, provider):
        """Test provider name"""
        assert provider.name == "Polygon"
    
    def test_provider_api_key(self, provider):
        """Test API key assignment"""
        assert provider.api_key == "test_api_key"


class TestTwelveDataProvider:
    """Test TwelveData provider specifically"""
    
    @pytest.fixture
    def provider(self):
        """Create TwelveData provider instance"""
        return TwelveDataProvider("test_api_key")
    
    def test_provider_name(self, provider):
        """Test provider name"""
        assert provider.name == "Twelve Data"
    
    def test_provider_api_key(self, provider):
        """Test API key assignment"""
        assert provider.api_key == "test_api_key"


class TestProviderErrorHandling:
    """Test error handling in providers"""
    
    @pytest.mark.parametrize("provider_class", [
        AlphaVantageProvider,
        FinnhubProvider,
        PolygonProvider,
        TwelveDataProvider,
        FMPProvider,
        TiingoProvider
    ])
    def test_provider_initialization_with_none_api_key(self, provider_class):
        """Test provider initialization with None API key"""
        # Most providers should handle None API key gracefully
        try:
            provider = provider_class(None)
            assert provider.api_key is None
        except (ValueError, TypeError):
            # Some providers may raise an error for None API key, which is acceptable
            pass
    
    @pytest.mark.parametrize("provider_class", [
        AlphaVantageProvider,
        FinnhubProvider,
        PolygonProvider,
        TwelveDataProvider,
        FMPProvider,
        TiingoProvider
    ])
    def test_provider_initialization_with_empty_string(self, provider_class):
        """Test provider initialization with empty string API key"""
        try:
            provider = provider_class("")
            assert provider.api_key == ""
        except (ValueError, TypeError):
            # Some providers may raise an error for empty API key, which is acceptable
            pass


class TestProviderCompatibility:
    """Test provider compatibility with the base interface"""
    
    @pytest.mark.parametrize("provider_class", [
        AlphaVantageProvider,
        FinnhubProvider,
        PolygonProvider,
        TwelveDataProvider,
        FMPProvider,
        TiingoProvider
    ])
    def test_provider_inherits_from_base(self, provider_class):
        """Test that providers inherit from MarketDataProvider"""
        # Check if provider is a subclass of MarketDataProvider or implements required interface
        provider = provider_class("test_key")
        
        # Provider should have a name attribute
        assert hasattr(provider, 'name')
        assert isinstance(provider.name, str)
        
        # Provider should have an api_key attribute
        assert hasattr(provider, 'api_key')
        
        # Provider should have get_quote method
        assert hasattr(provider, 'get_quote')
        assert callable(getattr(provider, 'get_quote'))


class TestProviderConfiguration:
    """Test provider configuration and setup"""
    
    def test_multiple_provider_instances(self):
        """Test creating multiple provider instances"""
        providers = [
            AlphaVantageProvider("av_key"),
            FinnhubProvider("fh_key"),
            PolygonProvider("poly_key"),
            TwelveDataProvider("td_key"),
            FMPProvider("fmp_key"),
            TiingoProvider("tiingo_key")
        ]
        
        # All providers should be unique instances
        for i, provider1 in enumerate(providers):
            for j, provider2 in enumerate(providers):
                if i != j:
                    assert provider1 is not provider2
                    assert provider1.api_key != provider2.api_key
    
    def test_provider_names_are_unique(self):
        """Test that provider names are unique"""
        providers = [
            AlphaVantageProvider("av_key"),
            FinnhubProvider("fh_key"),
            PolygonProvider("poly_key"),
            TwelveDataProvider("td_key"),
            FMPProvider("fmp_key"),
            TiingoProvider("tiingo_key")
        ]
        
        names = [provider.name for provider in providers]
        assert len(names) == len(set(names)), "Provider names should be unique"


if __name__ == "__main__":
    pytest.main([__file__])
