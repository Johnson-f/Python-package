from pydantic import BaseModel, Field
from typing import Optional, List


class CompanyProfile(BaseModel):
    country: Optional[str] = None
    currency: Optional[str] = None
    exchange: Optional[str] = None
    finnhub_industry: Optional[str] = Field(None, alias='finnhubIndustry')
    ipo: Optional[str] = None
    logo: Optional[str] = None
    market_capitalization: Optional[float] = Field(None, alias='marketCapitalization')
    name: Optional[str] = None
    phone: Optional[str] = None
    share_outstanding: Optional[float] = Field(None, alias='shareOutstanding')
    ticker: Optional[str] = None
    weburl: Optional[str] = None


class Quote(BaseModel):
    current_price: Optional[float] = Field(None, alias='c')
    high_price_of_the_day: Optional[float] = Field(None, alias='h')
    low_price_of_the_day: Optional[float] = Field(None, alias='l')
    open_price_of_the_day: Optional[float] = Field(None, alias='o')
    previous_close_price: Optional[float] = Field(None, alias='pc')
    timestamp: Optional[int] = Field(None, alias='t')


class MarketNews(BaseModel):
    category: Optional[str] = None
    datetime: Optional[int] = None
    headline: Optional[str] = None
    id: Optional[int] = None
    image: Optional[str] = None
    related: Optional[str] = None
    source: Optional[str] = None
    summary: Optional[str] = None
    url: Optional[str] = None
