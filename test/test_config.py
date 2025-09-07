"""Tests for MarketDataConfig and provider configuration"""

import pytest
import os
from unittest.mock import patch, Mock
from marketdata_providers.config import (
    MarketDataConfig,
    ProviderConfig,
    ProviderPriority
)


class TestProviderPriority:
    """Test ProviderPriority enum"""
    
    def test_priority_values(self):
        """Test priority enum values"""
        assert ProviderPriority.HIGH.value == 1
        assert ProviderPriority.MEDIUM.value == 2
        assert ProviderPriority.LOW.value == 3


class TestProviderConfig:
    """Test ProviderConfig model"""
    
    def test_provider_config_defaults(self):
        """Test default ProviderConfig values"""
        config = ProviderConfig()
        
        assert config.enabled is True
        assert config.api_key is None
        assert config.priority == ProviderPriority.MEDIUM
        assert config.rate_limit_per_minute == 60
        assert config.timeout_seconds == 30
        assert config.max_retries == 3
    
    def test_provider_config_custom_values(self):
        """Test ProviderConfig with custom values"""
        config = ProviderConfig(
            enabled=False,
            api_key="test_key_123",
            priority=ProviderPriority.HIGH,
            rate_limit_per_minute=120,
            timeout_seconds=45,
            max_retries=5
        )
        
        assert config.enabled is False
        assert config.api_key == "test_key_123"
        assert config.priority == ProviderPriority.HIGH
        assert config.rate_limit_per_minute == 120
        assert config.timeout_seconds == 45
        assert config.max_retries == 5
    
    def test_provider_config_serialization(self):
        """Test ProviderConfig serialization"""
        config = ProviderConfig(
            enabled=True,
            api_key="test_key",
            priority=ProviderPriority.HIGH
        )
        
        data = config.model_dump()
        
        assert data['enabled'] is True
        assert data['api_key'] == "test_key"
        assert data['priority'] == 1  # Should use enum value


class TestMarketDataConfig:
    """Test MarketDataConfig functionality"""
    
    def test_config_defaults(self):
        """Test default configuration values"""
        with patch.dict(os.environ, {}, clear=True):
            config = MarketDataConfig()
            
            assert config.enable_caching is True
            assert config.cache_ttl_seconds == 300
            assert config.enable_fallback is True
            assert config.fallback_on_error is True
            assert config.log_level == "INFO"
    
    def test_config_with_env_vars(self):
        """Test configuration with environment variables"""
        env_vars = {
            'ALPHA_VANTAGE_API_KEY': 'av_test_key',
            'FINNHUB_API_KEY': 'fh_test_key',
            'POLYGON_API_KEY': 'poly_test_key',
            'TWELVE_DATA_API_KEY': 'td_test_key',
            'FMP_API_KEY': 'fmp_test_key',
            'TIINGO_API_KEY': 'tiingo_test_key',
            'API_NINJAS_API_KEY': 'ninjas_test_key',
            'FISCAL_API_KEY': 'fiscal_test_key',
            'FRED_API_KEY': 'fred_test_key',
            'NEWSAPI_KEY': 'newsapi_test_key',
            'NEWSAPI_AI_KEY': 'newsapi_ai_test_key',
            'CURRENTS_API_KEY': 'currents_test_key',
            'MEDIASTACK_API_KEY': 'mediastack_test_key',
            'GNEWS_API_KEY': 'gnews_test_key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            config = MarketDataConfig()
            
            assert config.alpha_vantage.api_key == 'av_test_key'
            assert config.finnhub.api_key == 'fh_test_key'
            assert config.polygon.api_key == 'poly_test_key'
            assert config.twelve_data.api_key == 'td_test_key'
            assert config.fmp.api_key == 'fmp_test_key'
            assert config.tiingo.api_key == 'tiingo_test_key'
            assert config.api_ninjas.api_key == 'ninjas_test_key'
            assert config.fiscal.api_key == 'fiscal_test_key'
            assert config.fred.api_key == 'fred_test_key'
            assert config.newsapi.api_key == 'newsapi_test_key'
            assert config.newsapi_ai.api_key == 'newsapi_ai_test_key'
            assert config.currents_api.api_key == 'currents_test_key'
            assert config.mediastack.api_key == 'mediastack_test_key'
            assert config.gnews.api_key == 'gnews_test_key'
    
    def test_provider_priorities(self):
        """Test provider priority settings"""
        config = MarketDataConfig()
        
        # Test specific priorities as defined in config
        assert config.alpha_vantage.priority == ProviderPriority.LOW
        assert config.finnhub.priority == ProviderPriority.HIGH
        assert config.polygon.priority == ProviderPriority.HIGH
        assert config.twelve_data.priority == ProviderPriority.MEDIUM
        assert config.fmp.priority == ProviderPriority.MEDIUM
        assert config.tiingo.priority == ProviderPriority.LOW
        assert config.fred.priority == ProviderPriority.HIGH
        assert config.newsapi.priority == ProviderPriority.HIGH
        assert config.newsapi_ai.priority == ProviderPriority.HIGH
        assert config.gnews.priority == ProviderPriority.HIGH
        assert config.yahoo_finance.priority == ProviderPriority.HIGH
    
    def test_provider_rate_limits(self):
        """Test provider rate limit settings"""
        config = MarketDataConfig()
        
        # Test specific rate limits
        assert config.alpha_vantage.rate_limit_per_minute == 5
        assert config.finnhub.rate_limit_per_minute == 60
        assert config.polygon.rate_limit_per_minute == 5
        assert config.twelve_data.rate_limit_per_minute == 8
        assert config.fred.rate_limit_per_minute == 120
        assert config.api_ninjas.rate_limit_per_minute == 200
        assert config.yahoo_finance.rate_limit_per_minute == 2000
    
    def test_from_env_classmethod(self):
        """Test from_env class method"""
        env_vars = {
            'ALPHA_VANTAGE_API_KEY': 'test_av_key',
            'FINNHUB_API_KEY': 'test_fh_key'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            config = MarketDataConfig.from_env()
            
            assert isinstance(config, MarketDataConfig)
            assert config.alpha_vantage.api_key == 'test_av_key'
            assert config.finnhub.api_key == 'test_fh_key'
    
    def test_get_enabled_providers_empty(self):
        """Test get_enabled_providers with no API keys"""
        with patch.dict(os.environ, {}, clear=True):
            config = MarketDataConfig()
            enabled = config.get_enabled_providers()
            
            # Should only include yahoo_finance since it doesn't need an API key
            assert 'yahoo_finance' in enabled
            # Others should not be included without API keys
            assert 'alpha_vantage' not in enabled
            assert 'finnhub' not in enabled
    
    def test_get_enabled_providers_with_keys(self):
        """Test get_enabled_providers with API keys"""
        env_vars = {
            'ALPHA_VANTAGE_API_KEY': 'av_key',
            'FINNHUB_API_KEY': 'fh_key',
            'POLYGON_API_KEY': 'poly_key',
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            config = MarketDataConfig()
            enabled = config.get_enabled_providers()
            
            # Should be sorted by priority (HIGH=1, MEDIUM=2, LOW=3)
            assert 'finnhub' in enabled  # HIGH priority
            assert 'polygon' in enabled  # HIGH priority
            assert 'yahoo_finance' in enabled  # HIGH priority
            assert 'alpha_vantage' in enabled  # LOW priority
            
            # Check priority ordering
            finnhub_index = enabled.index('finnhub')
            alpha_vantage_index = enabled.index('alpha_vantage')
            assert finnhub_index < alpha_vantage_index  # HIGH priority comes before LOW
    
    def test_get_enabled_providers_priority_sorting(self):
        """Test that providers are correctly sorted by priority"""
        env_vars = {
            'ALPHA_VANTAGE_API_KEY': 'av_key',  # LOW priority (3)
            'FINNHUB_API_KEY': 'fh_key',        # HIGH priority (1)
            'TWELVE_DATA_API_KEY': 'td_key',    # MEDIUM priority (2)
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            config = MarketDataConfig()
            enabled = config.get_enabled_providers()
            
            # Find positions of providers
            high_priorities = [p for p in enabled if p in ['finnhub', 'yahoo_finance']]
            medium_priorities = [p for p in enabled if p in ['twelve_data']]
            low_priorities = [p for p in enabled if p in ['alpha_vantage']]
            
            # Verify HIGH priority providers come before MEDIUM and LOW
            if high_priorities and medium_priorities:
                assert enabled.index(high_priorities[0]) < enabled.index(medium_priorities[0])
            if medium_priorities and low_priorities:
                assert enabled.index(medium_priorities[0]) < enabled.index(low_priorities[0])
    
    def test_validate_provider_valid(self):
        """Test validate_provider with valid provider"""
        env_vars = {'FINNHUB_API_KEY': 'valid_key'}
        
        with patch.dict(os.environ, env_vars, clear=True):
            config = MarketDataConfig()
            
            assert config.validate_provider('finnhub') is True
            assert config.validate_provider('yahoo_finance') is True  # Has default API key
    
    def test_validate_provider_invalid(self):
        """Test validate_provider with invalid provider"""
        with patch.dict(os.environ, {}, clear=True):
            config = MarketDataConfig()
            
            assert config.validate_provider('finnhub') is False  # No API key
            assert config.validate_provider('nonexistent') is False  # Provider doesn't exist
    
    def test_validate_provider_disabled(self):
        """Test validate_provider with disabled provider"""
        env_vars = {'FINNHUB_API_KEY': 'valid_key'}
        
        with patch.dict(os.environ, env_vars, clear=True):
            config = MarketDataConfig()
            config.finnhub.enabled = False  # Disable the provider
            
            assert config.validate_provider('finnhub') is False
    
    def test_yahoo_finance_special_case(self):
        """Test Yahoo Finance provider special configuration"""
        config = MarketDataConfig()
        
        # Yahoo Finance should have a default API key and be enabled
        assert config.yahoo_finance.api_key == "yahoo_finance"
        assert config.yahoo_finance.enabled is True
        assert config.yahoo_finance.priority == ProviderPriority.HIGH
        assert config.yahoo_finance.rate_limit_per_minute == 2000
    
    def test_config_model_dump(self):
        """Test configuration serialization"""
        env_vars = {'FINNHUB_API_KEY': 'test_key'}
        
        with patch.dict(os.environ, env_vars, clear=True):
            config = MarketDataConfig()
            data = config.model_dump()
            
            assert isinstance(data, dict)
            assert 'finnhub' in data
            assert 'alpha_vantage' in data
            assert 'enable_caching' in data
            assert data['enable_caching'] is True
            assert data['cache_ttl_seconds'] == 300
            
            # Check provider config structure
            assert isinstance(data['finnhub'], dict)
            assert data['finnhub']['enabled'] is True
            assert data['finnhub']['api_key'] == 'test_key'
    
    def test_provider_config_overrides(self):
        """Test that provider configs can be modified"""
        config = MarketDataConfig()
        
        # Modify a provider config
        config.finnhub.priority = ProviderPriority.LOW
        config.finnhub.rate_limit_per_minute = 30
        config.finnhub.enabled = False
        
        assert config.finnhub.priority == ProviderPriority.LOW
        assert config.finnhub.rate_limit_per_minute == 30
        assert config.finnhub.enabled is False
    
    def test_global_settings(self):
        """Test global configuration settings"""
        config = MarketDataConfig()
        
        # Test modifying global settings
        config.enable_caching = False
        config.cache_ttl_seconds = 600
        config.enable_fallback = False
        config.fallback_on_error = False
        config.log_level = "DEBUG"
        
        assert config.enable_caching is False
        assert config.cache_ttl_seconds == 600
        assert config.enable_fallback is False
        assert config.fallback_on_error is False
        assert config.log_level == "DEBUG"


if __name__ == "__main__":
    pytest.main([__file__])
