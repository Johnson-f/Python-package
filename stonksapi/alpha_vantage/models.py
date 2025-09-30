"""
Pydantic models for Alpha Vantage API responses.

This module provides strongly-typed models for all Alpha Vantage API endpoints,
ensuring type safety and validation for API responses.
"""

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


# ==================== Base Models ====================


class MetaData(BaseModel):
    """Base metadata model for time series responses."""

    information: Optional[str] = Field(None, alias="1. Information")
    symbol: Optional[str] = Field(None, alias="2. Symbol")
    last_refreshed: Optional[str] = Field(None, alias="3. Last Refreshed")
    interval: Optional[str] = Field(None, alias="4. Interval")
    output_size: Optional[str] = Field(None, alias="5. Output Size")
    time_zone: Optional[str] = Field(None, alias="6. Time Zone")

    class Config:
        populate_by_name = True


class TimeSeriesData(BaseModel):
    """Base model for OHLCV time series data."""

    open: Decimal = Field(..., alias="1. open")
    high: Decimal = Field(..., alias="2. high")
    low: Decimal = Field(..., alias="3. low")
    close: Decimal = Field(..., alias="4. close")
    volume: int = Field(..., alias="5. volume")

    class Config:
        populate_by_name = True


class AdjustedTimeSeriesData(TimeSeriesData):
    """Model for adjusted time series data (includes dividends and splits)."""

    adjusted_close: Decimal = Field(..., alias="6. adjusted close")
    dividend_amount: Optional[Decimal] = Field(None, alias="7. dividend amount")
    split_coefficient: Optional[Decimal] = Field(None, alias="8. split coefficient")


# ==================== Time Series Models ====================


class IntradayTimeSeries(BaseModel):
    """Response model for intraday time series data."""

    meta_data: MetaData = Field(..., alias="Meta Data")
    time_series: Dict[str, TimeSeriesData] = Field(default_factory=dict)

    @field_validator("time_series", mode="before")
    @classmethod
    def parse_time_series(cls, v: Any) -> Dict[str, TimeSeriesData]:
        """Parse time series data from various possible key formats."""
        if isinstance(v, dict):
            # Find the time series key dynamically
            for key in v.keys():
                if "Time Series" in key:
                    raw_data = v[key]
                    return {
                        timestamp: TimeSeriesData(**data)
                        for timestamp, data in raw_data.items()
                    }
            return {}
        return v

    class Config:
        populate_by_name = True


class DailyTimeSeries(BaseModel):
    """Response model for daily time series data."""

    meta_data: MetaData = Field(..., alias="Meta Data")
    time_series: Dict[str, TimeSeriesData] = Field(default_factory=dict)

    @field_validator("time_series", mode="before")
    @classmethod
    def parse_time_series(cls, v: Any) -> Dict[str, TimeSeriesData]:
        """Parse daily time series data."""
        if isinstance(v, dict):
            for key in v.keys():
                if "Time Series" in key:
                    raw_data = v[key]
                    return {
                        timestamp: TimeSeriesData(**data)
                        for timestamp, data in raw_data.items()
                    }
            return {}
        return v

    class Config:
        populate_by_name = True


class DailyAdjustedTimeSeries(BaseModel):
    """Response model for daily adjusted time series data."""

    meta_data: MetaData = Field(..., alias="Meta Data")
    time_series: Dict[str, AdjustedTimeSeriesData] = Field(default_factory=dict)

    @field_validator("time_series", mode="before")
    @classmethod
    def parse_time_series(cls, v: Any) -> Dict[str, AdjustedTimeSeriesData]:
        """Parse daily adjusted time series data."""
        if isinstance(v, dict):
            for key in v.keys():
                if "Time Series" in key:
                    raw_data = v[key]
                    return {
                        timestamp: AdjustedTimeSeriesData(**data)
                        for timestamp, data in raw_data.items()
                    }
            return {}
        return v

    class Config:
        populate_by_name = True


class WeeklyTimeSeries(BaseModel):
    """Response model for weekly time series data."""

    meta_data: MetaData = Field(..., alias="Meta Data")
    time_series: Dict[str, TimeSeriesData] = Field(default_factory=dict)

    @field_validator("time_series", mode="before")
    @classmethod
    def parse_time_series(cls, v: Any) -> Dict[str, TimeSeriesData]:
        """Parse weekly time series data."""
        if isinstance(v, dict):
            for key in v.keys():
                if "Time Series" in key:
                    raw_data = v[key]
                    return {
                        timestamp: TimeSeriesData(**data)
                        for timestamp, data in raw_data.items()
                    }
            return {}
        return v

    class Config:
        populate_by_name = True


class MonthlyTimeSeries(BaseModel):
    """Response model for monthly time series data."""

    meta_data: MetaData = Field(..., alias="Meta Data")
    time_series: Dict[str, TimeSeriesData] = Field(default_factory=dict)

    @field_validator("time_series", mode="before")
    @classmethod
    def parse_time_series(cls, v: Any) -> Dict[str, TimeSeriesData]:
        """Parse monthly time series data."""
        if isinstance(v, dict):
            for key in v.keys():
                if "Time Series" in key:
                    raw_data = v[key]
                    return {
                        timestamp: TimeSeriesData(**data)
                        for timestamp, data in raw_data.items()
                    }
            return {}
        return v

    class Config:
        populate_by_name = True


# ==================== Quote & Search Models ====================


class GlobalQuote(BaseModel):
    """Response model for global quote endpoint."""

    symbol: str = Field(..., alias="01. symbol")
    open: Decimal = Field(..., alias="02. open")
    high: Decimal = Field(..., alias="03. high")
    low: Decimal = Field(..., alias="04. low")
    price: Decimal = Field(..., alias="05. price")
    volume: int = Field(..., alias="06. volume")
    latest_trading_day: str = Field(..., alias="07. latest trading day")
    previous_close: Decimal = Field(..., alias="08. previous close")
    change: Decimal = Field(..., alias="09. change")
    change_percent: str = Field(..., alias="10. change percent")

    class Config:
        populate_by_name = True


class QuoteResponse(BaseModel):
    """Wrapper for global quote response."""

    global_quote: GlobalQuote = Field(..., alias="Global Quote")

    class Config:
        populate_by_name = True


class SearchMatch(BaseModel):
    """Model for symbol search match."""

    symbol: str = Field(..., alias="1. symbol")
    name: str = Field(..., alias="2. name")
    type: str = Field(..., alias="3. type")
    region: str = Field(..., alias="4. region")
    market_open: str = Field(..., alias="5. marketOpen")
    market_close: str = Field(..., alias="6. marketClose")
    timezone: str = Field(..., alias="7. timezone")
    currency: str = Field(..., alias="8. currency")
    match_score: str = Field(..., alias="9. matchScore")

    class Config:
        populate_by_name = True


class SymbolSearchResponse(BaseModel):
    """Response model for symbol search endpoint."""

    best_matches: List[SearchMatch] = Field(default_factory=list, alias="bestMatches")

    class Config:
        populate_by_name = True


# ==================== Fundamental Data Models ====================


class CompanyOverview(BaseModel):
    """Response model for company overview endpoint."""

    symbol: Optional[str] = Field(None, alias="Symbol")
    asset_type: Optional[str] = Field(None, alias="AssetType")
    name: Optional[str] = Field(None, alias="Name")
    description: Optional[str] = Field(None, alias="Description")
    cik: Optional[str] = Field(None, alias="CIK")
    exchange: Optional[str] = Field(None, alias="Exchange")
    currency: Optional[str] = Field(None, alias="Currency")
    country: Optional[str] = Field(None, alias="Country")
    sector: Optional[str] = Field(None, alias="Sector")
    industry: Optional[str] = Field(None, alias="Industry")
    address: Optional[str] = Field(None, alias="Address")
    fiscal_year_end: Optional[str] = Field(None, alias="FiscalYearEnd")
    latest_quarter: Optional[str] = Field(None, alias="LatestQuarter")
    
    # Financial metrics
    market_capitalization: Optional[str] = Field(None, alias="MarketCapitalization")
    ebitda: Optional[str] = Field(None, alias="EBITDA")
    pe_ratio: Optional[str] = Field(None, alias="PERatio")
    peg_ratio: Optional[str] = Field(None, alias="PEGRatio")
    book_value: Optional[str] = Field(None, alias="BookValue")
    dividend_per_share: Optional[str] = Field(None, alias="DividendPerShare")
    dividend_yield: Optional[str] = Field(None, alias="DividendYield")
    eps: Optional[str] = Field(None, alias="EPS")
    revenue_per_share_ttm: Optional[str] = Field(None, alias="RevenuePerShareTTM")
    profit_margin: Optional[str] = Field(None, alias="ProfitMargin")
    operating_margin_ttm: Optional[str] = Field(None, alias="OperatingMarginTTM")
    return_on_assets_ttm: Optional[str] = Field(None, alias="ReturnOnAssetsTTM")
    return_on_equity_ttm: Optional[str] = Field(None, alias="ReturnOnEquityTTM")
    revenue_ttm: Optional[str] = Field(None, alias="RevenueTTM")
    gross_profit_ttm: Optional[str] = Field(None, alias="GrossProfitTTM")
    diluted_eps_ttm: Optional[str] = Field(None, alias="DilutedEPSTTM")
    quarterly_earnings_growth_yoy: Optional[str] = Field(
        None, alias="QuarterlyEarningsGrowthYOY"
    )
    quarterly_revenue_growth_yoy: Optional[str] = Field(
        None, alias="QuarterlyRevenueGrowthYOY"
    )
    analyst_target_price: Optional[str] = Field(None, alias="AnalystTargetPrice")
    analyst_rating_strong_buy: Optional[str] = Field(
        None, alias="AnalystRatingStrongBuy"
    )
    analyst_rating_buy: Optional[str] = Field(None, alias="AnalystRatingBuy")
    analyst_rating_hold: Optional[str] = Field(None, alias="AnalystRatingHold")
    analyst_rating_sell: Optional[str] = Field(None, alias="AnalystRatingSell")
    analyst_rating_strong_sell: Optional[str] = Field(
        None, alias="AnalystRatingStrongSell"
    )
    trailing_pe: Optional[str] = Field(None, alias="TrailingPE")
    forward_pe: Optional[str] = Field(None, alias="ForwardPE")
    price_to_sales_ratio_ttm: Optional[str] = Field(None, alias="PriceToSalesRatioTTM")
    price_to_book_ratio: Optional[str] = Field(None, alias="PriceToBookRatio")
    ev_to_revenue: Optional[str] = Field(None, alias="EVToRevenue")
    ev_to_ebitda: Optional[str] = Field(None, alias="EVToEBITDA")
    beta: Optional[str] = Field(None, alias="Beta")
    week_52_high: Optional[str] = Field(None, alias="52WeekHigh")
    week_52_low: Optional[str] = Field(None, alias="52WeekLow")
    day_50_moving_average: Optional[str] = Field(None, alias="50DayMovingAverage")
    day_200_moving_average: Optional[str] = Field(None, alias="200DayMovingAverage")
    shares_outstanding: Optional[str] = Field(None, alias="SharesOutstanding")
    dividend_date: Optional[str] = Field(None, alias="DividendDate")
    ex_dividend_date: Optional[str] = Field(None, alias="ExDividendDate")

    class Config:
        populate_by_name = True


class EarningsData(BaseModel):
    """Model for quarterly/annual earnings data."""

    fiscal_date_ending: str = Field(..., alias="fiscalDateEnding")
    reported_eps: Optional[str] = Field(None, alias="reportedEPS")
    estimated_eps: Optional[str] = Field(None, alias="estimatedEPS")
    surprise: Optional[str] = Field(None, alias="surprise")
    surprise_percentage: Optional[str] = Field(None, alias="surprisePercentage")

    class Config:
        populate_by_name = True


class Earnings(BaseModel):
    """Response model for earnings endpoint."""

    symbol: str
    annual_earnings: List[EarningsData] = Field(
        default_factory=list, alias="annualEarnings"
    )
    quarterly_earnings: List[EarningsData] = Field(
        default_factory=list, alias="quarterlyEarnings"
    )

    class Config:
        populate_by_name = True


# ==================== News & Sentiment Models ====================


class TickerSentiment(BaseModel):
    """Model for ticker sentiment in news articles."""

    ticker: str
    relevance_score: str
    ticker_sentiment_score: str
    ticker_sentiment_label: str


class TopicRelevance(BaseModel):
    """Model for topic relevance in news articles."""

    topic: str
    relevance_score: str


class NewsFeed(BaseModel):
    """Model for individual news article."""

    title: str
    url: str
    time_published: str
    authors: List[str] = Field(default_factory=list)
    summary: str
    banner_image: Optional[str] = None
    source: str
    category_within_source: Optional[str] = None
    source_domain: str
    topics: List[TopicRelevance] = Field(default_factory=list)
    overall_sentiment_score: float
    overall_sentiment_label: str
    ticker_sentiment: List[TickerSentiment] = Field(default_factory=list)


class NewsSentimentResponse(BaseModel):
    """Response model for news sentiment endpoint."""

    items: str
    sentiment_score_definition: str
    relevance_score_definition: str
    feed: List[NewsFeed]


# ==================== Forex Models ====================


class ForexMetaData(BaseModel):
    """Metadata for forex responses."""

    information: str = Field(..., alias="1. Information")
    from_symbol: str = Field(..., alias="2. From Symbol")
    to_symbol: str = Field(..., alias="3. To Symbol")
    last_refreshed: str = Field(..., alias="4. Last Refreshed")
    interval: Optional[str] = Field(None, alias="5. Interval")
    output_size: Optional[str] = Field(None, alias="6. Output Size")
    time_zone: str = Field(..., alias="7. Time Zone")

    class Config:
        populate_by_name = True


class ForexData(BaseModel):
    """Model for forex OHLC data."""

    open: Decimal = Field(..., alias="1. open")
    high: Decimal = Field(..., alias="2. high")
    low: Decimal = Field(..., alias="3. low")
    close: Decimal = Field(..., alias="4. close")

    class Config:
        populate_by_name = True


class ForexTimeSeries(BaseModel):
    """Response model for forex time series data."""

    meta_data: ForexMetaData = Field(..., alias="Meta Data")
    time_series: Dict[str, ForexData] = Field(default_factory=dict)

    @field_validator("time_series", mode="before")
    @classmethod
    def parse_time_series(cls, v: Any) -> Dict[str, ForexData]:
        """Parse forex time series data."""
        if isinstance(v, dict):
            for key in v.keys():
                if "Time Series" in key:
                    raw_data = v[key]
                    return {
                        timestamp: ForexData(**data) for timestamp, data in raw_data.items()
                    }
            return {}
        return v

    class Config:
        populate_by_name = True


class ExchangeRate(BaseModel):
    """Model for real-time exchange rate."""

    from_currency_code: str = Field(..., alias="1. From_Currency Code")
    from_currency_name: str = Field(..., alias="2. From_Currency Name")
    to_currency_code: str = Field(..., alias="3. To_Currency Code")
    to_currency_name: str = Field(..., alias="4. To_Currency Name")
    exchange_rate: Decimal = Field(..., alias="5. Exchange Rate")
    last_refreshed: str = Field(..., alias="6. Last Refreshed")
    time_zone: str = Field(..., alias="7. Time Zone")
    bid_price: Optional[Decimal] = Field(None, alias="8. Bid Price")
    ask_price: Optional[Decimal] = Field(None, alias="9. Ask Price")

    class Config:
        populate_by_name = True


class ExchangeRateResponse(BaseModel):
    """Response model for exchange rate endpoint."""

    realtime_currency_exchange_rate: ExchangeRate = Field(
        ..., alias="Realtime Currency Exchange Rate"
    )

    class Config:
        populate_by_name = True


# ==================== Crypto Models ====================


class CryptoMetaData(BaseModel):
    """Metadata for crypto responses."""

    information: str = Field(..., alias="1. Information")
    digital_currency_code: str = Field(..., alias="2. Digital Currency Code")
    digital_currency_name: str = Field(..., alias="3. Digital Currency Name")
    market_code: str = Field(..., alias="4. Market Code")
    market_name: str = Field(..., alias="5. Market Name")
    last_refreshed: str = Field(..., alias="6. Last Refreshed")
    interval: Optional[str] = Field(None, alias="7. Interval")
    output_size: Optional[str] = Field(None, alias="8. Output Size")
    time_zone: str = Field(..., alias="9. Time Zone")

    class Config:
        populate_by_name = True


class CryptoData(BaseModel):
    """Model for crypto OHLCV data."""

    open: Decimal = Field(..., alias="1. open")
    high: Decimal = Field(..., alias="2. high")
    low: Decimal = Field(..., alias="3. low")
    close: Decimal = Field(..., alias="4. close")
    volume: Decimal = Field(..., alias="5. volume")

    class Config:
        populate_by_name = True


class CryptoTimeSeries(BaseModel):
    """Response model for crypto time series data."""

    meta_data: CryptoMetaData = Field(..., alias="Meta Data")
    time_series: Dict[str, CryptoData] = Field(default_factory=dict)

    @field_validator("time_series", mode="before")
    @classmethod
    def parse_time_series(cls, v: Any) -> Dict[str, CryptoData]:
        """Parse crypto time series data."""
        if isinstance(v, dict):
            for key in v.keys():
                if "Time Series" in key:
                    raw_data = v[key]
                    return {
                        timestamp: CryptoData(**data) for timestamp, data in raw_data.items()
                    }
            return {}
        return v

    class Config:
        populate_by_name = True


# ==================== Technical Indicators Models ====================


class TechnicalIndicatorMetaData(BaseModel):
    """Metadata for technical indicator responses."""

    symbol: str = Field(..., alias="1: Symbol")
    indicator: str = Field(..., alias="2: Indicator")
    last_refreshed: str = Field(..., alias="3: Last Refreshed")
    interval: str = Field(..., alias="4: Interval")
    time_period: Optional[int] = Field(None, alias="5: Time Period")
    series_type: Optional[str] = Field(None, alias="6: Series Type")
    time_zone: str = Field(..., alias="7: Time Zone")

    class Config:
        populate_by_name = True


class TechnicalIndicatorData(BaseModel):
    """Generic model for technical indicator data point."""

    value: Decimal

    class Config:
        extra = "allow"  # Allow additional fields for different indicators


class TechnicalIndicatorResponse(BaseModel):
    """Response model for technical indicators."""

    meta_data: TechnicalIndicatorMetaData = Field(..., alias="Meta Data")
    technical_analysis: Dict[str, Dict[str, str]] = Field(default_factory=dict)

    @field_validator("technical_analysis", mode="before")
    @classmethod
    def parse_technical_analysis(cls, v: Any) -> Dict[str, Dict[str, str]]:
        """Parse technical analysis data."""
        if isinstance(v, dict):
            for key in v.keys():
                if "Technical Analysis" in key:
                    return v[key]
            return {}
        return v

    class Config:
        populate_by_name = True


# ==================== Economic Indicators Models ====================


class EconomicIndicatorData(BaseModel):
    """Model for economic indicator data point."""

    date: str
    value: str


class EconomicIndicatorResponse(BaseModel):
    """Response model for economic indicators."""

    name: str
    interval: str
    unit: str
    data: List[EconomicIndicatorData]


# ==================== Commodities Models ====================


class CommodityData(BaseModel):
    """Model for commodity data point."""

    date: str
    value: str


class CommodityResponse(BaseModel):
    """Response model for commodity data."""

    name: str
    interval: str
    unit: str
    data: List[CommodityData]
