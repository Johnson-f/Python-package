"""
Pydantic models for stonksapi.

This module provides strongly-typed models for all data providers.
"""

from datetime import date as DateType, datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Union
from enum import Enum

from pydantic import BaseModel, Field, model_validator, ConfigDict, HttpUrl

# Import all models from providers
from .yfinance.models import *
from .finance_query.models import *

# ==================== Unified Models ====================

class TickerInfo(BaseModel):
    """Unified model for ticker information from all providers."""
    
    # Descriptive fields
    symbol: Optional[str] = None
    name: Optional[str] = None
    long_name: Optional[str] = Field(None, alias='longName')
    short_name: Optional[str] = Field(None, alias='shortName')
    description: Optional[str] = None
    quote_type: Optional[str] = Field(None, alias='quoteType')
    currency: Optional[str] = None
    exchange: Optional[str] = None
    market: Optional[str] = None
    
    # Business summary
    long_business_summary: Optional[str] = Field(None, alias='longBusinessSummary')
    sector: Optional[str] = None
    industry: Optional[str] = None
    finnhub_industry: Optional[str] = None
    full_time_employees: Optional[int] = Field(None, alias='fullTimeEmployees')
    
    # Location and contact
    address: Optional[str] = None
    address1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[HttpUrl] = None
    
    # Market data
    market_cap: Optional[int] = Field(None, alias='marketCap')
    market_capitalization: Optional[float] = None
    shares_outstanding: Optional[float] = None
    regular_market_price: Optional[float] = Field(None, alias='regularMarketPrice')
    regular_market_open: Optional[float] = Field(None, alias='regularMarketOpen')
    regular_market_day_high: Optional[float] = Field(None, alias='regularMarketDayHigh')
    regular_market_day_low: Optional[float] = Field(None, alias='regularMarketDayLow')
    regular_market_previous_close: Optional[float] = Field(None, alias='regularMarketPreviousClose')
    fifty_two_week_high: Optional[float] = Field(None, alias='fiftyTwoWeekHigh')
    fifty_two_week_low: Optional[float] = Field(None, alias='fiftyTwoWeekLow')
    fifty_day_average: Optional[float] = Field(None, alias='fiftyDayAverage')
    two_hundred_day_average: Optional[float] = Field(None, alias='twoHundredDayAverage')
    
    # Volume
    volume: Optional[int] = Field(None, alias='volume')
    regular_market_volume: Optional[int] = Field(None, alias='regularMarketVolume')
    average_volume: Optional[int] = Field(None, alias='averageVolume')
    average_volume_10days: Optional[int] = Field(None, alias='averageVolume10days')
    
    # Financial ratios
    trailing_pe: Optional[float] = Field(None, alias='trailingPE')
    forward_pe: Optional[float] = Field(None, alias='forwardPE')
    price_to_sales_trailing_12_months: Optional[float] = Field(None, alias='priceToSalesTrailing12Months')
    trailing_eps: Optional[float] = Field(None, alias='trailingEps')
    forward_eps: Optional[float] = Field(None, alias='forwardEps')
    peg_ratio: Optional[float] = Field(None, alias='pegRatio')
    
    # Dividend and split info
    dividend_rate: Optional[float] = Field(None, alias='dividendRate')
    dividend_yield: Optional[float] = Field(None, alias='dividendYield')
    ex_dividend_date: Optional[int] = Field(None, alias='exDividendDate')
    last_split_factor: Optional[str] = Field(None, alias='lastSplitFactor')
    last_split_date: Optional[int] = Field(None, alias='lastSplitDate')

    # Source of the data
    source: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True, extra='ignore')

class Quote(BaseModel):
    """Unified model for a stock quote."""
    symbol: Optional[str] = None
    price: Optional[float] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    previous_close: Optional[float] = None
    volume: Optional[int] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    timestamp: Optional[int] = None
    source: Optional[str] = None

class HistoricalData(BaseModel):
    """Unified model for a single row of historical market data."""
    date: DateType
    open: float
    high: float
    low: float
    close: float
    volume: int
    dividends: Optional[float] = 0.0
    stock_splits: Optional[float] = 0.0
    source: Optional[str] = None

class NewsArticle(BaseModel):
    """Unified model for a news article."""
    id: Optional[str] = None
    title: str
    author: Optional[str] = None
    published_utc: Optional[str] = None
    article_url: Optional[HttpUrl] = None
    provider: Optional[str] = None
    publisher: Optional[str] = None
    summary: Optional[str] = None
    image_url: Optional[HttpUrl] = None

# ==================== YFinance Models ====================

class FinancialReport(BaseModel):
    """Pydantic model for a single financial report (e.g., for a specific year)."""
    date: DateType
    metrics: Dict[str, Any]

class FinancialStatement(BaseModel):
    """Pydantic model for a company's financial statements."""
    reports: List[FinancialReport]

class StockAction(BaseModel):
    """Base model for stock actions like dividends and splits."""
    date: DateType

class Dividend(StockAction):
    """Pydantic model for a dividend payment."""
    dividend: float

class Split(StockAction):
    """Pydantic model for a stock split event."""
    stock_splits: float


class MarketHours(BaseModel):
    status: str
    reason: str
    timestamp: str


class MarketMover(BaseModel):
    symbol: str
    name: str
    price: str
    change: str
    percent_change: str = Field(alias='percentChange')

    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class SectorPerformance(BaseModel):
    sector: str
    day_return: str = Field(alias='dayReturn')
    ytd_return: str = Field(alias='ytdReturn')
    year_return: str = Field(alias='yearReturn')
    three_year_return: str = Field(alias='threeYearReturn')
    five_year_return: str = Field(alias='fiveYearReturn')


