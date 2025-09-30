"""
Alpha Vantage API Client wrapper.

This module provides a comprehensive Python wrapper around the Alpha Vantage API,
using the alpha-vantage library with Pydantic models for type safety.
"""

import os
from enum import Enum
from typing import Optional

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.techindicators import TechIndicators

from .models import (
    CompanyOverview,
    CryptoTimeSeries,
    DailyAdjustedTimeSeries,
    DailyTimeSeries,
    Earnings,
    EconomicIndicatorResponse,
    ExchangeRateResponse,
    ForexTimeSeries,
    GlobalQuote,
    IntradayTimeSeries,
    MonthlyTimeSeries,
    NewsSentimentResponse,
    QuoteResponse,
    SymbolSearchResponse,
    TechnicalIndicatorResponse,
    WeeklyTimeSeries,
)


class OutputSize(str, Enum):
    """Output size options for time series data."""

    COMPACT = "compact"
    FULL = "full"


class Interval(str, Enum):
    """Time interval options for intraday data."""

    MIN_1 = "1min"
    MIN_5 = "5min"
    MIN_15 = "15min"
    MIN_30 = "30min"
    MIN_60 = "60min"


class AlphaVantageClient:
    """
    Comprehensive client for Alpha Vantage API.

    This client wraps the alpha-vantage library and provides strongly-typed
    responses using Pydantic models.

    Args:
        api_key: Your Alpha Vantage API key. If not provided, will read from
                 ALPHA_VANTAGE_API_KEY environment variable.
        output_format: Output format for API responses (default: 'json')

    Example:
        >>> client = AlphaVantageClient(api_key="your_api_key")
        >>> quote = client.get_quote("AAPL")
        >>> print(f"Price: {quote.global_quote.price}")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        output_format: str = "json",
    ):
        """Initialize the Alpha Vantage client."""
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either as argument or via "
                "ALPHA_VANTAGE_API_KEY environment variable"
            )

        self.output_format = output_format

        # Initialize Alpha Vantage library clients
        self._ts = TimeSeries(key=self.api_key, output_format=output_format)
        self._fd = FundamentalData(key=self.api_key, output_format=output_format)
        self._fx = ForeignExchange(key=self.api_key, output_format=output_format)
        self._crypto = CryptoCurrencies(key=self.api_key, output_format=output_format)
        self._ti = TechIndicators(key=self.api_key, output_format=output_format)

    # ==================== Time Series Methods ====================

    def get_intraday(
        self,
        symbol: str,
        interval: Interval = Interval.MIN_5,
        adjusted: bool = True,
        extended_hours: bool = True,
        month: Optional[str] = None,
        outputsize: OutputSize = OutputSize.COMPACT,
    ) -> IntradayTimeSeries:
        """
        Get intraday time series data.

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'IBM')
            interval: Time interval between data points
            adjusted: Whether to return adjusted data (splits/dividends)
            extended_hours: Include pre-market and post-market data
            month: Specific month in YYYY-MM format (e.g., '2023-01')
            outputsize: Amount of data to return

        Returns:
            IntradayTimeSeries: Typed intraday data with metadata

        Example:
            >>> data = client.get_intraday("AAPL", interval=Interval.MIN_5)
            >>> for timestamp, ohlcv in data.time_series.items():
            ...     print(f"{timestamp}: Close ${ohlcv.close}")
        """
        data, _ = self._ts.get_intraday(
            symbol=symbol,
            interval=interval.value,
            outputsize=outputsize.value,
        )
        return IntradayTimeSeries.model_validate(data)

    def get_daily(
        self,
        symbol: str,
        outputsize: OutputSize = OutputSize.COMPACT,
    ) -> DailyTimeSeries:
        """
        Get daily time series data.

        Args:
            symbol: Stock ticker symbol
            outputsize: Amount of data to return (compact: 100 days, full: 20+ years)

        Returns:
            DailyTimeSeries: Typed daily OHLCV data

        Example:
            >>> data = client.get_daily("AAPL")
            >>> latest_date = list(data.time_series.keys())[0]
            >>> latest_data = data.time_series[latest_date]
            >>> print(f"Latest close: ${latest_data.close}")
        """
        data, _ = self._ts.get_daily(symbol=symbol, outputsize=outputsize.value)
        return DailyTimeSeries.model_validate(data)

    def get_daily_adjusted(
        self,
        symbol: str,
        outputsize: OutputSize = OutputSize.COMPACT,
    ) -> DailyAdjustedTimeSeries:
        """
        Get daily adjusted time series data (includes dividend and split info).

        Args:
            symbol: Stock ticker symbol
            outputsize: Amount of data to return

        Returns:
            DailyAdjustedTimeSeries: Typed daily data with adjustments

        Example:
            >>> data = client.get_daily_adjusted("AAPL")
            >>> for date, ohlcv in data.time_series.items():
            ...     print(f"{date}: Adjusted Close ${ohlcv.adjusted_close}")
        """
        data, _ = self._ts.get_daily_adjusted(symbol=symbol, outputsize=outputsize.value)
        return DailyAdjustedTimeSeries.model_validate(data)

    def get_weekly(self, symbol: str) -> WeeklyTimeSeries:
        """
        Get weekly time series data.

        Args:
            symbol: Stock ticker symbol

        Returns:
            WeeklyTimeSeries: Typed weekly OHLCV data

        Example:
            >>> data = client.get_weekly("AAPL")
            >>> print(f"Total weeks: {len(data.time_series)}")
        """
        data, _ = self._ts.get_weekly(symbol=symbol)
        return WeeklyTimeSeries.model_validate(data)

    def get_monthly(self, symbol: str) -> MonthlyTimeSeries:
        """
        Get monthly time series data.

        Args:
            symbol: Stock ticker symbol

        Returns:
            MonthlyTimeSeries: Typed monthly OHLCV data

        Example:
            >>> data = client.get_monthly("AAPL")
            >>> print(f"Total months: {len(data.time_series)}")
        """
        data, _ = self._ts.get_monthly(symbol=symbol)
        return MonthlyTimeSeries.model_validate(data)

    def get_quote(self, symbol: str) -> QuoteResponse:
        """
        Get real-time quote for a symbol.

        Args:
            symbol: Stock ticker symbol

        Returns:
            QuoteResponse: Current quote with price, volume, and changes

        Example:
            >>> quote = client.get_quote("AAPL")
            >>> print(f"Current price: ${quote.global_quote.price}")
            >>> print(f"Change: {quote.global_quote.change_percent}")
        """
        data, _ = self._ts.get_quote_endpoint(symbol=symbol)
        return QuoteResponse.model_validate(data)

    def search_symbols(self, keywords: str) -> SymbolSearchResponse:
        """
        Search for symbols matching keywords.

        Args:
            keywords: Search terms (company name, ticker, etc.)

        Returns:
            SymbolSearchResponse: List of matching symbols with details

        Example:
            >>> results = client.search_symbols("Apple")
            >>> for match in results.best_matches:
            ...     print(f"{match.symbol}: {match.name} ({match.region})")
        """
        data, _ = self._ts.get_symbol_search(keywords=keywords)
        return SymbolSearchResponse.model_validate(data)

    # ==================== Fundamental Data Methods ====================

    def get_company_overview(self, symbol: str) -> CompanyOverview:
        """
        Get comprehensive company overview and financial metrics.

        Args:
            symbol: Stock ticker symbol

        Returns:
            CompanyOverview: Company info, ratios, and fundamental metrics

        Example:
            >>> overview = client.get_company_overview("AAPL")
            >>> print(f"Company: {overview.name}")
            >>> print(f"Sector: {overview.sector}")
            >>> print(f"P/E Ratio: {overview.pe_ratio}")
            >>> print(f"Market Cap: {overview.market_capitalization}")
        """
        data, _ = self._fd.get_company_overview(symbol=symbol)
        return CompanyOverview.model_validate(data)

    def get_earnings(self, symbol: str) -> Earnings:
        """
        Get quarterly and annual earnings data.

        Args:
            symbol: Stock ticker symbol

        Returns:
            Earnings: Historical earnings data with estimates and surprises

        Example:
            >>> earnings = client.get_earnings("AAPL")
            >>> for quarter in earnings.quarterly_earnings[:4]:
            ...     print(f"{quarter.fiscal_date_ending}: "
            ...           f"EPS ${quarter.reported_eps}")
        """
        data, _ = self._fd.get_earnings(symbol=symbol)
        return Earnings.model_validate(data)

    # ==================== Forex Methods ====================

    def get_currency_exchange_rate(
        self,
        from_currency: str,
        to_currency: str,
    ) -> ExchangeRateResponse:
        """
        Get real-time exchange rate between two currencies.

        Args:
            from_currency: Source currency code (e.g., 'USD', 'EUR')
            to_currency: Target currency code (e.g., 'JPY', 'GBP')

        Returns:
            ExchangeRateResponse: Current exchange rate with bid/ask

        Example:
            >>> rate = client.get_currency_exchange_rate("USD", "EUR")
            >>> exchange = rate.realtime_currency_exchange_rate
            >>> print(f"1 {exchange.from_currency_code} = "
            ...       f"{exchange.exchange_rate} {exchange.to_currency_code}")
        """
        data, _ = self._fx.get_currency_exchange_rate(
            from_currency=from_currency,
            to_currency=to_currency,
        )
        return ExchangeRateResponse.model_validate(data)

    def get_forex_intraday(
        self,
        from_symbol: str,
        to_symbol: str,
        interval: Interval = Interval.MIN_5,
        outputsize: OutputSize = OutputSize.COMPACT,
    ) -> ForexTimeSeries:
        """
        Get intraday forex time series data.

        Args:
            from_symbol: Base currency code
            to_symbol: Quote currency code
            interval: Time interval between data points
            outputsize: Amount of data to return

        Returns:
            ForexTimeSeries: Typed intraday forex OHLC data

        Example:
            >>> data = client.get_forex_intraday("EUR", "USD")
            >>> for timestamp, ohlc in list(data.time_series.items())[:5]:
            ...     print(f"{timestamp}: {ohlc.close}")
        """
        data, _ = self._fx.get_currency_exchange_intraday(
            from_symbol=from_symbol,
            to_symbol=to_symbol,
            interval=interval.value,
            outputsize=outputsize.value,
        )
        return ForexTimeSeries.model_validate(data)

    # ==================== Crypto Methods ====================

    def get_crypto_intraday(
        self,
        symbol: str,
        market: str = "USD",
        interval: Interval = Interval.MIN_5,
    ) -> CryptoTimeSeries:
        """
        Get intraday cryptocurrency time series data.

        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
            market: Market currency (e.g., 'USD', 'EUR')
            interval: Time interval between data points

        Returns:
            CryptoTimeSeries: Typed intraday crypto OHLCV data

        Example:
            >>> data = client.get_crypto_intraday("BTC", market="USD")
            >>> for timestamp, ohlcv in list(data.time_series.items())[:5]:
            ...     print(f"{timestamp}: ${ohlcv.close}")
        """
        data, _ = self._crypto.get_digital_currency_intraday(
            symbol=symbol,
            market=market,
            interval=interval.value,
        )
        return CryptoTimeSeries.model_validate(data)

    def get_crypto_daily(
        self,
        symbol: str,
        market: str = "USD",
    ) -> CryptoTimeSeries:
        """
        Get daily cryptocurrency time series data.

        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
            market: Market currency (e.g., 'USD', 'EUR')

        Returns:
            CryptoTimeSeries: Typed daily crypto OHLCV data

        Example:
            >>> data = client.get_crypto_daily("BTC", market="USD")
            >>> latest_date = list(data.time_series.keys())[0]
            >>> print(f"Latest BTC price: ${data.time_series[latest_date].close}")
        """
        data, _ = self._crypto.get_digital_currency_daily(
            symbol=symbol,
            market=market,
        )
        return CryptoTimeSeries.model_validate(data)

    # ==================== Technical Indicators Methods ====================

    def get_sma(
        self,
        symbol: str,
        interval: Interval = Interval.MIN_5,
        time_period: int = 20,
        series_type: str = "close",
    ) -> TechnicalIndicatorResponse:
        """
        Get Simple Moving Average (SMA) technical indicator.

        Args:
            symbol: Stock ticker symbol
            interval: Time interval
            time_period: Number of data points for calculation
            series_type: Price type ('close', 'open', 'high', 'low')

        Returns:
            TechnicalIndicatorResponse: SMA values with metadata

        Example:
            >>> sma = client.get_sma("AAPL", time_period=20)
            >>> for timestamp, values in list(sma.technical_analysis.items())[:5]:
            ...     print(f"{timestamp}: SMA = {values['SMA']}")
        """
        data, _ = self._ti.get_sma(
            symbol=symbol,
            interval=interval.value,
            time_period=time_period,
            series_type=series_type,
        )
        return TechnicalIndicatorResponse.model_validate(data)

    def get_ema(
        self,
        symbol: str,
        interval: Interval = Interval.MIN_5,
        time_period: int = 20,
        series_type: str = "close",
    ) -> TechnicalIndicatorResponse:
        """
        Get Exponential Moving Average (EMA) technical indicator.

        Args:
            symbol: Stock ticker symbol
            interval: Time interval
            time_period: Number of data points for calculation
            series_type: Price type ('close', 'open', 'high', 'low')

        Returns:
            TechnicalIndicatorResponse: EMA values with metadata

        Example:
            >>> ema = client.get_ema("AAPL", time_period=12)
            >>> for timestamp, values in list(ema.technical_analysis.items())[:5]:
            ...     print(f"{timestamp}: EMA = {values['EMA']}")
        """
        data, _ = self._ti.get_ema(
            symbol=symbol,
            interval=interval.value,
            time_period=time_period,
            series_type=series_type,
        )
        return TechnicalIndicatorResponse.model_validate(data)

    def get_rsi(
        self,
        symbol: str,
        interval: Interval = Interval.MIN_5,
        time_period: int = 14,
        series_type: str = "close",
    ) -> TechnicalIndicatorResponse:
        """
        Get Relative Strength Index (RSI) technical indicator.

        Args:
            symbol: Stock ticker symbol
            interval: Time interval
            time_period: Number of data points for calculation
            series_type: Price type ('close', 'open', 'high', 'low')

        Returns:
            TechnicalIndicatorResponse: RSI values with metadata

        Example:
            >>> rsi = client.get_rsi("AAPL")
            >>> for timestamp, values in list(rsi.technical_analysis.items())[:5]:
            ...     print(f"{timestamp}: RSI = {values['RSI']}")
        """
        data, _ = self._ti.get_rsi(
            symbol=symbol,
            interval=interval.value,
            time_period=time_period,
            series_type=series_type,
        )
        return TechnicalIndicatorResponse.model_validate(data)

    def get_macd(
        self,
        symbol: str,
        interval: Interval = Interval.MIN_5,
        series_type: str = "close",
        fastperiod: int = 12,
        slowperiod: int = 26,
        signalperiod: int = 9,
    ) -> TechnicalIndicatorResponse:
        """
        Get Moving Average Convergence Divergence (MACD) indicator.

        Args:
            symbol: Stock ticker symbol
            interval: Time interval
            series_type: Price type ('close', 'open', 'high', 'low')
            fastperiod: Fast EMA period
            slowperiod: Slow EMA period
            signalperiod: Signal line period

        Returns:
            TechnicalIndicatorResponse: MACD values with metadata

        Example:
            >>> macd = client.get_macd("AAPL")
            >>> for timestamp, values in list(macd.technical_analysis.items())[:5]:
            ...     print(f"{timestamp}: MACD = {values['MACD']}, "
            ...           f"Signal = {values['MACD_Signal']}")
        """
        data, _ = self._ti.get_macd(
            symbol=symbol,
            interval=interval.value,
            series_type=series_type,
            fastperiod=fastperiod,
            slowperiod=slowperiod,
            signalperiod=signalperiod,
        )
        return TechnicalIndicatorResponse.model_validate(data)

    def get_bbands(
        self,
        symbol: str,
        interval: Interval = Interval.MIN_5,
        time_period: int = 20,
        series_type: str = "close",
        nbdevup: int = 2,
        nbdevdn: int = 2,
    ) -> TechnicalIndicatorResponse:
        """
        Get Bollinger Bands (BBANDS) technical indicator.

        Args:
            symbol: Stock ticker symbol
            interval: Time interval
            time_period: Number of data points for calculation
            series_type: Price type ('close', 'open', 'high', 'low')
            nbdevup: Standard deviations for upper band
            nbdevdn: Standard deviations for lower band

        Returns:
            TechnicalIndicatorResponse: Bollinger Bands values

        Example:
            >>> bbands = client.get_bbands("AAPL")
            >>> for timestamp, values in list(bbands.technical_analysis.items())[:5]:
            ...     print(f"{timestamp}: Upper={values['Real Upper Band']}, "
            ...           f"Middle={values['Real Middle Band']}, "
            ...           f"Lower={values['Real Lower Band']}")
        """
        data, _ = self._ti.get_bbands(
            symbol=symbol,
            interval=interval.value,
            time_period=time_period,
            series_type=series_type,
            nbdevup=nbdevup,
            nbdevdn=nbdevdn,
        )
        return TechnicalIndicatorResponse.model_validate(data)
