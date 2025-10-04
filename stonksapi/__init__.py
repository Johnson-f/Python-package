"""
Stonksapi - A comprehensive financial data API package.

This package provides unified access to multiple financial data providers
with strongly-typed Pydantic models.

Example:
    >>> from stonksapi import StonksApiClient, TickerInfo, Quote
    >>> client = StonksApiClient()
    >>> ticker_info: TickerInfo = client.get_ticker_info("AAPL")
    >>> quote: Quote = client.get_quote("AAPL")
"""

__version__ = "0.4.0"

from .client import StonksApiClient
from .models import (
    # Unified Models
    TickerInfo,
    Quote,
    HistoricalData,
    NewsArticle,

    # Other useful models
    FinancialStatement,
    Dividend,
    Split,
    MarketHours,
    MarketMover,
    SectorPerformance,
)

__all__ = [
    "StonksApiClient",
    "TickerInfo",
    "Quote",
    "HistoricalData",
    "NewsArticle",
    "FinancialStatement",
    "Dividend",
    "Split",
    "MarketHours",
    "MarketMover",
    "SectorPerformance",
]