"""Tests for base models and enums in marketdata_providers"""

import pytest
from decimal import Decimal
from datetime import datetime, date
from marketdata_providers.base import (
    MarketDataType,
    Interval,
    StockQuote,
    HistoricalPrice,
    OptionQuote,
    CompanyInfo,
    EconomicEvent,
    EarningsCalendar,
    EarningsCallTranscript,
    DividendRecord,
    NewsArticle,
    EarningsSurprise,
    StockSplit,
    IPOCalendar,
    AnalystEstimates,
    MarketHoliday,
    TechnicalIndicator,
    ForexQuote,
    CryptoQuote,
    MarketIndex,
    ExchangeInfo,
    MarketConditions,
    TiingoFundamentalData,
    Logo,
    ExchangeRate,
    CurrencyConversion,
    MarketMover,
    SimplePrice,
    EodPrice,
    SupportedSymbol,
    ForexPair,
    Cryptocurrency,
    MarketStatus
)


class TestMarketDataType:
    """Test MarketDataType enum"""
    
    def test_enum_values(self):
        """Test that enum has expected values"""
        assert MarketDataType.QUOTE.value == "quote"
        assert MarketDataType.HISTORICAL.value == "historical"
        assert MarketDataType.INTRADAY.value == "intraday"
        assert MarketDataType.OPTIONS.value == "options"
        assert MarketDataType.OPTIONS_CHAIN.value == "options_chain"
        assert MarketDataType.FUNDAMENTALS.value == "fundamentals"
        assert MarketDataType.EARNINGS.value == "earnings"
        assert MarketDataType.DIVIDENDS.value == "dividends"
        assert MarketDataType.NEWS.value == "news"
        assert MarketDataType.COMPANY_INFO.value == "company_info"
        assert MarketDataType.TECHNICAL_INDICATORS.value == "technical_indicators"
        assert MarketDataType.ECONOMIC_DATA.value == "economic_data"


class TestInterval:
    """Test Interval enum"""
    
    def test_enum_values(self):
        """Test that interval enum has expected values"""
        assert Interval.MIN_1.value == "1min"
        assert Interval.MIN_5.value == "5min"
        assert Interval.MIN_15.value == "15min"
        assert Interval.MIN_30.value == "30min"
        assert Interval.HOUR_1.value == "1h"
        assert Interval.HOUR_4.value == "4h"
        assert Interval.DAILY.value == "1d"
        assert Interval.WEEKLY.value == "1w"
        assert Interval.MONTHLY.value == "1m"


class TestStockQuote:
    """Test StockQuote model"""
    
    def test_stock_quote_creation(self):
        """Test creating a StockQuote instance"""
        quote = StockQuote(
            symbol="AAPL",
            price=Decimal("150.25"),
            change=Decimal("2.50"),
            change_percent=Decimal("1.69"),
            volume=1000000,
            timestamp=datetime(2023, 1, 15, 16, 0, 0),
            provider="test_provider"
        )
        
        assert quote.symbol == "AAPL"
        assert quote.price == Decimal("150.25")
        assert quote.change == Decimal("2.50")
        assert quote.change_percent == Decimal("1.69")
        assert quote.volume == 1000000
        assert quote.open is None  # Optional field
    
    def test_stock_quote_with_optional_fields(self):
        """Test StockQuote with optional fields"""
        quote = StockQuote(
            symbol="GOOGL",
            price=Decimal("2500.00"),
            change=Decimal("-10.00"),
            change_percent=Decimal("-0.40"),
            volume=500000,
            timestamp=datetime(2023, 1, 15, 16, 0, 0),
            provider="test_provider",
            open=Decimal("2510.00"),
            high=Decimal("2520.00"),
            low=Decimal("2495.00"),
            previous_close=Decimal("2510.00")
        )
        
        assert quote.open == Decimal("2510.00")
        assert quote.high == Decimal("2520.00")
        assert quote.low == Decimal("2495.00")
        assert quote.previous_close == Decimal("2510.00")


class TestHistoricalPrice:
    """Test HistoricalPrice model"""
    
    def test_historical_price_creation(self):
        """Test creating a HistoricalPrice instance"""
        price = HistoricalPrice(
            symbol="TSLA",
            date=date(2023, 1, 15),
            open=Decimal("200.00"),
            high=Decimal("205.00"),
            low=Decimal("195.00"),
            close=Decimal("202.50"),
            volume=2000000,
            provider="test_provider"
        )
        
        assert price.symbol == "TSLA"
        assert price.date == date(2023, 1, 15)
        assert price.open == Decimal("200.00")
        assert price.high == Decimal("205.00")
        assert price.low == Decimal("195.00")
        assert price.close == Decimal("202.50")
        assert price.volume == 2000000


class TestOptionQuote:
    """Test OptionQuote model"""
    
    def test_option_quote_creation(self):
        """Test creating an OptionQuote instance"""
        option = OptionQuote(
            symbol="AAPL240315C00150000",
            underlying_symbol="AAPL",
            strike=Decimal("150.00"),
            expiration=date(2024, 3, 15),
            option_type="call",
            bid=Decimal("5.20"),
            ask=Decimal("5.40"),
            last_price=Decimal("5.30"),
            volume=1000,
            open_interest=5000,
            timestamp=datetime(2023, 1, 15, 16, 0, 0),
            provider="test_provider"
        )
        
        assert option.symbol == "AAPL240315C00150000"
        assert option.underlying_symbol == "AAPL"
        assert option.strike == Decimal("150.00")
        assert option.expiration == date(2024, 3, 15)
        assert option.option_type == "call"
        assert option.bid == Decimal("5.20")
        assert option.ask == Decimal("5.40")
        assert option.last_price == Decimal("5.30")
        assert option.volume == 1000
        assert option.open_interest == 5000


class TestCompanyInfo:
    """Test CompanyInfo model"""
    
    def test_company_info_creation(self):
        """Test creating a CompanyInfo instance"""
        info = CompanyInfo(
            symbol="MSFT",
            name="Microsoft Corporation",
            description="Technology company",
            sector="Technology",
            industry="Software",
            market_cap=2000000000000,
            employees=200000,
            provider="test_provider"
        )
        
        assert info.symbol == "MSFT"
        assert info.name == "Microsoft Corporation"
        assert info.description == "Technology company"
        assert info.sector == "Technology"
        assert info.industry == "Software"
        assert info.market_cap == 2000000000000
        assert info.employees == 200000


class TestSimplePrice:
    """Test SimplePrice model"""
    
    def test_simple_price_creation(self):
        """Test creating a SimplePrice instance"""
        price = SimplePrice(
            symbol="BTC",
            price=Decimal("45000.00"),
            provider="test_provider"
        )
        
        assert price.symbol == "BTC"
        assert price.price == Decimal("45000.00")
        assert price.provider == "test_provider"
    
    def test_simple_price_with_different_values(self):
        """Test SimplePrice with different values"""
        price = SimplePrice(
            symbol="ETH",
            price=Decimal("3000.00"),
            provider="another_provider"
        )
        
        assert price.symbol == "ETH"
        assert price.price == Decimal("3000.00")
        assert price.provider == "another_provider"


class TestForexQuote:
    """Test ForexQuote model"""
    
    def test_forex_quote_creation(self):
        """Test creating a ForexQuote instance"""
        quote = ForexQuote(
            from_currency="EUR",
            to_currency="USD",
            symbol="EURUSD",
            price=Decimal("1.0851"),
            timestamp=datetime(2023, 1, 15, 10, 30, 0),
            provider="test_provider"
        )
        
        assert quote.from_currency == "EUR"
        assert quote.to_currency == "USD"
        assert quote.symbol == "EURUSD"
        assert quote.price == Decimal("1.0851")
        assert quote.timestamp == datetime(2023, 1, 15, 10, 30, 0)


class TestCryptoQuote:
    """Test CryptoQuote model"""
    
    def test_crypto_quote_creation(self):
        """Test creating a CryptoQuote instance"""
        crypto = CryptoQuote(
            symbol="BTCUSD",
            price=Decimal("45000.00"),
            volume_24h=Decimal("1000000.00"),
            change_24h=Decimal("2.5"),
            change_percent_24h=Decimal("5.88")
        )
        
        assert crypto.symbol == "BTCUSD"
        assert crypto.price == Decimal("45000.00")
        assert crypto.volume_24h == Decimal("1000000.00")
        assert crypto.change_24h == Decimal("2.5")
        assert crypto.change_percent_24h == Decimal("5.88")


class TestNewsArticle:
    """Test NewsArticle model"""
    
    def test_news_article_creation(self):
        """Test creating a NewsArticle instance"""
        article = NewsArticle(
            title="Market Update",
            content="Stock market closed higher today",
            url="https://example.com/news",
            published_at=datetime(2023, 1, 15, 16, 0, 0),
            source="Financial News"
        )
        
        assert article.title == "Market Update"
        assert article.content == "Stock market closed higher today"
        assert article.url == "https://example.com/news"
        assert article.published_at == datetime(2023, 1, 15, 16, 0, 0)
        assert article.source == "Financial News"


class TestEarningsCalendar:
    """Test EarningsCalendar model"""
    
    def test_earnings_calendar_creation(self):
        """Test creating an EarningsCalendar instance"""
        earnings = EarningsCalendar(
            symbol="AAPL",
            company_name="Apple Inc.",
            report_date=date(2023, 1, 26),
            fiscal_date_ending=date(2022, 12, 31),
            estimate=Decimal("1.94")
        )
        
        assert earnings.symbol == "AAPL"
        assert earnings.company_name == "Apple Inc."
        assert earnings.report_date == date(2023, 1, 26)
        assert earnings.fiscal_date_ending == date(2022, 12, 31)
        assert earnings.estimate == Decimal("1.94")


class TestDividendRecord:
    """Test DividendRecord model"""
    
    def test_dividend_record_creation(self):
        """Test creating a DividendRecord instance"""
        dividend = DividendRecord(
            symbol="KO",
            ex_date=date(2023, 2, 14),
            record_date=date(2023, 2, 16),
            payment_date=date(2023, 4, 3),
            amount=Decimal("0.46")
        )
        
        assert dividend.symbol == "KO"
        assert dividend.ex_date == date(2023, 2, 14)
        assert dividend.record_date == date(2023, 2, 16)
        assert dividend.payment_date == date(2023, 4, 3)
        assert dividend.amount == Decimal("0.46")


if __name__ == "__main__":
    pytest.main([__file__])
