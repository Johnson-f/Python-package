"""
Pydantic models for yfinance API responses.
"""
from datetime import date as DateType
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


class StockAction(BaseModel):
    """Base model for stock actions like dividends and splits."""
    date: DateType

class Dividend(StockAction):
    """Pydantic model for a dividend payment."""
    dividend: float

class Split(StockAction):
    """Pydantic model for a stock split event."""
    stock_splits: float

class HistoricalData(BaseModel):
    """Pydantic model for a single row of historical market data."""
    date: DateType = Field(alias='Date')
    open: float = Field(alias='Open')
    high: float = Field(alias='High')
    low: float = Field(alias='Low')
    close: float = Field(alias='Close')
    volume: int = Field(alias='Volume')
    dividends: float = Field(alias='Dividends')
    stock_splits: float = Field(alias='Stock Splits')

    model_config = ConfigDict(populate_by_name=True)


class FinancialReport(BaseModel):
    """Pydantic model for a single financial report (e.g., for a specific year)."""
    date: DateType
    metrics: Dict[str, Any]

class FinancialStatement(BaseModel):
    """Pydantic model for a company's financial statements."""
    reports: List[FinancialReport]


# Earnings and Calendar Models
class EarningsData(BaseModel):
    """Model for earnings data."""
    date: DateType
    earnings: Optional[float] = None
    revenue: Optional[float] = None
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class EarningsCalendar(BaseModel):
    """Model for earnings calendar events."""
    earnings_date: Optional[DateType] = Field(None, alias='Earnings Date')
    earnings_average: Optional[float] = Field(None, alias='Earnings Average')
    earnings_low: Optional[float] = Field(None, alias='Earnings Low')
    earnings_high: Optional[float] = Field(None, alias='Earnings High')
    revenue_average: Optional[float] = Field(None, alias='Revenue Average')
    revenue_low: Optional[float] = Field(None, alias='Revenue Low')
    revenue_high: Optional[float] = Field(None, alias='Revenue High')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class EarningsEstimate(BaseModel):
    """Model for earnings estimates."""
    period: Optional[str] = None
    no_of_analysts: Optional[int] = Field(None, alias='No. of Analysts')
    avg_estimate: Optional[float] = Field(None, alias='Avg. Estimate')
    low_estimate: Optional[float] = Field(None, alias='Low Estimate')
    high_estimate: Optional[float] = Field(None, alias='High Estimate')
    year_ago_eps: Optional[float] = Field(None, alias='Year Ago EPS')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class RevenueEstimate(BaseModel):
    """Model for revenue estimates."""
    period: Optional[str] = None
    no_of_analysts: Optional[int] = Field(None, alias='No. of Analysts')
    avg_estimate: Optional[float] = Field(None, alias='Avg. Estimate')
    low_estimate: Optional[float] = Field(None, alias='Low Estimate')
    high_estimate: Optional[float] = Field(None, alias='High Estimate')
    year_ago_sales: Optional[float] = Field(None, alias='Year Ago Sales')
    sales_growth: Optional[str] = Field(None, alias='Sales Growth (year/est)')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


# Analysis Models
class Recommendation(BaseModel):
    """Model for analyst recommendations."""
    period: Optional[str] = None
    strong_buy: Optional[int] = Field(None, alias='strongBuy')
    buy: Optional[int] = None
    hold: Optional[int] = None
    sell: Optional[int] = None
    strong_sell: Optional[int] = Field(None, alias='strongSell')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class RecommendationSummary(BaseModel):
    """Model for recommendation summary."""
    period: Optional[str] = None
    strong_buy: Optional[int] = Field(None, alias='strongBuy')
    buy: Optional[int] = None
    hold: Optional[int] = None
    sell: Optional[int] = None
    strong_sell: Optional[int] = Field(None, alias='strongSell')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class UpgradeDowngrade(BaseModel):
    """Model for analyst upgrades/downgrades."""
    grade_date: Optional[DateType] = Field(None, alias='GradeDate')
    firm: Optional[str] = Field(None, alias='Firm')
    to_grade: Optional[str] = Field(None, alias='ToGrade')
    from_grade: Optional[str] = Field(None, alias='FromGrade')
    action: Optional[str] = Field(None, alias='Action')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class AnalystPriceTarget(BaseModel):
    """Model for analyst price targets."""
    current: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    mean: Optional[float] = None
    median: Optional[float] = None
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class EPSTrend(BaseModel):
    """Model for EPS trends."""
    period: Optional[str] = None
    current_estimate: Optional[float] = Field(None, alias='Current Estimate')
    days_7_ago: Optional[float] = Field(None, alias='7 Days Ago')
    days_30_ago: Optional[float] = Field(None, alias='30 Days Ago')
    days_60_ago: Optional[float] = Field(None, alias='60 Days Ago')
    days_90_ago: Optional[float] = Field(None, alias='90 Days Ago')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class EPSRevisions(BaseModel):
    """Model for EPS revisions."""
    period: Optional[str] = None
    up_last_7_days: Optional[int] = Field(None, alias='Up Last 7 Days')
    up_last_30_days: Optional[int] = Field(None, alias='Up Last 30 Days')
    down_last_30_days: Optional[int] = Field(None, alias='Down Last 30 Days')
    down_last_90_days: Optional[int] = Field(None, alias='Down Last 90 Days')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class GrowthEstimates(BaseModel):
    """Model for growth estimates."""
    period: Optional[str] = None
    estimate: Optional[str] = None
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


# Holdings Models
class MajorHolder(BaseModel):
    """Model for major holders."""
    insider_percent_held: Optional[str] = Field(None, alias='insidersPercentHeld')
    institutions_percent_held: Optional[str] = Field(None, alias='institutionsPercentHeld')
    institutions_float_percent_held: Optional[str] = Field(None, alias='institutionsFloatPercentHeld')
    institutions_count: Optional[str] = Field(None, alias='institutionsCount')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class InstitutionalHolder(BaseModel):
    """Model for institutional holders."""
    holder: Optional[str] = Field(None, alias='Holder')
    shares: Optional[int] = Field(None, alias='Shares')
    date_reported: Optional[str] = Field(None, alias='Date Reported')
    out: Optional[str] = Field(None, alias='% Out')
    value: Optional[int] = Field(None, alias='Value')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class MutualFundHolder(BaseModel):
    """Model for mutual fund holders."""
    holder: Optional[str] = Field(None, alias='Holder')
    shares: Optional[int] = Field(None, alias='Shares')
    date_reported: Optional[str] = Field(None, alias='Date Reported')
    out: Optional[str] = Field(None, alias='% Out')
    value: Optional[int] = Field(None, alias='Value')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class InsiderTransaction(BaseModel):
    """Model for insider transactions."""
    filer: Optional[str] = Field(None, alias='Filer')
    transaction_text: Optional[str] = Field(None, alias='Transaction Text')
    money_text: Optional[str] = Field(None, alias='Money Text')
    ownership: Optional[str] = Field(None, alias='Ownership')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class InsiderPurchase(BaseModel):
    """Model for insider purchases."""
    shares: Optional[int] = None
    trans: Optional[int] = None
    purchase_activity: Optional[str] = Field(None, alias='Purchase Activity')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


class InsiderRosterHolder(BaseModel):
    """Model for insider roster holders."""
    name: Optional[str] = Field(None, alias='Name')
    position: Optional[str] = Field(None, alias='Position')
    url: Optional[str] = Field(None, alias='URL')
    most_recent_transaction: Optional[str] = Field(None, alias='Most Recent Transaction')
    latest_trans_date: Optional[str] = Field(None, alias='Latest Trans Date')
    shares_owned_directly: Optional[int] = Field(None, alias='Shares Owned Directly')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


# Sustainability Model
class SustainabilityData(BaseModel):
    """Model for ESG and sustainability data."""
    palm_oil: Optional[bool] = Field(None, alias='palmOil')
    controversial_weapons: Optional[bool] = Field(None, alias='controversialWeapons')
    gambling: Optional[bool] = None
    social_score: Optional[float] = Field(None, alias='socialScore')
    nuclear: Optional[bool] = None
    fur_leather: Optional[bool] = Field(None, alias='furLeather')
    alcoholic: Optional[bool] = None
    gmo: Optional[bool] = None
    catholic: Optional[bool] = None
    social_percentile: Optional[float] = Field(None, alias='socialPercentile')
    peer_count: Optional[int] = Field(None, alias='peerCount')
    governance_score: Optional[float] = Field(None, alias='governanceScore')
    environment_percentile: Optional[float] = Field(None, alias='environmentPercentile')
    animal_testing: Optional[bool] = Field(None, alias='animalTesting')
    tobacco: Optional[bool] = None
    total_esg: Optional[float] = Field(None, alias='totalEsg')
    highest_controversy: Optional[int] = Field(None, alias='highestControversy')
    esg_performance: Optional[str] = Field(None, alias='esgPerformance')
    coal: Optional[bool] = None
    pesticides: Optional[bool] = None
    adult: Optional[bool] = None
    governance_percentile: Optional[float] = Field(None, alias='governancePercentile')
    peer_group: Optional[str] = Field(None, alias='peerGroup')
    small_arms: Optional[bool] = Field(None, alias='smallArms')
    environment_score: Optional[float] = Field(None, alias='environmentScore')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


# News Model
class NewsArticle(BaseModel):
    """Model for news articles."""
    uuid: Optional[str] = None
    title: Optional[str] = None
    publisher: Optional[str] = None
    link: Optional[HttpUrl] = None
    provider_publish_time: Optional[int] = Field(None, alias='providerPublishTime')
    type: Optional[str] = None
    thumbnail: Optional[Dict[str, Any]] = None
    related_tickers: Optional[List[str]] = Field(None, alias='relatedTickers')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


# SEC Filings Model
class SECFiling(BaseModel):
    """Model for SEC filings."""
    date: Optional[str] = None
    epochDate: Optional[int] = None
    type: Optional[str] = None
    title: Optional[str] = None
    edgarUrl: Optional[HttpUrl] = None
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


# Fund Data Model
class FundData(BaseModel):
    """Model for fund-specific data."""
    fund_family: Optional[str] = Field(None, alias='fundFamily')
    fund_inception_date: Optional[int] = Field(None, alias='fundInceptionDate')
    legal_type: Optional[str] = Field(None, alias='legalType')
    investment_style: Optional[str] = Field(None, alias='investmentStyle')
    management_info: Optional[Dict[str, Any]] = Field(None, alias='managementInfo')
    fund_operations: Optional[Dict[str, Any]] = Field(None, alias='fundOperations')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


# Fast Info Model
class FastInfo(BaseModel):
    """Model for fast info data (quick access to key metrics)."""
    last_price: Optional[float] = Field(None, alias='lastPrice')
    last_volume: Optional[int] = Field(None, alias='lastVolume')
    market_cap: Optional[int] = Field(None, alias='marketCap')
    open: Optional[float] = None
    previous_close: Optional[float] = Field(None, alias='previousClose')
    quote_type: Optional[str] = Field(None, alias='quoteType')
    regular_market_previous_close: Optional[float] = Field(None, alias='regularMarketPreviousClose')
    shares: Optional[int] = None
    ten_day_average_volume: Optional[int] = Field(None, alias='tenDayAverageVolume')
    three_month_average_volume: Optional[int] = Field(None, alias='threeMonthAverageVolume')
    timezone: Optional[str] = None
    two_hundred_day_average: Optional[float] = Field(None, alias='twoHundredDayAverage')
    year_change: Optional[float] = Field(None, alias='yearChange')
    year_high: Optional[float] = Field(None, alias='yearHigh')
    year_low: Optional[float] = Field(None, alias='yearLow')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


# Shares Outstanding Model
class SharesOutstanding(BaseModel):
    """Model for shares outstanding data."""
    date: DateType
    shares: Optional[int] = None
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


# Capital Gains Model
class CapitalGain(BaseModel):
    """Model for capital gains."""
    date: DateType
    capital_gains: Optional[float] = Field(None, alias='Capital Gains')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')


# Actions Model (combines dividends and splits)
class Action(BaseModel):
    """Model for stock actions (dividends and splits combined)."""
    date: DateType
    dividends: Optional[float] = Field(None, alias='Dividends')
    stock_splits: Optional[float] = Field(None, alias='Stock Splits')
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')
