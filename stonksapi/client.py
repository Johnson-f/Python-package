"""
Unified client for the stonksapi package.
"""

from typing import Optional, List, Literal, Dict, Any
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

    # ==================== YFinance Provider Methods ====================
    
    def get_yf_ticker_info(self, symbol: str) -> models.TickerInfo:
        """Get comprehensive ticker information from YFinance."""
        return self.yfinance.get_ticker_info(symbol)

    def get_yf_fast_info(self, symbol: str) -> models.FastInfo:
        """Get fast info (key metrics) from YFinance."""
        return self.yfinance.get_fast_info(symbol)

    def get_yf_history(self, symbol: str, **kwargs) -> List[models.HistoricalData]:
        """Get historical market data from YFinance."""
        return self.yfinance.get_history(symbol, **kwargs)

    def get_yf_dividends(self, symbol: str) -> List[models.Dividend]:
        """Get dividend history from YFinance."""
        return self.yfinance.get_dividends(symbol)

    def get_yf_splits(self, symbol: str) -> List[models.Split]:
        """Get stock split history from YFinance."""
        return self.yfinance.get_splits(symbol)

    def get_yf_actions(self, symbol: str) -> List[models.Action]:
        """Get all corporate actions (dividends + splits) from YFinance."""
        return self.yfinance.get_actions(symbol)

    def get_yf_capital_gains(self, symbol: str) -> List[models.CapitalGain]:
        """Get capital gains distributions from YFinance."""
        return self.yfinance.get_capital_gains(symbol)

    # Financial Statements - YFinance
    def get_yf_income_statement(self, symbol: str, quarterly: bool = False) -> models.FinancialStatement:
        """Get income statement from YFinance."""
        return self.yfinance.get_income_statement(symbol, quarterly)

    def get_yf_balance_sheet(self, symbol: str, quarterly: bool = False) -> models.FinancialStatement:
        """Get balance sheet from YFinance."""
        return self.yfinance.get_balance_sheet(symbol, quarterly)

    def get_yf_cash_flow(self, symbol: str, quarterly: bool = False) -> models.FinancialStatement:
        """Get cash flow statement from YFinance."""
        return self.yfinance.get_cash_flow(symbol, quarterly)

    # Earnings and Estimates - YFinance
    def get_yf_earnings(self, symbol: str) -> List[models.EarningsData]:
        """Get earnings data from YFinance."""
        return self.yfinance.get_earnings(symbol)

    def get_yf_calendar(self, symbol: str) -> List[models.EarningsCalendar]:
        """Get earnings calendar from YFinance."""
        return self.yfinance.get_calendar(symbol)

    def get_yf_earnings_dates(self, symbol: str) -> List[models.EarningsCalendar]:
        """Get earnings dates from YFinance."""
        return self.yfinance.get_earnings_dates(symbol)

    def get_yf_earnings_estimate(self, symbol: str) -> List[models.EarningsEstimate]:
        """Get earnings estimates from YFinance."""
        return self.yfinance.get_earnings_estimate(symbol)

    def get_yf_revenue_estimate(self, symbol: str) -> List[models.RevenueEstimate]:
        """Get revenue estimates from YFinance."""
        return self.yfinance.get_revenue_estimate(symbol)

    # Analyst Coverage - YFinance
    def get_yf_recommendations(self, symbol: str) -> List[models.Recommendation]:
        """Get analyst recommendations from YFinance."""
        return self.yfinance.get_recommendations(symbol)

    def get_yf_recommendations_summary(self, symbol: str) -> List[models.RecommendationSummary]:
        """Get recommendations summary from YFinance."""
        return self.yfinance.get_recommendations_summary(symbol)

    def get_yf_upgrades_downgrades(self, symbol: str) -> List[models.UpgradeDowngrade]:
        """Get analyst upgrades/downgrades from YFinance."""
        return self.yfinance.get_upgrades_downgrades(symbol)

    def get_yf_analyst_price_targets(self, symbol: str) -> models.AnalystPriceTarget:
        """Get analyst price targets from YFinance."""
        return self.yfinance.get_analyst_price_targets(symbol)

    def get_yf_eps_trend(self, symbol: str) -> List[models.EPSTrend]:
        """Get EPS trends from YFinance."""
        return self.yfinance.get_eps_trend(symbol)

    def get_yf_eps_revisions(self, symbol: str) -> List[models.EPSRevisions]:
        """Get EPS revisions from YFinance."""
        return self.yfinance.get_eps_revisions(symbol)

    def get_yf_growth_estimates(self, symbol: str) -> List[models.GrowthEstimates]:
        """Get growth estimates from YFinance."""
        return self.yfinance.get_growth_estimates(symbol)

    # Ownership and Holdings - YFinance
    def get_yf_major_holders(self, symbol: str) -> models.MajorHolder:
        """Get major holders from YFinance."""
        return self.yfinance.get_major_holders(symbol)

    def get_yf_institutional_holders(self, symbol: str) -> List[models.InstitutionalHolder]:
        """Get institutional holders from YFinance."""
        return self.yfinance.get_institutional_holders(symbol)

    def get_yf_mutualfund_holders(self, symbol: str) -> List[models.MutualFundHolder]:
        """Get mutual fund holders from YFinance."""
        return self.yfinance.get_mutualfund_holders(symbol)

    def get_yf_insider_transactions(self, symbol: str) -> List[models.InsiderTransaction]:
        """Get insider transactions from YFinance."""
        return self.yfinance.get_insider_transactions(symbol)

    def get_yf_insider_purchases(self, symbol: str) -> List[models.InsiderPurchase]:
        """Get insider purchases from YFinance."""
        return self.yfinance.get_insider_purchases(symbol)

    def get_yf_insider_roster_holders(self, symbol: str) -> List[models.InsiderRosterHolder]:
        """Get insider roster from YFinance."""
        return self.yfinance.get_insider_roster_holders(symbol)

    # ESG and News - YFinance
    def get_yf_sustainability(self, symbol: str) -> models.SustainabilityData:
        """Get sustainability/ESG data from YFinance."""
        return self.yfinance.get_sustainability(symbol)

    def get_yf_news(self, symbol: str) -> List[models.NewsArticle]:
        """Get news articles from YFinance."""
        return self.yfinance.get_news(symbol)

    def get_yf_sec_filings(self, symbol: str) -> List[models.SECFiling]:
        """Get SEC filings from YFinance."""
        return self.yfinance.get_sec_filings(symbol)

    # Additional Data - YFinance
    def get_yf_funds_data(self, symbol: str) -> models.FundData:
        """Get fund data from YFinance."""
        return self.yfinance.get_funds_data(symbol)

    def get_yf_shares_full(self, symbol: str) -> List[models.SharesOutstanding]:
        """Get shares outstanding history from YFinance."""
        return self.yfinance.get_shares_full(symbol)

    def get_yf_isin(self, symbol: str) -> str:
        """Get ISIN from YFinance."""
        return self.yfinance.get_isin(symbol)

    def get_yf_history_metadata(self, symbol: str) -> Dict[str, Any]:
        """Get history metadata from YFinance."""
        return self.yfinance.get_history_metadata(symbol)

    # ==================== Finance Query Provider Methods ====================
    
    def get_fq_market_hours(self) -> models.MarketHours:
        """Get market hours from Finance Query."""
        return self.finance_query.get_market_hours()

    def get_fq_detailed_quotes(self, symbols: List[str]) -> List[models.DetailedQuote]:
        """Get detailed quotes from Finance Query."""
        return self.finance_query.get_detailed_quotes(symbols)

    def get_fq_simple_quotes(self, symbols: List[str]) -> List[models.SimpleQuote]:
        """Get simple quotes from Finance Query."""
        return self.finance_query.get_simple_quotes(symbols)

    def get_fq_similar_stocks(self, symbol: str, limit: int = 20) -> List[models.SimilarStock]:
        """Get similar stocks from Finance Query."""
        return self.finance_query.get_similar_stocks(symbol, limit)

    def get_fq_historical_data(self, symbol: str, range: str, interval: str) -> Dict[str, models.HistoricalDataPoint]:
        """Get historical data from Finance Query."""
        return self.finance_query.get_historical_data(symbol, range, interval)

    # Market Movers - Finance Query (Enhanced)
    def get_fq_market_movers(self, mover_type: str = "actives", limit: int = 25) -> List[models.MarketMover]:
        """Get market movers from Finance Query."""
        return self.finance_query.get_market_movers(mover_type, limit)

    def get_fq_actives(self, limit: int = 25) -> List[models.MarketMover]:
        """Get most active stocks from Finance Query."""
        return self.finance_query.get_actives(limit)

    def get_fq_gainers(self, limit: int = 25) -> List[models.MarketMover]:
        """Get top gainers from Finance Query."""
        return self.finance_query.get_gainers(limit)

    def get_fq_losers(self, limit: int = 25) -> List[models.MarketMover]:
        """Get top losers from Finance Query."""
        return self.finance_query.get_losers(limit)

    # News and Search - Finance Query
    def get_fq_stock_news(self, symbol: str) -> List[models.StockNews]:
        """Get stock news from Finance Query."""
        return self.finance_query.get_stock_news(symbol)

    def get_fq_search_symbols(self, query: str) -> List[models.SymbolSearchResult]:
        """Search symbols using Finance Query."""
        return self.finance_query.search_symbols(query)

    # Sectors - Finance Query
    def get_fq_all_sector_performance(self) -> List[models.SectorPerformance]:
        """Get all sector performance from Finance Query."""
        return self.finance_query.get_all_sector_performance()

    def get_fq_sector_performance(self, symbol: str) -> models.SectorPerformance:
        """Get sector performance for a symbol from Finance Query."""
        return self.finance_query.get_sector_performance(symbol)

    # Financial Statements - Finance Query
    def get_fq_financials(self, symbol: str, statement: models.StatementType = models.StatementType.INCOME, 
                         frequency: models.Frequency = models.Frequency.ANNUAL) -> models.FinancialStatement:
        """Get financial statements from Finance Query."""
        return self.finance_query.get_financials(symbol, statement, frequency)

    def get_fq_income_statement(self, symbol: str, frequency: models.Frequency = models.Frequency.ANNUAL) -> models.FinancialStatement:
        """Get income statement from Finance Query."""
        return self.finance_query.get_income_statement(symbol, frequency)

    def get_fq_balance_sheet(self, symbol: str, frequency: models.Frequency = models.Frequency.ANNUAL) -> models.FinancialStatement:
        """Get balance sheet from Finance Query."""
        return self.finance_query.get_balance_sheet(symbol, frequency)

    def get_fq_cash_flow_statement(self, symbol: str, frequency: models.Frequency = models.Frequency.ANNUAL) -> models.FinancialStatement:
        """Get cash flow statement from Finance Query."""
        return self.finance_query.get_cash_flow_statement(symbol, frequency)

    # Holders Data - Finance Query
    def get_fq_holders_data(self, symbol: str, holder_type: models.HolderType = models.HolderType.INSTITUTIONAL) -> models.HoldersData:
        """Get holders data from Finance Query."""
        return self.finance_query.get_holders_data(symbol, holder_type)

    def get_fq_major_holders(self, symbol: str) -> models.HoldersData:
        """Get major holders from Finance Query."""
        return self.finance_query.get_major_holders(symbol)

    def get_fq_institutional_holders(self, symbol: str) -> models.HoldersData:
        """Get institutional holders from Finance Query."""
        return self.finance_query.get_institutional_holders(symbol)

    def get_fq_mutual_fund_holders(self, symbol: str) -> models.HoldersData:
        """Get mutual fund holders from Finance Query."""
        return self.finance_query.get_mutual_fund_holders(symbol)

    def get_fq_insider_transactions(self, symbol: str) -> models.HoldersData:
        """Get insider transactions from Finance Query."""
        return self.finance_query.get_insider_transactions(symbol)

    def get_fq_insider_purchases(self, symbol: str) -> models.HoldersData:
        """Get insider purchases from Finance Query."""
        return self.finance_query.get_insider_purchases(symbol)

    def get_fq_insider_roster(self, symbol: str) -> models.HoldersData:
        """Get insider roster from Finance Query."""
        return self.finance_query.get_insider_roster(symbol)

    # Earnings Transcripts - Finance Query
    def get_fq_earnings_transcript(self, symbol: str, quarter: Optional[str] = None, 
                                  year: Optional[int] = None) -> models.EarningsTranscript:
        """Get earnings transcripts from Finance Query."""
        return self.finance_query.get_earnings_transcript(symbol, quarter, year)

    # Technical Indicators - Finance Query
    def get_fq_technical_indicator(self, symbol: str, indicator: str, range_period: str = "1y", 
                                  interval: str = "1d", **kwargs) -> models.TechnicalIndicator:
        """Get technical indicator from Finance Query."""
        return self.finance_query.get_technical_indicator(symbol, indicator, range_period, interval, **kwargs)

    def get_fq_multiple_technical_indicators(self, symbol: str, indicators: List[str], 
                                           range_period: str = "1y", interval: str = "1d") -> List[models.TechnicalIndicator]:
        """Get multiple technical indicators from Finance Query."""
        return self.finance_query.get_multiple_technical_indicators(symbol, indicators, range_period, interval)

    # Market Indices - Finance Query
    def get_fq_market_indices(self) -> List[models.MarketIndex]:
        """Get market indices from Finance Query."""
        return self.finance_query.get_market_indices()

    # Health Check - Finance Query
    def get_fq_health_check(self) -> Dict[str, str]:
        """Check Finance Query API health."""
        return self.finance_query.health_check()

    def get_fq_ping(self) -> Dict[str, str]:
        """Ping Finance Query API."""
        return self.finance_query.ping()

    # ==================== Unified Smart Methods ====================
    
    def get_comprehensive_ticker_info(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive ticker information from both YFinance and Finance Query."""
        yf_info = self.get_yf_ticker_info(symbol)
        fq_quotes = self.get_fq_detailed_quotes([symbol])
        
        return {
            "yfinance_data": yf_info,
            "finance_query_quote": fq_quotes[0] if fq_quotes else None,
            "symbol": symbol
        }

    def get_unified_financials(self, symbol: str, quarterly: bool = False) -> Dict[str, Any]:
        """Get financial statements from both providers for comparison."""
        frequency = models.Frequency.QUARTERLY if quarterly else models.Frequency.ANNUAL
        
        try:
            yf_income = self.get_yf_income_statement(symbol, quarterly)
            yf_balance = self.get_yf_balance_sheet(symbol, quarterly)
            yf_cashflow = self.get_yf_cash_flow(symbol, quarterly)
            yf_data = {
                "income_statement": yf_income,
                "balance_sheet": yf_balance,
                "cash_flow": yf_cashflow
            }
        except Exception as e:
            yf_data = {"error": str(e)}
        
        try:
            fq_income = self.get_fq_income_statement(symbol, frequency)
            fq_balance = self.get_fq_balance_sheet(symbol, frequency)
            fq_cashflow = self.get_fq_cash_flow_statement(symbol, frequency)
            fq_data = {
                "income_statement": fq_income,
                "balance_sheet": fq_balance,
                "cash_flow": fq_cashflow
            }
        except Exception as e:
            fq_data = {"error": str(e)}
        
        return {
            "yfinance": yf_data,
            "finance_query": fq_data
        }

    def get_unified_holders_analysis(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive holders analysis from both providers."""
        try:
            # YFinance holders data
            yf_major = self.get_yf_major_holders(symbol)
            yf_institutional = self.get_yf_institutional_holders(symbol)
            yf_mutual = self.get_yf_mutualfund_holders(symbol)
            yf_insider_trans = self.get_yf_insider_transactions(symbol)
            yf_data = {
                "major_holders": yf_major,
                "institutional_holders": yf_institutional,
                "mutual_fund_holders": yf_mutual,
                "insider_transactions": yf_insider_trans
            }
        except Exception as e:
            yf_data = {"error": str(e)}
        
        try:
            # Finance Query holders data
            fq_major = self.get_fq_major_holders(symbol)
            fq_institutional = self.get_fq_institutional_holders(symbol)
            fq_mutual = self.get_fq_mutual_fund_holders(symbol)
            fq_insider_trans = self.get_fq_insider_transactions(symbol)
            fq_data = {
                "major_holders": fq_major,
                "institutional_holders": fq_institutional,
                "mutual_fund_holders": fq_mutual,
                "insider_transactions": fq_insider_trans
            }
        except Exception as e:
            fq_data = {"error": str(e)}
        
        return {
            "yfinance": yf_data,
            "finance_query": fq_data
        }

    def get_unified_news(self, symbol: str) -> Dict[str, Any]:
        """Get news from both YFinance and Finance Query."""
        try:
            yf_news = self.get_yf_news(symbol)
        except Exception as e:
            yf_news = {"error": str(e)}
        
        try:
            fq_news = self.get_fq_stock_news(symbol)
        except Exception as e:
            fq_news = {"error": str(e)}
        
        return {
            "yfinance_news": yf_news,
            "finance_query_news": fq_news
        }

    def get_comprehensive_analysis(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive analysis combining all available data from both providers."""
        return {
            "ticker_info": self.get_comprehensive_ticker_info(symbol),
            "financials": self.get_unified_financials(symbol),
            "holders_analysis": self.get_unified_holders_analysis(symbol),
            "news": self.get_unified_news(symbol),
            "market_data": {
                "yf_fast_info": self.get_yf_fast_info(symbol),
                "fq_detailed_quote": self.get_fq_detailed_quotes([symbol])[0] if self.get_fq_detailed_quotes([symbol]) else None
            }
        }