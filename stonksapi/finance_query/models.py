from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum


class MarketHours(BaseModel):
    status: str
    reason: str
    timestamp: str


class Quote(BaseModel):
    symbol: str
    name: str
    price: str
    pre_market_price: Optional[str] = Field(None, alias='preMarketPrice')
    after_hours_price: Optional[str] = Field(None, alias='afterHoursPrice')
    change: str
    percent_change: str = Field(alias='percentChange')
    logo: Optional[str] = None


class DetailedQuote(Quote):
    open: Optional[str] = None
    high: Optional[str] = None
    low: Optional[str] = None
    year_high: Optional[str] = Field(None, alias='yearHigh')
    year_low: Optional[str] = Field(None, alias='yearLow')
    volume: Optional[int] = None
    avg_volume: Optional[int] = Field(None, alias='avgVolume')
    market_cap: Optional[str] = Field(None, alias='marketCap')
    beta: Optional[float] = None
    pe: Optional[str] = None
    eps: Optional[str] = None
    dividend: Optional[str] = None
    yield_str: Optional[str] = Field(None, alias='yield')
    ex_dividend: Optional[str] = Field(None, alias='exDividend')
    net_assets: Optional[str] = Field(None, alias='netAssets')
    nav: Optional[str] = None
    expense_ratio: Optional[str] = Field(None, alias='expenseRatio')
    category: Optional[str] = None
    last_capital_gain: Optional[str] = Field(None, alias='lastCapitalGain')
    morningstar_rating: Optional[str] = Field(None, alias='morningstarRating')
    morningstar_risk_rating: Optional[str] = Field(None, alias='morningstarRiskRating')
    holdings_turnover: Optional[str] = Field(None, alias='holdingsTurnover')
    earnings_date: Optional[str] = Field(None, alias='earningsDate')
    last_dividend: Optional[str] = Field(None, alias='lastDividend')
    inception_date: Optional[str] = Field(None, alias='inceptionDate')
    sector: Optional[str] = None
    industry: Optional[str] = None
    about: Optional[str] = None
    employees: Optional[str] = None
    five_days_return: Optional[str] = Field(None, alias='fiveDaysReturn')
    one_month_return: Optional[str] = Field(None, alias='oneMonthReturn')
    three_month_return: Optional[str] = Field(None, alias='threeMonthReturn')
    six_month_return: Optional[str] = Field(None, alias='sixMonthReturn')
    ytd_return: Optional[str] = Field(None, alias='ytdReturn')
    year_return: Optional[str] = Field(None, alias='yearReturn')
    three_year_return: Optional[str] = Field(None, alias='threeYearReturn')
    five_year_return: Optional[str] = Field(None, alias='fiveYearReturn')
    ten_year_return: Optional[str] = Field(None, alias='tenYearReturn')
    max_return: Optional[str] = Field(None, alias='maxReturn')


class SimpleQuote(Quote):
    pass


class SimilarStock(Quote):
    pass


class HistoricalDataPoint(BaseModel):
    open: float
    high: float
    low: float
    close: float
    adj_close: Optional[float] = Field(None, alias='adjClose')
    volume: int


class MarketMover(BaseModel):
    symbol: str
    name: str
    price: str
    change: str
    percent_change: str = Field(alias='percentChange')


class StockNews(BaseModel):
    title: str
    link: str
    source: str
    img: str
    time: str


class SymbolSearchResult(BaseModel):
    name: str
    symbol: str
    exchange: str
    type: str


class SectorPerformance(BaseModel):
    sector: str
    day_return: str = Field(alias='dayReturn')
    ytd_return: str = Field(alias='ytdReturn')
    year_return: str = Field(alias='yearReturn')
    three_year_return: str = Field(alias='threeYearReturn')
    five_year_return: str = Field(alias='fiveYearReturn')


# Enums
class StatementType(str, Enum):
    INCOME = "income"
    BALANCE = "balance"
    CASHFLOW = "cashflow"


class Frequency(str, Enum):
    ANNUAL = "annual"
    QUARTERLY = "quarterly"


class HolderType(str, Enum):
    MAJOR = "major"
    INSTITUTIONAL = "institutional"
    MUTUALFUND = "mutualfund"
    INSIDER_TRANSACTIONS = "insider_transactions"
    INSIDER_PURCHASES = "insider_purchases"
    INSIDER_ROSTER = "insider_roster"


# Financial Statements Models
class FinancialStatement(BaseModel):
    symbol: str
    statement_type: StatementType
    frequency: Frequency
    statement: Dict[str, Dict[str, Union[int, float, None]]]


# Holders Models
class MajorHoldersBreakdown(BaseModel):
    insider_percent: Optional[str] = Field(None, alias='insiderPercent')
    institution_percent: Optional[str] = Field(None, alias='institutionPercent')
    institution_float_percent: Optional[str] = Field(None, alias='institutionFloatPercent')
    institution_count: Optional[str] = Field(None, alias='institutionCount')


class InstitutionalHolder(BaseModel):
    holder: str
    shares: Optional[int] = None
    date_reported: Optional[str] = Field(None, alias='dateReported')
    percent_out: Optional[str] = Field(None, alias='percentOut')
    value: Optional[int] = None


class MutualFundHolder(BaseModel):
    holder: str
    shares: Optional[int] = None
    date_reported: Optional[str] = Field(None, alias='dateReported')
    percent_out: Optional[str] = Field(None, alias='percentOut')
    value: Optional[int] = None


class InsiderTransaction(BaseModel):
    start_date: Optional[datetime] = Field(None, alias='startDate')
    insider: Optional[str] = None
    position: Optional[str] = None
    transaction: Optional[str] = None
    shares: Optional[int] = None
    value: Optional[int] = None
    ownership: Optional[str] = None


class InsiderPurchase(BaseModel):
    shares: Optional[int] = None
    transactions: Optional[int] = None
    purchase_activity: Optional[str] = Field(None, alias='purchaseActivity')


class InsiderRosterMember(BaseModel):
    name: Optional[str] = None
    position: Optional[str] = None
    url: Optional[str] = None
    most_recent_transaction: Optional[str] = Field(None, alias='mostRecentTransaction')
    latest_transaction_date: Optional[str] = Field(None, alias='latestTransactionDate')
    shares_owned_directly: Optional[int] = Field(None, alias='sharesOwnedDirectly')


class HoldersData(BaseModel):
    symbol: str
    holder_type: HolderType
    major_breakdown: Optional[MajorHoldersBreakdown] = Field(None, alias='majorBreakdown')
    institutional_holders: Optional[List[InstitutionalHolder]] = Field(None, alias='institutionalHolders')
    mutualfund_holders: Optional[List[MutualFundHolder]] = Field(None, alias='mutualfundHolders')
    insider_transactions: Optional[List[InsiderTransaction]] = Field(None, alias='insiderTransactions')
    insider_purchases: Optional[InsiderPurchase] = Field(None, alias='insiderPurchases')
    insider_roster: Optional[List[InsiderRosterMember]] = Field(None, alias='insiderRoster')


# Earnings Transcript Models
class TranscriptMetadata(BaseModel):
    source: Optional[str] = None
    retrieved_at: Optional[datetime] = Field(None, alias='retrievedAt')
    transcripts_id: Optional[int] = Field(None, alias='transcriptsId')


class TranscriptItem(BaseModel):
    symbol: str
    quarter: str
    year: int
    date: Optional[datetime] = None
    transcript: str
    participants: Optional[List[str]] = None
    metadata: Optional[TranscriptMetadata] = None


class EarningsTranscript(BaseModel):
    symbol: str
    transcripts: List[TranscriptItem]


# Technical Indicators Models
class SMAData(BaseModel):
    date: str
    sma: Optional[float] = None


class EMAData(BaseModel):
    date: str
    ema: Optional[float] = None


class WMAData(BaseModel):
    date: str
    wma: Optional[float] = None


class VWMAData(BaseModel):
    date: str
    vwma: Optional[float] = None


class RSIData(BaseModel):
    date: str
    rsi: Optional[float] = None


class SRSIData(BaseModel):
    date: str
    k_percent: Optional[float] = Field(None, alias='kPercent')
    d_percent: Optional[float] = Field(None, alias='dPercent')


class STOCHData(BaseModel):
    date: str
    k_percent: Optional[float] = Field(None, alias='kPercent')
    d_percent: Optional[float] = Field(None, alias='dPercent')


class CCIData(BaseModel):
    date: str
    cci: Optional[float] = None


class MACDData(BaseModel):
    date: str
    macd: Optional[float] = None
    signal: Optional[float] = None
    histogram: Optional[float] = None


class ADXData(BaseModel):
    date: str
    adx: Optional[float] = None
    plus_di: Optional[float] = Field(None, alias='plusDI')
    minus_di: Optional[float] = Field(None, alias='minusDI')


class AROONData(BaseModel):
    date: str
    aroon_up: Optional[float] = Field(None, alias='aroonUp')
    aroon_down: Optional[float] = Field(None, alias='aroonDown')
    aroon_oscillator: Optional[float] = Field(None, alias='aroonOscillator')


class BBANDSData(BaseModel):
    date: str
    upper_band: Optional[float] = Field(None, alias='upperBand')
    middle_band: Optional[float] = Field(None, alias='middleBand')
    lower_band: Optional[float] = Field(None, alias='lowerBand')


class OBVData(BaseModel):
    date: str
    obv: Optional[float] = None


class SuperTrendData(BaseModel):
    date: str
    super_trend: Optional[float] = Field(None, alias='superTrend')
    trend: Optional[str] = None


class IchimokuData(BaseModel):
    date: str
    tenkan_sen: Optional[float] = Field(None, alias='tenkanSen')
    kijun_sen: Optional[float] = Field(None, alias='kijunSen')
    senkou_span_a: Optional[float] = Field(None, alias='senkouSpanA')
    senkou_span_b: Optional[float] = Field(None, alias='senkouSpanB')
    chikou_span: Optional[float] = Field(None, alias='chikouSpan')


class TechnicalIndicator(BaseModel):
    symbol: str
    indicator: str
    data: Union[
        List[SMAData],
        List[EMAData],
        List[WMAData],
        List[VWMAData],
        List[RSIData],
        List[SRSIData],
        List[STOCHData],
        List[CCIData],
        List[MACDData],
        List[ADXData],
        List[AROONData],
        List[BBANDSData],
        List[OBVData],
        List[SuperTrendData],
        List[IchimokuData]
    ]


# Market Index Models
class MarketIndex(BaseModel):
    name: str
    value: Optional[str] = None
    change: Optional[str] = None
    percent_change: Optional[str] = Field(None, alias='percentChange')
    five_days_return: Optional[str] = Field(None, alias='fiveDaysReturn')
    one_month_return: Optional[str] = Field(None, alias='oneMonthReturn')
    three_month_return: Optional[str] = Field(None, alias='threeMonthReturn')
    six_month_return: Optional[str] = Field(None, alias='sixMonthReturn')
    ytd_return: Optional[str] = Field(None, alias='ytdReturn')
    year_return: Optional[str] = Field(None, alias='yearReturn')
    three_year_return: Optional[str] = Field(None, alias='threeYearReturn')
    five_year_return: Optional[str] = Field(None, alias='fiveYearReturn')
    ten_year_return: Optional[str] = Field(None, alias='tenYearReturn')
    max_return: Optional[str] = Field(None, alias='maxReturn')
