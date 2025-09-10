"""Market Data Brain - Central Orchestrator with multi-provider aggregation"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union, Type, Set
from datetime import datetime, date, timedelta
from decimal import Decimal
from enum import Enum
from collections import defaultdict
import statistics

from .base import (
    MarketDataProvider,
    MarketDataType,
    StockQuote,
    HistoricalPrice,
    OptionQuote,
    CompanyInfo,
    EconomicEvent,
    EarningsCalendar,
    EarningsCallTranscript,
    DividendRecord,
    NewsArticle,
    EarningsSurprise,
    StockSplit,
    IPOCalendar,
    AnalystEstimates,
    MarketHoliday,
    TechnicalIndicator,
    ForexQuote,
    CryptoQuote,
    MarketIndex,
    ExchangeInfo,
    MarketConditions,
    TiingoFundamentalData,
    Logo,
    ExchangeRate,
    CurrencyConversion,
    MarketMover,
    SimplePrice,
    EodPrice,
    SupportedSymbol,
    ForexPair,
    Cryptocurrency,
    MarketStatus
)
from .config import MarketDataConfig
from .providers import (
    AlphaVantageProvider,
    FinnhubProvider,
    PolygonProvider,
    TwelveDataProvider,
    FMPProvider,
    TiingoProvider,
    APINinjasProvider,
    FiscalAIProvider,
    FREDProvider,
    NewsAPIProvider,
    NewsAPIAIProvider,
    CurrentsAPIProvider,
    MediaStackProvider,
    GNewsProvider
)

logger = logging.getLogger(__name__)


class ProviderResult:
    """Result container for single provider fetch operations"""
    def __init__(self, data: Any, provider: str, success: bool = True, error: Optional[str] = None):
        self.data = data
        self.provider = provider
        self.success = success
        self.error = error
        self.timestamp = datetime.now()


class AggregatedResult:
    """Result container for aggregated multi-provider data"""
    def __init__(self, data: Any, providers_used: List[str], success: bool = True, 
                 error: Optional[str] = None, provider_results: Optional[Dict[str, ProviderResult]] = None):
        self.data = data
        self.providers_used = providers_used
        self.success = success
        self.error = error
        self.provider_results = provider_results or {}
        self.timestamp = datetime.now()
        self.coverage_percentage = self._calculate_coverage()
    
    def _calculate_coverage(self) -> float:
        """Calculate data coverage percentage based on successful providers"""
        if not self.provider_results:
            return 0.0
        successful = len([r for r in self.provider_results.values() if r.success and r.data is not None])
        total = len(self.provider_results)
        return (successful / total) * 100 if total > 0 else 0.0


class MarketDataBrain:
    """
    The Brain of the market data system - orchestrates concurrent data fetching across all providers 
    and intelligently aggregates results for maximum data coverage.

    This class manages multiple market data providers, fetches from all simultaneously,
    and combines the results to provide the most comprehensive and accurate data possible.
    """

    def __init__(self, config: Optional[MarketDataConfig] = None):
        """
        Initialize the Brain with configuration.

        Args:
            config: MarketDataConfig object or None (will use env vars)
        """
        self.config = config or MarketDataConfig.from_env()
        self.providers: Dict[str, MarketDataProvider] = {}
        self.rate_limited_providers: Dict[str, datetime] = {}  # Track rate-limited providers
        self._initialize_providers()
        self.cache: Dict[str, AggregatedResult] = {}
        self.cache_ttl = self.config.cache_ttl_seconds
        self.aggregation_strategies = self._initialize_aggregation_strategies()

    async def initialize(self):
        """Initialize the brain (for compatibility with test scripts)"""
        # Brain is already initialized in __init__, this is just for compatibility
        pass

    async def close(self):
        """Close all provider connections"""
        for provider in self.providers.values():
            if hasattr(provider, 'close'):
                try:
                    await provider.close()
                except Exception as e:
                    logger.warning(f"Error closing provider {provider.name}: {e}")

    def _is_provider_rate_limited(self, provider_name: str) -> bool:
        """Check if a provider is currently rate limited"""
        if provider_name in self.rate_limited_providers:
            rate_limit_time = self.rate_limited_providers[provider_name]
            # Re-enable provider after 1 hour
            if (datetime.now() - rate_limit_time).total_seconds() > 3600:
                del self.rate_limited_providers[provider_name]
                logger.info(f"Brain re-enabled rate-limited provider: {provider_name}")
                return False
            return True
        return False

    def _mark_provider_rate_limited(self, provider_name: str):
        """Mark a provider as rate limited"""
        self.rate_limited_providers[provider_name] = datetime.now()
        logger.warning(f"Brain marked provider as rate limited: {provider_name}")

    def _initialize_providers(self):
        """Initialize all enabled providers"""
        provider_classes = {
            'alpha_vantage': AlphaVantageProvider,
            'finnhub': FinnhubProvider,
            'polygon': PolygonProvider,
            'twelve_data': TwelveDataProvider,
            'fmp': FMPProvider,
            'tiingo': TiingoProvider,
            'api_ninjas': APINinjasProvider,
            'fiscal': FiscalAIProvider,
            'fred': FREDProvider,
            'newsapi': NewsAPIProvider,
            'newsapi_ai': NewsAPIAIProvider,
            'currents_api': CurrentsAPIProvider,
            'mediastack': MediaStackProvider,
            'gnews': GNewsProvider
        }

        for provider_name, provider_class in provider_classes.items():
            provider_config = getattr(self.config, provider_name)
            if provider_config.enabled and provider_config.api_key:
                try:
                    self.providers[provider_name] = provider_class(provider_config.api_key)
                    logger.info(f"Brain initialized {provider_name} provider")
                except Exception as e:
                    logger.error(f"Brain failed to initialize {provider_name}: {e}")

    def _get_cache_key(self, data_type: str, **kwargs) -> str:
        """Generate cache key for a request"""
        params = "_".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
        return f"{data_type}_{params}"

    def _is_cache_valid(self, result: AggregatedResult) -> bool:
        """Check if cached result is still valid"""
        if not self.config.enable_caching:
            return False

        age = (datetime.now() - result.timestamp).total_seconds()
        return age < self.cache_ttl
    
    def _initialize_aggregation_strategies(self) -> Dict[str, callable]:
        """Initialize data aggregation strategies for different data types"""
        return {
            'quote': self._aggregate_quotes,
            'historical': self._aggregate_historical,
            'options_chain': self._aggregate_options,
            'company_info': self._aggregate_company_info,
            'economic_events': self._aggregate_economic_events,
            'earnings_calendar': self._aggregate_earnings_calendar,
            'news': self._aggregate_news,
            'fundamentals': self._aggregate_fundamentals,
            'earnings': self._aggregate_earnings,
            'dividends': self._aggregate_dividends,
            'intraday': self._aggregate_historical,  # Same as historical
            'technical_indicators': self._aggregate_technical_indicators,
            'economic_data': self._aggregate_economic_data,
            'earnings_transcript': self._aggregate_earnings_transcript,
            'market_status': self._aggregate_market_status,
        }

    async def _try_provider(
        self,
        provider: MarketDataProvider,
        method_name: str,
        **kwargs
    ) -> ProviderResult:
        """Try to fetch data from a single provider"""
        try:
            method = getattr(provider, method_name)
            result = await method(**kwargs)
            if result is not None:
                logger.info(f"Brain successfully fetched {method_name} from {provider.name}")
                return ProviderResult(data=result, provider=provider.name.lower(), success=True)
            else:
                return ProviderResult(data=None, provider=provider.name.lower(), success=False, 
                                    error="No data returned")
        except Exception as e:
            error_msg = str(e).lower()

            # Check for rate limit indicators
            if any(indicator in error_msg for indicator in [
                'rate limit', 'too many requests', '429', 'quota exceeded',
                'api key limit', 'daily limit exceeded', '25 requests per day'
            ]):
                self._mark_provider_rate_limited(provider.name.lower())
                logger.warning(f"Brain detected rate limit from {provider.name}: {e}")

            logger.error(f"Brain error fetching {method_name} from {provider.name}: {e}")
            return ProviderResult(data=None, provider=provider.name.lower(), success=False, error=str(e))

    async def _fetch_from_all_providers(
        self,
        method_name: str,
        data_type: str,
        **kwargs
    ) -> AggregatedResult:
        """
        Fetch data from all available providers concurrently and aggregate results.

        Args:
            method_name: Name of the method to call on providers
            data_type: Type of data being fetched (for caching and aggregation)
            **kwargs: Arguments to pass to the method

        Returns:
            AggregatedResult with aggregated data from all providers
        """
        # Check cache first
        cache_key = self._get_cache_key(data_type, **kwargs)
        if cache_key in self.cache:
            cached_result = self.cache[cache_key]
            if self._is_cache_valid(cached_result):
                logger.info(f"Brain returning cached aggregated {data_type} data (coverage: {cached_result.coverage_percentage:.1f}%)")
                return cached_result

        # Get all enabled providers (including rate-limited ones for maximum coverage)
        enabled_providers = self.config.get_enabled_providers()
        available_providers = [provider for provider in enabled_providers if provider in self.providers]

        if not available_providers:
            return AggregatedResult(
                data=None,
                providers_used=[],
                success=False,
                error="No providers available"
            )

        logger.info(f"Brain fetching {data_type} from all available providers: {available_providers}")

        # Fetch from all providers concurrently
        tasks = []
        for provider_name in available_providers:
            provider = self.providers[provider_name]
            task = self._try_provider(provider, method_name, **kwargs)
            tasks.append(task)

        # Wait for all providers to complete (or timeout)
        try:
            provider_results = await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            logger.error(f"Brain error during concurrent fetching: {e}")
            return AggregatedResult(
                data=None,
                providers_used=[],
                success=False,
                error=f"Concurrent fetching failed: {str(e)}"
            )

        # Process results and handle exceptions
        processed_results = {}
        for i, result in enumerate(provider_results):
            provider_name = available_providers[i]
            if isinstance(result, Exception):
                logger.error(f"Brain exception from {provider_name}: {result}")
                processed_results[provider_name] = ProviderResult(
                    data=None, 
                    provider=provider_name, 
                    success=False, 
                    error=str(result)
                )
            else:
                processed_results[provider_name] = result

        # Get successful results
        successful_results = {
            name: result for name, result in processed_results.items() 
            if result.success and result.data is not None
        }

        if not successful_results:
            logger.warning(f"Brain: No providers returned data for {data_type}")
            return AggregatedResult(
                data=None,
                providers_used=[],
                success=False,
                error="All providers failed to return data",
                provider_results=processed_results
            )

        # Aggregate the successful results
        aggregation_func = self.aggregation_strategies.get(data_type, self._default_aggregation)
        try:
            aggregated_data = aggregation_func(successful_results)
        except Exception as e:
            logger.error(f"Brain aggregation error for {data_type}: {e}")
            # Fallback to best single result
            best_result = next(iter(successful_results.values()))
            aggregated_data = best_result.data

        providers_used = list(successful_results.keys())
        result = AggregatedResult(
            data=aggregated_data,
            providers_used=providers_used,
            success=True,
            provider_results=processed_results
        )

        logger.info(f"Brain aggregated {data_type} from {len(providers_used)} providers (coverage: {result.coverage_percentage:.1f}%)")

        # Cache successful result
        if self.config.enable_caching:
            self.cache[cache_key] = result

        return result

    # Aggregation functions for different data types
    
    def _default_aggregation(self, successful_results: Dict[str, ProviderResult]) -> Any:
        """Default aggregation: return the first successful result"""
        return next(iter(successful_results.values())).data
    
    def _aggregate_quotes(self, successful_results: Dict[str, ProviderResult]) -> StockQuote:
        """Aggregate stock quotes from multiple providers"""
        quotes = [result.data for result in successful_results.values()]
        
        # Use the most recent timestamp and best available data
        primary_quote = max(quotes, key=lambda q: q.timestamp)
        
        # Aggregate numeric fields using median for price accuracy
        prices = [q.price for q in quotes if q.price]
        volumes = [q.volume for q in quotes if q.volume]
        
        if len(prices) > 1:
            # Use median price for accuracy across providers
            primary_quote.price = Decimal(str(statistics.median(float(p) for p in prices)))
        
        if len(volumes) > 1:
            # Use maximum volume as it's often the most complete
            primary_quote.volume = max(volumes)
            
        # Combine extended data from all providers
        for quote in quotes:
            if quote != primary_quote:
                # Fill in missing fields from other providers
                for field in ['market_cap', 'pe_ratio', 'week_52_high', 'week_52_low', 
                            'avg_volume', 'day_high', 'day_low']:
                    if not getattr(primary_quote, field) and getattr(quote, field):
                        setattr(primary_quote, field, getattr(quote, field))
        
        return primary_quote
    
    def _aggregate_historical(self, successful_results: Dict[str, ProviderResult]) -> List[HistoricalPrice]:
        """Aggregate historical price data from multiple providers"""
        all_prices = []
        for result in successful_results.values():
            if isinstance(result.data, list):
                all_prices.extend(result.data)
        
        # Group by date and merge data
        price_by_date = defaultdict(list)
        for price in all_prices:
            date_key = price.date.strftime('%Y-%m-%d') if hasattr(price.date, 'strftime') else str(price.date)
            price_by_date[date_key].append(price)
        
        # Create consolidated prices
        consolidated = []
        for date_key, prices in price_by_date.items():
            if len(prices) == 1:
                consolidated.append(prices[0])
            else:
                # Merge multiple prices for the same date
                primary = prices[0]
                # Use the adjusted close from the provider that has it
                for price in prices:
                    if price.adjusted_close and not primary.adjusted_close:
                        primary.adjusted_close = price.adjusted_close
                    if price.dividend and not primary.dividend:
                        primary.dividend = price.dividend
                    if price.split and not primary.split:
                        primary.split = price.split
                consolidated.append(primary)
        
        # Sort by date
        consolidated.sort(key=lambda p: p.date)
        return consolidated
    
    def _aggregate_options(self, successful_results: Dict[str, ProviderResult]) -> List[OptionQuote]:
        """Aggregate options data from multiple providers"""
        all_options = []
        for result in successful_results.values():
            if isinstance(result.data, list):
                all_options.extend(result.data)
        
        # Remove duplicates by strike and expiration
        seen = set()
        unique_options = []
        for option in all_options:
            key = (option.strike or option.strike_price, option.expiration or option.expiration_date, option.option_type)
            if key not in seen:
                seen.add(key)
                unique_options.append(option)
        
        return unique_options
    
    def _aggregate_company_info(self, successful_results: Dict[str, ProviderResult]) -> CompanyInfo:
        """Aggregate company information from multiple providers"""
        companies = [result.data for result in successful_results.values()]
        
        # Start with the most complete record
        primary = max(companies, key=lambda c: sum(1 for field in ['description', 'sector', 'industry', 'website'] if getattr(c, field)))
        
        # Merge fields from all providers
        for company in companies:
            if company != primary:
                for field in company.__dict__:
                    primary_value = getattr(primary, field, None)
                    company_value = getattr(company, field, None)
                    
                    # Fill in missing fields or use longer descriptions
                    if not primary_value and company_value:
                        setattr(primary, field, company_value)
                    elif field == 'description' and company_value and len(str(company_value)) > len(str(primary_value or '')):
                        setattr(primary, field, company_value)
        
        return primary
    
    def _aggregate_economic_events(self, successful_results: Dict[str, ProviderResult]) -> List[EconomicEvent]:
        """Aggregate economic events from multiple providers"""
        all_events = []
        for result in successful_results.values():
            if isinstance(result.data, list):
                all_events.extend(result.data)
        
        # Remove duplicates by event name and date
        seen = set()
        unique_events = []
        for event in all_events:
            key = (event.event_name, event.timestamp.strftime('%Y-%m-%d'))
            if key not in seen:
                seen.add(key)
                unique_events.append(event)
        
        # Sort by importance and timestamp
        unique_events.sort(key=lambda e: (e.importance, e.timestamp), reverse=True)
        return unique_events
    
    def _aggregate_earnings_calendar(self, successful_results: Dict[str, ProviderResult]) -> List[EarningsCalendar]:
        """Aggregate earnings calendar from multiple providers"""
        all_earnings = []
        for result in successful_results.values():
            if isinstance(result.data, list):
                all_earnings.extend(result.data)
        
        # Remove duplicates by symbol and date
        seen = set()
        unique_earnings = []
        for earning in all_earnings:
            key = (earning.symbol, earning.date)
            if key not in seen:
                seen.add(key)
                unique_earnings.append(earning)
        
        unique_earnings.sort(key=lambda e: e.date)
        return unique_earnings
    
    def _aggregate_news(self, successful_results: Dict[str, ProviderResult]) -> List[Dict[str, Any]]:
        """Aggregate news from multiple providers"""
        all_news = []
        for result in successful_results.values():
            if isinstance(result.data, list):
                all_news.extend(result.data)
        
        # Remove duplicates by title similarity and sort by date
        unique_news = []
        seen_titles = set()
        
        for article in sorted(all_news, key=lambda x: x.get('published_date', ''), reverse=True):
            title = article.get('title', '').lower()[:100]  # First 100 chars for similarity
            if title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(article)
        
        return unique_news
    
    def _aggregate_fundamentals(self, successful_results: Dict[str, ProviderResult]) -> Dict[str, Any]:
        """Aggregate fundamental data from multiple providers"""
        all_fundamentals = [result.data for result in successful_results.values()]
        
        # Merge all fundamental data
        merged = {}
        for fundamental in all_fundamentals:
            if isinstance(fundamental, dict):
                merged.update(fundamental)
        
        return merged
    
    def _aggregate_earnings(self, successful_results: Dict[str, ProviderResult]) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """Aggregate earnings data from multiple providers"""
        all_earnings = []
        for result in successful_results.values():
            if isinstance(result.data, list):
                all_earnings.extend(result.data)
            elif isinstance(result.data, dict):
                all_earnings.append(result.data)
        
        return all_earnings if all_earnings else {}
    
    def _aggregate_dividends(self, successful_results: Dict[str, ProviderResult]) -> List[Dict[str, Any]]:
        """Aggregate dividend data from multiple providers"""
        all_dividends = []
        for result in successful_results.values():
            if isinstance(result.data, list):
                all_dividends.extend(result.data)
        
        # Remove duplicates by date
        seen = set()
        unique_dividends = []
        for dividend in all_dividends:
            date_key = dividend.get('date') or dividend.get('ex_date')
            if date_key not in seen:
                seen.add(date_key)
                unique_dividends.append(dividend)
        
        return unique_dividends
    
    def _aggregate_technical_indicators(self, successful_results: Dict[str, ProviderResult]) -> Dict[str, Any]:
        """Aggregate technical indicators from multiple providers"""
        # For technical indicators, prefer the most complete dataset
        best_result = max(successful_results.values(), 
                         key=lambda r: len(r.data.get('values', [])) if isinstance(r.data, dict) else 0)
        return best_result.data
    
    def _aggregate_economic_data(self, successful_results: Dict[str, ProviderResult]) -> Any:
        """Aggregate economic data from multiple providers"""
        # For economic data, prefer the most recent or complete dataset
        return next(iter(successful_results.values())).data
    
    def _aggregate_earnings_transcript(self, successful_results: Dict[str, ProviderResult]) -> Optional[EarningsCallTranscript]:
        """Aggregate earnings transcripts from multiple providers"""
        # For transcripts, prefer the longest/most complete one
        transcripts = [result.data for result in successful_results.values() if result.data]
        if not transcripts:
            return None
        
        return max(transcripts, key=lambda t: len(t.transcript) if hasattr(t, 'transcript') else 0)
    
    def _aggregate_market_status(self, successful_results: Dict[str, ProviderResult]) -> Dict[str, Any]:
        """Aggregate market status from multiple providers"""
        # For market status, use the most recent data
        all_status = [result.data for result in successful_results.values()]
        
        # Merge all status data
        merged_status = {}
        for status in all_status:
            if isinstance(status, dict):
                merged_status.update(status)
        
        return merged_status

    # Main public methods for each data type

    async def get_quote(self, symbol: str) -> AggregatedResult:
        """
        Get current quote for a symbol from all providers and aggregate results.

        Args:
            symbol: Stock symbol

        Returns:
            AggregatedResult containing aggregated StockQuote data
        """
        return await self._fetch_from_all_providers(
            method_name="get_quote",
            data_type="quote",
            symbol=symbol
        )
    async def get_historical(
        self,
        symbol: str,
        start_date: date,
        end_date: date,
        interval: str = "1d"
    ) -> AggregatedResult:
        """
        Get historical prices from all providers and aggregate results.

        Args:
            symbol: Stock symbol
            start_date: Start date for historical data
            end_date: End date for historical data
            interval: Time interval (1min, 5min, 1d, etc.)

        Returns:
            AggregatedResult containing aggregated List[HistoricalPrice]
        """
        return await self._fetch_from_all_providers(
            method_name="get_historical",
            data_type="historical",
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            interval=interval
        )

    async def get_options_chain(
        self,
        symbol: str,
        expiration: Optional[date] = None
    ) -> AggregatedResult:
        """
        Get options chain from all providers and aggregate results.

        Args:
            symbol: Stock symbol
            expiration: Optional expiration date filter

        Returns:
            AggregatedResult containing aggregated List[OptionQuote]
        """
        return await self._fetch_from_all_providers(
            method_name="get_options_chain",
            data_type="options_chain",
            symbol=symbol,
            expiration=expiration
        )

    async def get_company_info(self, symbol: str) -> AggregatedResult:
        """
        Get company information from all providers and aggregate results.

        Args:
            symbol: Stock symbol

        Returns:
            AggregatedResult containing aggregated CompanyInfo
        """
        return await self._fetch_from_all_providers(
            method_name="get_company_info",
            data_type="company_info",
            symbol=symbol
        )

    async def get_fundamentals(self, symbol: str) -> AggregatedResult:
        """
        Get fundamental data from all providers and aggregate results.

        Args:
            symbol: Stock symbol

        Returns:
            AggregatedResult containing aggregated fundamental metrics dict
        """
        return await self._fetch_from_all_providers(
            method_name="get_fundamentals",
            data_type="fundamentals",
            symbol=symbol
        )

    async def get_earnings(self, symbol: str) -> AggregatedResult:
        """
        Get earnings data from all providers and aggregate results.

        Args:
            symbol: Stock symbol

        Returns:
            AggregatedResult containing aggregated earnings data
        """
        return await self._fetch_from_all_providers(
            method_name="get_earnings",
            data_type="earnings",
            symbol=symbol
        )

    async def get_dividends(self, symbol: str) -> AggregatedResult:
        """
        Get dividend data from all providers and aggregate results.

        Args:
            symbol: Stock symbol

        Returns:
            AggregatedResult containing aggregated dividend data list
        """
        return await self._fetch_from_all_providers(
            method_name="get_dividends",
            data_type="dividends",
            symbol=symbol
        )

    async def get_news(
        self,
        symbol: Optional[str] = None,
        limit: int = 10,
        **kwargs
    ) -> AggregatedResult:
        """
        Get news from all providers and aggregate results

        Args:
            symbol: Optional stock symbol to filter news
            limit: Maximum number of news items to return
            **kwargs: Additional provider-specific arguments

        Returns:
            AggregatedResult containing aggregated list of news items
        """
        return await self._fetch_from_all_providers(
            method_name="get_news",
            data_type="news",
            symbol=symbol,
            limit=limit,
            **kwargs
        )

    async def get_economic_events(
        self,
        countries: Optional[List[str]] = None,
        importance: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 50,
        **kwargs
    ) -> AggregatedResult:
        """
        Get economic calendar events from all providers and aggregate results

        Args:
            countries: List of country codes (e.g., ['US', 'EU', 'GB'])
            importance: Filter by importance (1=Low, 2=Medium, 3=High)
            start_date: Start date for events
            end_date: End date for events
            limit: Maximum number of events to return
            **kwargs: Additional provider-specific arguments

        Returns:
            AggregatedResult containing aggregated list of EconomicEvent objects
        """
        # Set default date range if not provided
        today = date.today()
        if not start_date:
            start_date = today
        if not end_date:
            end_date = today + timedelta(days=30)  # Default to next 30 days

        return await self._fetch_from_all_providers(
            method_name="get_economic_events",
            data_type="economic_events",
            countries=countries,
            importance=importance,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            **kwargs
        )

    async def get_intraday(
        self,
        symbol: str,
        interval: str = "5min"
    ) -> AggregatedResult:
        """
        Get intraday prices from all providers and aggregate results.

        Args:
            symbol: Stock symbol
            interval: Time interval (1min, 5min, 15min, etc.)

        Returns:
            AggregatedResult containing aggregated List[HistoricalPrice]
        """
        return await self._fetch_from_all_providers(
            method_name="get_intraday",
            data_type="intraday",
            symbol=symbol,
            interval=interval
        )

    async def get_technical_indicators(
        self,
        symbol: str,
        indicator: str,
        interval: str = "daily"
    ) -> AggregatedResult:
        """
        Get technical indicators from all providers and aggregate results.

        Args:
            symbol: Stock symbol
            indicator: Indicator name (sma, ema, macd, rsi, etc.)
            interval: Time interval

        Returns:
            AggregatedResult containing aggregated indicator data
        """
        return await self._fetch_from_all_providers(
            method_name="get_technical_indicators",
            data_type="technical_indicators",
            symbol=symbol,
            indicator=indicator,
            interval=interval
        )

    async def get_economic_data(self, indicator: str) -> AggregatedResult:
        """
        Get economic data from all providers and aggregate results.

        Args:
            indicator: Economic indicator name

        Returns:
            AggregatedResult containing aggregated economic data
        """
        return await self._fetch_from_all_providers(
            method_name="get_economic_data",
            data_type="economic_data",
            indicator=indicator
        )

    async def get_earnings_calendar(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 10
    ) -> AggregatedResult:
        """
        Get earnings calendar data from all providers and aggregate results.

        Args:
            symbol: Optional stock symbol to filter by
            start_date: Start date for the calendar
            end_date: End date for the calendar
            limit: Maximum number of results to return

        Returns:
            AggregatedResult containing aggregated List[EarningsCalendar]
        """
        # Set default date range if not provided
        today = date.today()
        if not start_date:
            start_date = today
        if not end_date:
            end_date = today + timedelta(days=30)  # Default to next 30 days

        return await self._fetch_from_all_providers(
            method_name="get_earnings_calendar",
            data_type="earnings_calendar",
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )

    async def get_earnings_transcript(
        self,
        symbol: str,
        year: int,
        quarter: int
    ) -> AggregatedResult:
        """
        Get earnings call transcript from all providers and aggregate results.

        Args:
            symbol: Stock symbol
            year: Fiscal year
            quarter: Fiscal quarter (1-4)

        Returns:
            AggregatedResult containing aggregated EarningsCallTranscript
        """
        return await self._fetch_from_all_providers(
            method_name="get_earnings_transcript",
            data_type="earnings_transcript",
            symbol=symbol,
            year=year,
            quarter=quarter
        )

    async def get_market_status(self, **kwargs) -> AggregatedResult:
        """
        Get current market status from all providers and aggregate results.

        Args:
            **kwargs: Additional provider-specific arguments

        Returns:
            AggregatedResult containing aggregated MarketStatus
        """
        return await self._fetch_from_all_providers(
            method_name="get_market_status",
            data_type="market_status",
            **kwargs
        )

    # Batch operations

    async def get_multiple_quotes(self, symbols: List[str]) -> Dict[str, AggregatedResult]:
        """
        Get quotes for multiple symbols concurrently with aggregation.

        Args:
            symbols: List of stock symbols

        Returns:
            Dictionary mapping symbols to AggregatedResults
        """
        tasks = {symbol: self.get_quote(symbol) for symbol in symbols}
        results = await asyncio.gather(*tasks.values())
        return dict(zip(tasks.keys(), results))

    async def get_multiple_historical(
        self,
        symbols: List[str],
        start_date: date,
        end_date: date,
        interval: str = "1d"
    ) -> Dict[str, AggregatedResult]:
        """
        Get historical data for multiple symbols concurrently with aggregation.

        Args:
            symbols: List of stock symbols
            start_date: Start date for historical data
            end_date: End date for historical data
            interval: Time interval

        Returns:
            Dictionary mapping symbols to AggregatedResults
        """
        tasks = {
            symbol: self.get_historical(symbol, start_date, end_date, interval)
            for symbol in symbols
        }
        results = await asyncio.gather(*tasks.values())
        return dict(zip(tasks.keys(), results))

    # Utility methods

    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
        logger.info("Brain cache cleared")

    def get_available_providers(self) -> List[str]:
        """Get list of currently available providers"""
        return list(self.providers.keys())

    def get_provider_status(self) -> Dict[str, bool]:
        """Get status of all configured providers"""
        status = {}
        for name in ['alpha_vantage', 'finnhub', 'polygon', 'twelve_data', 'fmp', 'tiingo', 'api_ninjas', 'fiscal']:
            config = getattr(self.config, name)
            status[name] = config.enabled and config.api_key is not None
        return status
