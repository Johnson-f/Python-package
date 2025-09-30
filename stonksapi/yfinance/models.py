"""
Pydantic models for yfinance API responses.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, HttpUrl

class TickerInfo(BaseModel):
    """Pydantic model for the .info dictionary of a yfinance Ticker."""
    
    # Descriptive fields
    symbol: Optional[str] = None
    long_name: Optional[str] = Field(None, alias='longName')
    short_name: Optional[str] = Field(None, alias='shortName')
    quote_type: Optional[str] = Field(None, alias='quoteType')
    currency: Optional[str] = None
    exchange: Optional[str] = None
    market: Optional[str] = None
    
    # Business summary
    long_business_summary: Optional[str] = Field(None, alias='longBusinessSummary')
    sector: Optional[str] = None
    industry: Optional[str] = None
    full_time_employees: Optional[int] = Field(None, alias='fullTimeEmployees')
    
    # Location and contact
    address1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[HttpUrl] = None
    
    # Market data
    market_cap: Optional[int] = Field(None, alias='marketCap')
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

    model_config = ConfigDict(populate_by_name=True, extra='ignore')
