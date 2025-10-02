from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class TickerDetails(BaseModel):
    ticker: str
    name: str
    market: str
    locale: str
    primary_exchange: Optional[str] = Field(None, alias='primary_exchange')
    type: Optional[str] = None
    active: bool
    currency_name: Optional[str] = Field(None, alias='currency_name')
    cik: Optional[str] = None
    composite_figi: Optional[str] = Field(None, alias='composite_figi')
    share_class_figi: Optional[str] = Field(None, alias='share_class_figi')
    last_updated_utc: Optional[str] = Field(None, alias='last_updated_utc')


class Aggregate(BaseModel):
    open: float = Field(alias='o')
    high: float = Field(alias='h')
    low: float = Field(alias='l')
    close: float = Field(alias='c')
    volume: int = Field(alias='v')
    vwap: Optional[float] = Field(None, alias='vw')
    timestamp: int = Field(alias='t')
    transactions: Optional[int] = Field(None, alias='n')


class DailyOpenClose(BaseModel):
    status: str
    from_date: str = Field(alias='from')
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    after_hours: float = Field(alias='afterHours')
    pre_market: float = Field(alias='preMarket')


class LastQuote(BaseModel):
    ticker: str = Field(alias='T')
    bid_size: int = Field(alias='S')
    bid_price: float = Field(alias='P')
    bid_exchange: int = Field(alias='X')
    ask_size: int = Field(alias='s')
    ask_price: float = Field(alias='p')
    ask_exchange: int = Field(alias='x')
    timestamp: int = Field(alias='t')


class Publisher(BaseModel):
    name: str
    homepage_url: Optional[str] = Field(None, alias='homepage_url')
    logo_url: Optional[str] = Field(None, alias='logo_url')
    favicon_url: Optional[str] = Field(None, alias='favicon_url')


class NewsArticle(BaseModel):
    id: str
    publisher: Publisher
    title: str
    author: str
    published_utc: str
    article_url: str
    tickers: List[str]
    image_url: Optional[str] = Field(None, alias='image_url')
    description: Optional[str] = None
    keywords: Optional[List[str]] = None


class IndicatorValue(BaseModel):
    timestamp: int
    value: float


class MACDValue(BaseModel):
    timestamp: int
    value: float
    signal: float
    histogram: float


class OptionContract(BaseModel):
    ticker: str
    cfi: Optional[str] = None
    contract_type: Optional[str] = Field(None, alias='contract_type')
    exercise_style: Optional[str] = Field(None, alias='exercise_style')
    expiration_date: Optional[str] = Field(None, alias='expiration_date')
    primary_exchange: Optional[str] = Field(None, alias='primary_exchange')
    shares_per_contract: Optional[float] = Field(None, alias='shares_per_contract')
    strike_price: Optional[float] = Field(None, alias='strike_price')
    underlying_ticker: Optional[str] = Field(None, alias='underlying_ticker')


class LastQuoteForOption(BaseModel):
    ticker: str
    bid: float
    bid_size: int
    ask: float
    ask_size: int
    last_price: float
    last_size: int
    timestamp: int


class Financials(BaseModel):
    balance_sheet: Dict[str, Any]
    cash_flow_statement: Dict[str, Any]
    income_statement: Dict[str, Any]
    comprehensive_income: Dict[str, Any]


class StockFinancial(BaseModel):
    cik: str
    company_name: str
    end_date: str
    filing_date: str
    financials: Financials
    fiscal_period: str
    fiscal_year: str
    source_filing_file_url: str
    source_filing_url: str
    start_date: str