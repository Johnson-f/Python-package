import requests
from typing import List, Dict, Optional

from .models import (
    MarketHours,
    DetailedQuote,
    SimpleQuote,
    SimilarStock,
    HistoricalDataPoint,
    MarketMover,
    StockNews,
    SymbolSearchResult,
    SectorPerformance,
    FinancialStatement,
    StatementType,
    Frequency,
    HoldersData,
    HolderType,
    EarningsTranscript,
    TechnicalIndicator,
    MarketIndex,
)


class FinanceQueryClient:
    def __init__(self):
        self.base_url = "https://finance-query.onrender.com"

    def _make_request(self, endpoint: str, params: dict = None):
        """Helper function to make requests to the API."""
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            # Handle connection errors, timeouts, etc.
            raise ConnectionError(f"API request failed: {e}") from e

    def get_market_hours(self) -> MarketHours:
        """Get the current market status."""
        data = self._make_request("hours")
        return MarketHours.model_validate(data)

    def get_detailed_quotes(self, symbols: List[str]) -> List[DetailedQuote]:
        """Get detailed quotes for a list of symbols."""
        data = self._make_request("v1/quotes", params={"symbols": ",".join(symbols)})
        return [DetailedQuote.model_validate(item) for item in data]

    def get_simple_quotes(self, symbols: List[str]) -> List[SimpleQuote]:
        """Get simple quotes for a list of symbols."""
        data = self._make_request("v1/simple-quotes", params={"symbols": ",".join(symbols)})
        return [SimpleQuote.model_validate(item) for item in data]

    def get_similar_stocks(self, symbol: str, limit: int = 20) -> List[SimilarStock]:
        """Get similar stocks for a given symbol."""
        params = {"symbol": symbol, "limit": limit}
        data = self._make_request("v1/similar", params=params)
        return [SimilarStock.model_validate(item) for item in data]

    def get_historical_data(
        self, symbol: str, range: str, interval: str
    ) -> Dict[str, HistoricalDataPoint]:
        """Get historical data for a stock."""
        params = {"symbol": symbol, "range": range, "interval": interval}
        data = self._make_request("v1/historical", params=params)
        return {k: HistoricalDataPoint.model_validate(v) for k, v in data.items()}

    def get_market_movers(self, mover_type: str = "actives", limit: int = 25) -> List[MarketMover]:
        """
        Get market movers (actives, gainers, or losers).
        
        Args:
            mover_type: Type of movers ('actives', 'gainers', 'losers')
            limit: Number of results to return
        """
        params = {"type": mover_type, "limit": limit}
        data = self._make_request("v1/movers", params=params)
        return [MarketMover.model_validate(item) for item in data]

    def get_actives(self, limit: int = 25) -> List[MarketMover]:
        """Get the most active stocks."""
        return self.get_market_movers("actives", limit)

    def get_gainers(self, limit: int = 25) -> List[MarketMover]:
        """Get the top gaining stocks."""
        return self.get_market_movers("gainers", limit)

    def get_losers(self, limit: int = 25) -> List[MarketMover]:
        """Get the top losing stocks."""
        return self.get_market_movers("losers", limit)

    def get_stock_news(self, symbol: str) -> List[StockNews]:
        """Get news for a specific stock."""
        data = self._make_request("v1/news", params={"symbol": symbol})
        return [StockNews.model_validate(item) for item in data]

    def search_symbols(self, query: str) -> List[SymbolSearchResult]:
        """Search for stock symbols."""
        params = {"query": query, "hits": 2, "yahoo": "true"}
        data = self._make_request("v1/search", params=params)
        return [SymbolSearchResult.model_validate(item) for item in data]

    def get_all_sector_performance(self) -> List[SectorPerformance]:
        """Get performance data for all sectors."""
        data = self._make_request("v1/sectors")
        return [SectorPerformance.model_validate(item) for item in data]

    def get_sector_performance(self, symbol: str) -> SectorPerformance:
        """Get the performance of a specific stock's sector."""
        data = self._make_request(f"v1/sectors/symbol/{symbol}")
        return SectorPerformance.model_validate(data)

    # Financial Statements
    def get_financials(
        self,
        symbol: str,
        statement: StatementType = StatementType.INCOME,
        frequency: Frequency = Frequency.ANNUAL
    ) -> FinancialStatement:
        """
        Get financial statements for a given symbol.
        
        Args:
            symbol: Stock symbol
            statement: Type of financial statement
            frequency: Annual or quarterly data
        """
        params = {"statement": statement.value, "frequency": frequency.value}
        data = self._make_request(f"v1/financials/{symbol}", params=params)
        return FinancialStatement.model_validate(data)

    def get_income_statement(
        self, symbol: str, frequency: Frequency = Frequency.ANNUAL
    ) -> FinancialStatement:
        """Get income statement for a given symbol."""
        return self.get_financials(symbol, StatementType.INCOME, frequency)

    def get_balance_sheet(
        self, symbol: str, frequency: Frequency = Frequency.ANNUAL
    ) -> FinancialStatement:
        """Get balance sheet for a given symbol."""
        return self.get_financials(symbol, StatementType.BALANCE, frequency)

    def get_cash_flow_statement(
        self, symbol: str, frequency: Frequency = Frequency.ANNUAL
    ) -> FinancialStatement:
        """Get cash flow statement for a given symbol."""
        return self.get_financials(symbol, StatementType.CASHFLOW, frequency)

    # Holders Data
    def get_holders_data(
        self, symbol: str, holder_type: HolderType = HolderType.INSTITUTIONAL
    ) -> HoldersData:
        """
        Get holders information for a given symbol.
        
        Args:
            symbol: Stock symbol
            holder_type: Type of holders data to retrieve
        """
        params = {"holder_type": holder_type.value}
        data = self._make_request(f"v1/holders/{symbol}", params=params)
        return HoldersData.model_validate(data)

    def get_major_holders(self, symbol: str) -> HoldersData:
        """Get major holders breakdown for a given symbol."""
        return self.get_holders_data(symbol, HolderType.MAJOR)

    def get_institutional_holders(self, symbol: str) -> HoldersData:
        """Get institutional holders for a given symbol."""
        return self.get_holders_data(symbol, HolderType.INSTITUTIONAL)

    def get_mutual_fund_holders(self, symbol: str) -> HoldersData:
        """Get mutual fund holders for a given symbol."""
        return self.get_holders_data(symbol, HolderType.MUTUALFUND)

    def get_insider_transactions(self, symbol: str) -> HoldersData:
        """Get insider transactions for a given symbol."""
        return self.get_holders_data(symbol, HolderType.INSIDER_TRANSACTIONS)

    def get_insider_purchases(self, symbol: str) -> HoldersData:
        """Get insider purchases summary for a given symbol."""
        return self.get_holders_data(symbol, HolderType.INSIDER_PURCHASES)

    def get_insider_roster(self, symbol: str) -> HoldersData:
        """Get insider roster for a given symbol."""
        return self.get_holders_data(symbol, HolderType.INSIDER_ROSTER)

    # Earnings Transcripts
    def get_earnings_transcript(
        self, symbol: str, quarter: Optional[str] = None, year: Optional[int] = None
    ) -> EarningsTranscript:
        """
        Get earnings call transcripts for a given symbol.
        
        Args:
            symbol: Stock symbol
            quarter: Specific quarter (Q1, Q2, Q3, Q4)
            year: Specific year
        """
        params = {}
        if quarter:
            params["quarter"] = quarter
        if year:
            params["year"] = year
        
        data = self._make_request(f"v1/earnings-transcript/{symbol}", params=params)
        return EarningsTranscript.model_validate(data)

    # Technical Indicators
    def get_technical_indicator(
        self,
        symbol: str,
        indicator: str,
        range_period: str = "1y",
        interval: str = "1d",
        **kwargs
    ) -> TechnicalIndicator:
        """
        Get a single technical indicator for a given symbol.
        
        Args:
            symbol: Stock symbol
            indicator: Type of technical indicator (sma, ema, rsi, macd, etc.)
            range_period: Time range for data
            interval: Data interval
            **kwargs: Additional parameters for the specific indicator
        """
        params = {
            "symbol": symbol,
            "indicator": indicator,
            "range": range_period,
            "interval": interval,
            **kwargs
        }
        data = self._make_request("v1/indicator", params=params)
        return TechnicalIndicator.model_validate(data)

    def get_multiple_technical_indicators(
        self,
        symbol: str,
        indicators: List[str],
        range_period: str = "1y",
        interval: str = "1d"
    ) -> List[TechnicalIndicator]:
        """
        Get multiple technical indicators for a given symbol.
        
        Args:
            symbol: Stock symbol
            indicators: List of technical indicators
            range_period: Time range for data
            interval: Data interval
        """
        params = {
            "symbol": symbol,
            "indicators": ",".join(indicators),
            "range": range_period,
            "interval": interval
        }
        data = self._make_request("v1/indicators", params=params)
        return [TechnicalIndicator.model_validate(item) for item in data]

    # Market Indices
    def get_market_indices(self) -> List[MarketIndex]:
        """Get performance data for major market indices."""
        data = self._make_request("v1/indices")
        return [MarketIndex.model_validate(item) for item in data]

    # Health Check
    def health_check(self) -> Dict[str, str]:
        """Check API health status."""
        return self._make_request("health")

    def ping(self) -> Dict[str, str]:
        """Ping the API."""
        return self._make_request("ping")
