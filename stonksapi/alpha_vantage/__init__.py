"""
Alpha Vantage API wrapper with Pydantic models (part of stonksapi package).

This module provides a comprehensive, type-safe wrapper around the Alpha Vantage API
for financial data access including stocks, forex, cryptocurrencies, technical indicators,
and fundamental data.

Quick Start:
    >>> from stonksapi.alpha_vantage import AlphaVantageClient
    >>> 
    >>> client = AlphaVantageClient(api_key="your_api_key")
    >>> 
    >>> # Get real-time quote
    >>> quote = client.get_quote("AAPL")
    >>> print(f"Price: ${quote.global_quote.price}")
    >>> 
    >>> # Get company overview
    >>> overview = client.get_company_overview("AAPL")
    >>> print(f"P/E Ratio: {overview.pe_ratio}")
    >>> 
    >>> # Get daily data
    >>> daily = client.get_daily("AAPL")
    >>> for date, data in list(daily.time_series.items())[:5]:
    ...     print(f"{date}: Close ${data.close}")
"""

from .client import AlphaVantageClient, Interval, OutputSize
from .models import (
    AdjustedTimeSeriesData,
    CommodityData,
    CommodityResponse,
    CompanyOverview,
    CryptoData,
    CryptoMetaData,
    CryptoTimeSeries,
    DailyAdjustedTimeSeries,
    DailyTimeSeries,
    Earnings,
    EarningsData,
    EconomicIndicatorData,
    EconomicIndicatorResponse,
    ExchangeRate,
    ExchangeRateResponse,
    ForexData,
    ForexMetaData,
    ForexTimeSeries,
    GlobalQuote,
    IntradayTimeSeries,
    MetaData,
    MonthlyTimeSeries,
    NewsFeed,
    NewsSentimentResponse,
    QuoteResponse,
    SearchMatch,
    SymbolSearchResponse,
    TechnicalIndicatorData,
    TechnicalIndicatorMetaData,
    TechnicalIndicatorResponse,
    TickerSentiment,
    TimeSeriesData,
    TopicRelevance,
    WeeklyTimeSeries,
)

__version__ = "0.1.0"

__all__ = [
    # Client
    "AlphaVantageClient",
    "Interval",
    "OutputSize",
    # Time Series Models
    "TimeSeriesData",
    "AdjustedTimeSeriesData",
    "IntradayTimeSeries",
    "DailyTimeSeries",
    "DailyAdjustedTimeSeries",
    "WeeklyTimeSeries",
    "MonthlyTimeSeries",
    "MetaData",
    # Quote & Search Models
    "GlobalQuote",
    "QuoteResponse",
    "SearchMatch",
    "SymbolSearchResponse",
    # Fundamental Data Models
    "CompanyOverview",
    "Earnings",
    "EarningsData",
    # News & Sentiment Models
    "NewsFeed",
    "NewsSentimentResponse",
    "TickerSentiment",
    "TopicRelevance",
    # Forex Models
    "ForexData",
    "ForexMetaData",
    "ForexTimeSeries",
    "ExchangeRate",
    "ExchangeRateResponse",
    # Crypto Models
    "CryptoData",
    "CryptoMetaData",
    "CryptoTimeSeries",
    # Technical Indicators Models
    "TechnicalIndicatorData",
    "TechnicalIndicatorMetaData",
    "TechnicalIndicatorResponse",
    # Economic Indicators Models
    "EconomicIndicatorData",
    "EconomicIndicatorResponse",
    # Commodities Models
    "CommodityData",
    "CommodityResponse",
]
