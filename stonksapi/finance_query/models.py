from pydantic import BaseModel, Field
from typing import Optional, List, Dict


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
