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

    def _reconstruct_time_series_dict(self, data_tuple):
        """Reconstructs the dictionary for time series models from the library's tuple response."""
        data, meta_data = data_tuple
        # The key is the only other key in the dict besides "Meta Data"
        # This is brittle, but it's how the alpha-vantage library works.
        # A better implementation would be to not use this library and call the API directly.
        key_name = [k for k in data.keys() if k != 'Meta Data'][0]
        return {"Meta Data": meta_data, key_name: data[key_name]}

    # ==================== Time Series Methods ====================

    def get_intraday(
        self,
        symbol: str,
        interval: Interval = Interval.MIN_5,
        outputsize: OutputSize = OutputSize.COMPACT,
    ) -> IntradayTimeSeries:
        data, meta_data = self._ts.get_intraday(
            symbol=symbol,
            interval=interval.value,
            outputsize=outputsize.value,
        )
        return IntradayTimeSeries.model_validate(self._reconstruct_time_series_dict((data, meta_data)))

    def get_daily(
        self,
        symbol: str,
        outputsize: OutputSize = OutputSize.COMPACT,
    ) -> DailyTimeSeries:
        data, meta_data = self._ts.get_daily(symbol=symbol, outputsize=outputsize.value)
        return DailyTimeSeries.model_validate(self._reconstruct_time_series_dict((data, meta_data)))

    def get_daily_adjusted(
        self,
        symbol: str,
        outputsize: OutputSize = OutputSize.COMPACT,
    ) -> DailyAdjustedTimeSeries:
        data, meta_data = self._ts.get_daily_adjusted(symbol=symbol, outputsize=outputsize.value)
        return DailyAdjustedTimeSeries.model_validate(self._reconstruct_time_series_dict((data, meta_data)))

    def get_weekly(self, symbol: str) -> WeeklyTimeSeries:
        data, meta_data = self._ts.get_weekly(symbol=symbol)
        return WeeklyTimeSeries.model_validate(self._reconstruct_time_series_dict((data, meta_data)))

    def get_monthly(self, symbol: str) -> MonthlyTimeSeries:
        data, meta_data = self._ts.get_monthly(symbol=symbol)
        return MonthlyTimeSeries.model_validate(self._reconstruct_time_series_dict((data, meta_data)))

    def get_quote(self, symbol: str) -> QuoteResponse:
        data, _ = self._ts.get_quote_endpoint(symbol=symbol)
        return QuoteResponse.model_validate({"Global Quote": data})

    def search_symbols(self, keywords: str) -> SymbolSearchResponse:
        data, _ = self._ts.get_symbol_search(keywords=keywords)
        return SymbolSearchResponse.model_validate(data)

    # ==================== Fundamental Data Methods ====================

    def get_company_overview(self, symbol: str) -> CompanyOverview:
        data, _ = self._fd.get_company_overview(symbol=symbol)
        return CompanyOverview.model_validate(data)

    def get_earnings(self, symbol: str) -> Earnings:
        data, _ = self._fd.get_earnings(symbol=symbol)
        return Earnings.model_validate(data)

    # ==================== Forex Methods ====================

    def get_currency_exchange_rate(
        self,
        from_currency: str,
        to_currency: str,
    ) -> ExchangeRateResponse:
        data, _ = self._fx.get_currency_exchange_rate(
            from_currency=from_currency,
            to_currency=to_currency,
        )
        return ExchangeRateResponse.model_validate({"Realtime Currency Exchange Rate": data})

    def get_forex_intraday(
        self,
        from_symbol: str,
        to_symbol: str,
        interval: Interval = Interval.MIN_5,
        outputsize: OutputSize = OutputSize.COMPACT,
    ) -> ForexTimeSeries:
        data, meta_data = self._fx.get_currency_exchange_intraday(
            from_symbol=from_symbol,
            to_symbol=to_symbol,
            interval=interval.value,
            outputsize=outputsize.value,
        )
        return ForexTimeSeries.model_validate(self._reconstruct_time_series_dict((data, meta_data)))

    # ==================== Crypto Methods ====================

    def get_crypto_intraday(
        self,
        symbol: str,
        market: str = "USD",
        interval: Interval = Interval.MIN_5,
    ) -> CryptoTimeSeries:
        data, meta_data = self._crypto.get_digital_currency_intraday(
            symbol=symbol,
            market=market,
            interval=interval.value,
        )
        return CryptoTimeSeries.model_validate(self._reconstruct_time_series_dict((data, meta_data)))

    def get_crypto_daily(
        self,
        symbol: str,
        market: str = "USD",
    ) -> CryptoTimeSeries:
        data, meta_data = self._crypto.get_digital_currency_daily(
            symbol=symbol,
            market=market,
        )
        return CryptoTimeSeries.model_validate(self._reconstruct_time_series_dict((data, meta_data)))

    # ==================== Technical Indicators Methods ====================

    def get_sma(
        self,
        symbol: str,
        interval: Interval = Interval.MIN_5,
        time_period: int = 20,
        series_type: str = "close",
    ) -> TechnicalIndicatorResponse:
        data, meta_data = self._ti.get_sma(
            symbol=symbol,
            interval=interval.value,
            time_period=time_period,
            series_type=series_type,
        )
        return TechnicalIndicatorResponse.model_validate(self._reconstruct_time_series_dict((data, meta_data)))

    def get_ema(
        self,
        symbol: str,
        interval: Interval = Interval.MIN_5,
        time_period: int = 20,
        series_type: str = "close",
    ) -> TechnicalIndicatorResponse:
        data, meta_data = self._ti.get_ema(
            symbol=symbol,
            interval=interval.value,
            time_period=time_period,
            series_type=series_type,
        )
        return TechnicalIndicatorResponse.model_validate(self._reconstruct_time_series_dict((data, meta_data)))

    def get_rsi(
        self,
        symbol: str,
        interval: Interval = Interval.MIN_5,
        time_period: int = 14,
        series_type: str = "close",
    ) -> TechnicalIndicatorResponse:
        data, meta_data = self._ti.get_rsi(
            symbol=symbol,
            interval=interval.value,
            time_period=time_period,
            series_type=series_type,
        )
        return TechnicalIndicatorResponse.model_validate(self._reconstruct_time_series_dict((data, meta_data)))

    def get_macd(
        self,
        symbol: str,
        interval: Interval = Interval.MIN_5,
        series_type: str = "close",
        fastperiod: int = 12,
        slowperiod: int = 26,
        signalperiod: int = 9,
    ) -> TechnicalIndicatorResponse:
        data, meta_data = self._ti.get_macd(
            symbol=symbol,
            interval=interval.value,
            series_type=series_type,
            fastperiod=fastperiod,
            slowperiod=slowperiod,
            signalperiod=signalperiod,
        )
        return TechnicalIndicatorResponse.model_validate(self._reconstruct_time_series_dict((data, meta_data)))

    def get_bbands(
        self,
        symbol: str,
        interval: Interval = Interval.MIN_5,
        time_period: int = 20,
        series_type: str = "close",
        nbdevup: int = 2,
        nbdevdn: int = 2,
    ) -> TechnicalIndicatorResponse:
        data, meta_data = self._ti.get_bbands(
            symbol=symbol,
            interval=interval.value,
            time_period=time_period,
            series_type=series_type,
            nbdevup=nbdevup,
            nbdevdn=nbdevdn,
        )
        return TechnicalIndicatorResponse.model_validate(self._reconstruct_time_series_dict((data, meta_data)))