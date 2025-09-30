"""
yfinance API Client wrapper.

This module provides a Python wrapper around the yfinance library,
returning Pydantic models for type safety.
"""

import yfinance as yf
from typing import List

from .models import TickerInfo

class YFinanceClient:
    """
    Client for fetching financial data from Yahoo Finance via the yfinance library.
    """

    def get_ticker_info(self, symbol: str) -> TickerInfo:
        """
        Get comprehensive profile information for a given stock ticker.

        Args:
            symbol: The stock ticker symbol (e.g., 'AAPL', 'MSFT').

        Returns:
            TickerInfo: A Pydantic model containing the ticker information.
        """
        ticker = yf.Ticker(symbol)
        info_dict = ticker.info
        return TickerInfo.model_validate(info_dict)

    def get_multiple_ticker_info(self, symbols: List[str]) -> List[TickerInfo]:
        """
        Get comprehensive profile information for a list of stock tickers.

        Args:
            symbols: A list of stock ticker symbols (e.g., ['AAPL', 'MSFT']).

        Returns:
            A list of Pydantic models containing the ticker information for each symbol.
        """
        infos = []
        for symbol in symbols:
            infos.append(self.get_ticker_info(symbol))
        return infos
