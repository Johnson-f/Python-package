import requests
from typing import List, Dict

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

    def get_actives(self, limit: int = 25) -> List[MarketMover]:
        """Get the most active stocks."""
        params = {"limit": limit}
        data = self._make_request("v1/actives", params=params)
        return [MarketMover.model_validate(item) for item in data]

    def get_gainers(self, limit: int = 25) -> List[MarketMover]:
        """Get the top gaining stocks."""
        params = {"limit": limit}
        data = self._make_request("v1/gainers", params=params)
        return [MarketMover.model_validate(item) for item in data]

    def get_losers(self, limit: int = 25) -> List[MarketMover]:
        """Get the top losing stocks."""
        params = {"limit": limit}
        data = self._make_request("v1/losers", params=params)
        return [MarketMover.model_validate(item) for item in data]

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
