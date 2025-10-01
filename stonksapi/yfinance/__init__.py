"""
Yahoo Finance API wrapper with Pydantic models (part of stonksapi package).

This module provides a type-safe wrapper around the yfinance library.

Quick Start:
    >>> from stonksapi.yfinance import YFinanceClient
    >>> 
    >>> client = YFinanceClient()
    >>> 
    >>> # Get Ticker Info
    >>> info = client.get_ticker_info("AAPL")
    >>> print(f"Company: {info.long_name}")
    >>> print(f"Sector: {info.sector}")
"""

from .client import YFinanceClient
from .models import (
    TickerInfo,
    HistoricalData,
    Dividend,
    Split,
    FinancialStatement,
    FinancialReport,
)

__all__ = [
    "YFinanceClient",
    "TickerInfo",
    "HistoricalData",
    "Dividend",
    "Split",
    "FinancialStatement",
    "FinancialReport",
]
