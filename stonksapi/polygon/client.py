import os
from polygon import RESTClient
from typing import Optional, List

from .models import (
    TickerDetails,
    Aggregate,
    DailyOpenClose,
    LastQuote,
    NewsArticle,
    IndicatorValue,
    MACDValue,
    OptionContract,
    LastQuoteForOption,
    StockFinancial,
)


class PolygonClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("POLYGON_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either as an argument or as a POLYGON_API_KEY environment variable."
            )
        self._client = RESTClient(self.api_key)

    def get_ticker_details(self, ticker: str) -> TickerDetails:
        """
        Get details for a single ticker.
        https://polygon.io/docs/stocks/get_v3_reference_tickers__ticker
        """
        response = self._client.get_ticker_details(ticker)
        return TickerDetails.model_validate(vars(response))

    def get_aggregates(
        self, ticker: str, multiplier: int, timespan: str, from_date: str, to_date: str
    ) -> List[Aggregate]:
        """
        Get aggregate bars for a stock over a given date range.
        https://polygon.io/docs/stocks/get_v2_aggs_ticker__stocksticker__range__multiplier___timespan___from___to
        """
        aggs = self._client.get_aggs(ticker, multiplier, timespan, from_date, to_date)
        return [Aggregate.model_validate(vars(agg)) for agg in aggs]

    def get_daily_open_close(self, ticker: str, date: str) -> DailyOpenClose:
        """
        Get the daily open, close and after hours prices of a stock.
        https://polygon.io/docs/stocks/get_v1_open-close__stocksticker___date
        """
        resp = self._client.get_daily_open_close_agg(ticker, date)
        return DailyOpenClose.model_validate(vars(resp))

    def get_last_quote(self, ticker: str) -> LastQuote:
        """
        Get the last quote for a given stock.
        https://polygon.io/docs/stocks/get_v2_last_nbbo__stocksticker
        """
        resp = self._client.get_last_quote(ticker)
        return LastQuote.model_validate(vars(resp.last))

    def get_market_news(self, limit: int = 100) -> List[NewsArticle]:
        """
        Get the latest market news.
        https://polygon.io/docs/stocks/get_v2_reference_news
        """
        resp_generator = self._client.list_ticker_news(limit=limit)
        news_items = []
        for news_item in resp_generator:
            news_items.append(news_item)
        return [NewsArticle.model_validate(news) for news in news_items]

    def get_sma(
        self,
        ticker: str,
        timespan: str,
        window: int,
        timestamp: Optional[str] = None,
        timestamp_gt: Optional[str] = None,
        timestamp_gte: Optional[str] = None,
        timestamp_lt: Optional[str] = None,
        timestamp_lte: Optional[str] = None,
        series_type: str = "close",
        expand_underlying: bool = False,
    ) -> List[IndicatorValue]:
        """
        Get the simple moving average (SMA) for a stock.
        https://polygon.io/docs/stocks/get_v1_indicators_sma__stockticker
        """
        resp = self._client.get_sma(
            ticker,
            timespan=timespan,
            window=window,
            timestamp=timestamp,
            timestamp_gt=timestamp_gt,
            timestamp_gte=timestamp_gte,
            timestamp_lt=timestamp_lt,
            timestamp_lte=timestamp_lte,
            series_type=series_type,
            expand_underlying=expand_underlying,
        )
        return [IndicatorValue.model_validate(vars(val)) for val in resp.values]

    def get_ema(
        self,
        ticker: str,
        timespan: str,
        window: int,
        timestamp: Optional[str] = None,
        timestamp_gt: Optional[str] = None,
        timestamp_gte: Optional[str] = None,
        timestamp_lt: Optional[str] = None,
        timestamp_lte: Optional[str] = None,
        series_type: str = "close",
        expand_underlying: bool = False,
    ) -> List[IndicatorValue]:
        """
        Get the exponential moving average (EMA) for a stock.
        https://polygon.io/docs/stocks/get_v1_indicators_ema__stockticker
        """
        resp = self._client.get_ema(
            ticker,
            timespan=timespan,
            window=window,
            timestamp=timestamp,
            timestamp_gt=timestamp_gt,
            timestamp_gte=timestamp_gte,
            timestamp_lt=timestamp_lt,
            timestamp_lte=timestamp_lte,
            series_type=series_type,
            expand_underlying=expand_underlying,
        )
        return [IndicatorValue.model_validate(vars(val)) for val in resp.values]

    def get_macd(
        self,
        ticker: str,
        timespan: str,
        timestamp: Optional[str] = None,
        timestamp_gt: Optional[str] = None,
        timestamp_gte: Optional[str] = None,
        timestamp_lt: Optional[str] = None,
        timestamp_lte: Optional[str] = None,
        short_window: int = 12,
        long_window: int = 26,
        signal_window: int = 9,
        series_type: str = "close",
        expand_underlying: bool = False,
    ) -> List[MACDValue]:
        """
        Get the moving average convergence/divergence (MACD) for a stock.
        https://polygon.io/docs/stocks/get_v1_indicators_macd__stockticker
        """
        resp = self._client.get_macd(
            ticker,
            timespan=timespan,
            timestamp=timestamp,
            timestamp_gt=timestamp_gt,
            timestamp_gte=timestamp_gte,
            timestamp_lt=timestamp_lt,
            timestamp_lte=timestamp_lte,
            short_window=short_window,
            long_window=long_window,
            signal_window=signal_window,
            series_type=series_type,
            expand_underlying=expand_underlying,
        )
        return [MACDValue.model_validate(vars(val)) for val in resp.values]

    def get_rsi(
        self,
        ticker: str,
        timespan: str,
        window: int = 14,
        timestamp: Optional[str] = None,
        timestamp_gt: Optional[str] = None,
        timestamp_gte: Optional[str] = None,
        timestamp_lt: Optional[str] = None,
        timestamp_lte: Optional[str] = None,
        series_type: str = "close",
        expand_underlying: bool = False,
    ) -> List[IndicatorValue]:
        """
        Get the relative strength index (RSI) for a stock.
        https://polygon.io/docs/stocks/get_v1_indicators_rsi__stockticker
        """
        resp = self._client.get_rsi(
            ticker,
            timespan=timespan,
            window=window,
            timestamp=timestamp,
            timestamp_gt=timestamp_gt,
            timestamp_gte=timestamp_gte,
            timestamp_lt=timestamp_lt,
            timestamp_lte=timestamp_lte,
            series_type=series_type,
            expand_underlying=expand_underlying,
        )
        if resp and hasattr(resp, 'values'):
            return [IndicatorValue.model_validate(vars(val)) for val in resp.values]
        return []

    def list_option_contracts(
        self,
        underlying_ticker: str,
        limit: int = 1000,
        expired: Optional[bool] = None,
        expiration_date_lt: Optional[str] = None,
        expiration_date_lte: Optional[str] = None,
        expiration_date_gt: Optional[str] = None,
        expiration_date_gte: Optional[str] = None,
    ) -> List[OptionContract]:
        """
        List all option contracts for an underlying ticker.
        https://polygon.io/docs/options/get_v3_reference_options_contracts
        """
        resp = self._client.list_options_contracts(
            underlying_ticker=underlying_ticker,
            limit=limit,
            expired=expired,
            expiration_date_lt=expiration_date_lt,
            expiration_date_lte=expiration_date_lte,
            expiration_date_gt=expiration_date_gt,
            expiration_date_gte=expiration_date_gte,
        )
        return [OptionContract.model_validate(vars(c)) for c in resp]

    def get_last_quote_for_option(
        self, option_ticker: str
    ) -> LastQuoteForOption:
        """
        Get the last quote for a single option contract.
        https://polygon.io/docs/options/get_v2_last_nbbo__optionsticker
        """
        resp = self._client.get_last_quote_for_option_contract(option_ticker)
        return LastQuoteForOption.model_validate(vars(resp.last))

    def get_stock_financials(
        self, ticker: str, limit: int = 100
    ) -> List[StockFinancial]:
        """
        Get the historical financials for a stock.
        https://polygon.io/docs/stocks/get_vx_reference_financials
        """
        resp_generator = self._client.vx.list_stock_financials(ticker, limit=limit)
        financial_items = []
        for fin_item in resp_generator:
            financial_items.append(fin_item)
        return [StockFinancial.model_validate(fin) for fin in financial_items]