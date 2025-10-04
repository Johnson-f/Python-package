"""
Unified client for the stonksapi package.
"""

from typing import Optional, List, Literal
from datetime import date, timedelta

from .alpha_vantage.client import AlphaVantageClient, OutputSize as AlphaVantageOutputSize
from .finance_query.client import FinanceQueryClient
from .finnhub.client import FinnhubClient
from .polygon.client import PolygonClient
from .yfinance.client import YFinanceClient
from . import models


class StonksApiClient:
    """
    A unified client for accessing financial data from multiple providers.
    """

    def __init__(
        self,
        alpha_vantage_api_key: Optional[str] = None,
        finnhub_api_key: Optional[str] = None,
        polygon_api_key: Optional[str] = None,
    ):
        """
        Initializes the StonksApiClient.

        Args:
            alpha_vantage_api_key: API key for Alpha Vantage.
            finnhub_api_key: API key for Finnhub.
            polygon_api_key: API key for Polygon.
        """
        self.alpha_vantage = AlphaVantageClient(api_key=alpha_vantage_api_key)
        self.finance_query = FinanceQueryClient()
        self.finnhub = FinnhubClient(api_key=finnhub_api_key)
        self.polygon = PolygonClient(api_key=polygon_api_key)
        self.yfinance = YFinanceClient()

        self.is_alpha_vantage_available = bool(self.alpha_vantage.api_key)
        self.is_finnhub_available = bool(self.finnhub.api_key)
        self.is_polygon_available = bool(self.polygon.api_key)

    def get_ticker_info(
        self, ticker: str, source: Optional[Literal["yfinance", "alpha_vantage", "finnhub", "polygon"]] = None
    ) -> models.TickerInfo:
        """
        Get ticker information from the specified source.
        If no source is provided, it defaults to yfinance.

        Args:
            ticker: The stock ticker symbol.
            source: The data source to use.

        Returns:
            A unified TickerInfo model.
        """
        source = source or "yfinance"

        if source == "yfinance":
            info = self.yfinance.get_ticker_info(ticker)
            return models.TickerInfo(**info.model_dump(), source="yfinance")
        elif source == "alpha_vantage":
            if not self.is_alpha_vantage_available:
                raise ValueError("Alpha Vantage API key not provided.")
            overview = self.alpha_vantage.get_company_overview(ticker)
            return models.TickerInfo(
                symbol=overview.symbol,
                name=overview.name,
                description=overview.description,
                country=overview.country,
                currency=overview.currency,
                exchange=overview.exchange,
                sector=overview.sector,
                industry=overview.industry,
                market_cap=int(overview.market_capitalization) if overview.market_capitalization else None,
                pe_ratio=float(overview.pe_ratio) if overview.pe_ratio else None,
                eps=float(overview.eps) if overview.eps else None,
                dividend_yield=float(overview.dividend_yield) if overview.dividend_yield else None,
                source="alpha_vantage",
            )
        elif source == "finnhub":
            if not self.is_finnhub_available:
                raise ValueError("Finnhub API key not provided.")
            profile = self.finnhub.get_company_profile(ticker)
            return models.TickerInfo(
                symbol=profile.ticker,
                name=profile.name,
                country=profile.country,
                currency=profile.currency,
                exchange=profile.exchange,
                finnhub_industry=profile.finnhub_industry,
                market_capitalization=profile.market_capitalization,
                shares_outstanding=profile.share_outstanding,
                website=profile.weburl,
                source="finnhub",
            )
        elif source == "polygon":
            if not self.is_polygon_available:
                raise ValueError("Polygon API key not provided.")
            details = self.polygon.get_ticker_details(ticker)
            return models.TickerInfo(
                symbol=details.ticker,
                name=details.name,
                market=details.market,
                locale=details.locale,
                primary_exchange=details.primary_exchange,
                type=details.type,
                active=details.active,
                currency_name=details.currency_name,
                cik=details.cik,
                source="polygon",
            )

    def get_quote(
        self, ticker: str, source: Optional[Literal["finnhub", "alpha_vantage", "polygon", "finance_query"]] = None
    ) -> models.Quote:
        """
        Get a quote from the specified source.
        If no source is provided, it will try to use the best available source, with fallback to free sources.

        Args:
            ticker: The stock ticker symbol.
            source: The data source to use.

        Returns:
            A unified Quote model.
        """
        if source:
            if source == "finnhub" and not self.is_finnhub_available:
                raise ValueError("Finnhub API key not provided.")
            if source == "alpha_vantage" and not self.is_alpha_vantage_available:
                raise ValueError("Alpha Vantage API key not provided.")
            if source == "polygon" and not self.is_polygon_available:
                raise ValueError("Polygon API key not provided.")
            return self._get_quote_from_source(ticker, source)

        # Automatic fallback logic
        if self.is_finnhub_available:
            return self._get_quote_from_source(ticker, "finnhub")
        if self.is_alpha_vantage_available:
            return self._get_quote_from_source(ticker, "alpha_vantage")
        if self.is_polygon_available:
            return self._get_quote_from_source(ticker, "polygon")
        
        return self._get_quote_from_source(ticker, "finance_query")

    def _get_quote_from_source(self, ticker: str, source: str) -> models.Quote:
        if source == "finnhub":
            quote = self.finnhub.get_quote(ticker)
            return models.Quote(
                symbol=ticker,
                price=quote.current_price,
                open=quote.open_price_of_the_day,
                high=quote.high_price_of_the_day,
                low=quote.low_price_of_the_day,
                previous_close=quote.previous_close_price,
                change=quote.current_price - quote.previous_close_price if quote.current_price and quote.previous_close_price else None,
                change_percent=(quote.current_price / quote.previous_close_price - 1) * 100 if quote.current_price and quote.previous_close_price else None,
                timestamp=quote.timestamp,
                source="finnhub",
            )
        elif source == "alpha_vantage":
            quote = self.alpha_vantage.get_quote(ticker).global_quote
            return models.Quote(
                symbol=quote.symbol,
                price=float(quote.price),
                open=float(quote.open),
                high=float(quote.high),
                low=float(quote.low),
                previous_close=float(quote.previous_close),
                volume=quote.volume,
                change=float(quote.change),
                change_percent=float(quote.change_percent.replace("%", "")),
                source="alpha_vantage",
            )
        elif source == "polygon":
            quote = self.polygon.get_last_quote(ticker)
            return models.Quote(
                symbol=ticker,
                price=quote.ask_price, # Or bid_price, or a midpoint
                timestamp=quote.timestamp,
                source="polygon",
            )
        elif source == "finance_query":
            quote = self.finance_query.get_simple_quotes([ticker])[0]
            return models.Quote(
                symbol=quote.symbol,
                price=float(quote.price),
                change=float(quote.change),
                change_percent=float(quote.percent_change.replace("%", "")),
                source="finance_query",
            )

    def get_historical_data(
        self, 
        ticker: str, 
        range: str = "1y",
        interval: str = "1d",
    ) -> List[models.HistoricalData]:
        """
        Get historical data from Finance Query.

        Args:
            ticker: The stock ticker symbol.
            range: The data range (e.g., "1d", "5d", "1mo", "1y", "max").
            interval: The data interval (e.g., "1m", "1h", "1d").

        Returns:
            A list of unified HistoricalData models.
        """
        history = self.finance_query.get_historical_data(ticker, range=range, interval=interval)
        return [
            models.HistoricalData(
                date=date.fromisoformat(dt.split(' ')[0]),
                open=d.open,
                high=d.high,
                low=d.low,
                close=d.close,
                volume=d.volume,
                source="finance_query",
            )
            for dt, d in history.items()
        ]
      
    # Finance query provider 
    def get_market_movers(
        self, category: Literal["actives", "gainers", "losers"] = "actives"
    ) -> List[models.MarketMover]:
        """
        Get market movers from Finance Query.

        Args:
            category: The category of market movers to fetch.

        Returns:
            A list of MarketMover models.
        """
        if category == "actives":
            movers = self.finance_query.get_actives()
            return [models.MarketMover(**m.model_dump()) for m in movers]
        elif category == "gainers":
            movers = self.finance_query.get_gainers()
            return [models.MarketMover(**m.model_dump()) for m in movers]
        elif category == "losers":
            movers = self.finance_query.get_losers()
            return [models.MarketMover(**m.model_dump()) for m in movers]

    def get_market_news(
        self, 
        ticker: Optional[str] = None, 
        source: Optional[Literal["finnhub", "polygon", "finance_query"]] = None
    ) -> List[models.NewsArticle]:
        """
        Get market news from the specified source.
        If no source is provided, it will try to use the best available source.

        Args:
            ticker: The stock ticker symbol to get news for.
            source: The data source to use.

        Returns:
            A list of unified NewsArticle models.
        """
        if source:
            if source == "finnhub" and not self.is_finnhub_available:
                raise ValueError("Finnhub API key not provided.")
            if source == "polygon" and not self.is_polygon_available:
                raise ValueError("Polygon API key not provided.")
            return self._get_market_news_from_source(ticker, source)

        # Automatic fallback logic
        if self.is_finnhub_available:
            return self._get_market_news_from_source(ticker, "finnhub")
        if self.is_polygon_available:
            return self._get_market_news_from_source(ticker, "polygon")
        
        return self._get_market_news_from_source(ticker, "finance_query")

    def _get_market_news_from_source(self, ticker: Optional[str], source: str) -> List[models.NewsArticle]:
        if source == "finnhub":
            news_list = self.finnhub.get_market_news("general")
            return [
                models.NewsArticle(
                    id=str(n.id),
                    title=n.headline,
                    published_utc=str(n.datetime),
                    article_url=n.url,
                    provider="finnhub",
                    publisher=n.source,
                    summary=n.summary,
                    image_url=n.image or None,
                )
                for n in news_list
            ]
        elif source == "polygon":
            news_list = self.polygon.get_market_news(limit=50)
            return [
                models.NewsArticle(
                    id=n.id,
                    title=n.title,
                    author=n.author,
                    published_utc=n.published_utc,
                    article_url=n.article_url,
                    tickers=n.tickers,
                    provider="polygon",
                    publisher=n.publisher.name,
                    summary=n.description,
                    image_url=n.image_url,
                )
                for n in news_list
            ]
        elif source == "finance_query":
            if not ticker:
                raise ValueError("Ticker must be provided for finance_query news source.")
            news_list = self.finance_query.get_stock_news(ticker)
            return [
                models.NewsArticle(
                    title=n.title,
                    article_url=n.link,
                    provider="finance_query",
                    publisher=n.source,
                    image_url=n.img,
                    published_utc=n.time,
                )
                for n in news_list
            ]