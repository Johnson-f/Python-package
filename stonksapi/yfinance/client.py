"""
yfinance API Client wrapper.

This module provides a Python wrapper around the yfinance library,
returning Pydantic models for type safety.
"""

import yfinance as yf
from typing import List
from datetime import date
import pandas as pd

from .models import (
    TickerInfo,
    HistoricalData,
    Dividend,
    Split,
    FinancialStatement,
    FinancialReport,
)


class YFinanceClient:
    """
    Client for fetching financial data from Yahoo Finance via the yfinance library.
    """

    def _dataframe_to_financial_statement(
        self, df: pd.DataFrame
    ) -> FinancialStatement:
        """Converts a yfinance financial statement DataFrame to a Pydantic model."""
        reports = []
        for report_date in df.columns:
            metrics = df[report_date].to_dict()
            report = FinancialReport(date=report_date.date(), metrics=metrics)
            reports.append(report)
        return FinancialStatement(reports=reports)

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

    def get_history(self, symbol: str, **kwargs) -> List[HistoricalData]:
        """
        Get historical market data for a given ticker.

        Args:
            symbol: The stock ticker symbol.
            **kwargs: Additional arguments to pass to yf.Ticker().history().
                      Examples: period="1mo", interval="1d".

        Returns:
            A list of Pydantic models containing the historical data.
        """
        ticker = yf.Ticker(symbol)
        hist_df = ticker.history(**kwargs)
        hist_df = hist_df.reset_index()  # Convert index (Date) to a column
        hist_df["Date"] = hist_df["Date"].dt.date  # Convert datetime to date
        return [
            HistoricalData.model_validate(row.to_dict())
            for _, row in hist_df.iterrows()
        ]

    def get_dividends(self, symbol: str) -> List[Dividend]:
        """
        Get dividend history for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of Pydantic models containing dividend data.
        """
        ticker = yf.Ticker(symbol)
        dividends_series = ticker.dividends
        dividends_df = dividends_series.reset_index()
        dividends_df.columns = ["date", "dividend"]
        dividends_df["date"] = dividends_df["date"].dt.date
        return [
            Dividend.model_validate(row.to_dict()) for _, row in dividends_df.iterrows()
        ]

    def get_splits(self, symbol: str) -> List[Split]:
        """
        Get stock split history for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of Pydantic models containing stock split data.
        """
        ticker = yf.Ticker(symbol)
        splits_series = ticker.splits
        splits_df = splits_series.reset_index()
        splits_df.columns = ["date", "stock_splits"]
        splits_df["date"] = splits_df["date"].dt.date
        return [Split.model_validate(row.to_dict()) for _, row in splits_df.iterrows()]

    def get_income_statement(
        self, symbol: str, quarterly: bool = False
    ) -> FinancialStatement:
        """
        Get the income statement for a given ticker.

        Args:
            symbol: The stock ticker symbol.
            quarterly: If True, returns quarterly data, otherwise annual.

        Returns:
            A Pydantic model containing the income statement.
        """
        ticker = yf.Ticker(symbol)
        income_df = ticker.quarterly_financials if quarterly else ticker.financials
        return self._dataframe_to_financial_statement(income_df)

    def get_balance_sheet(
        self, symbol: str, quarterly: bool = False
    ) -> FinancialStatement:
        """
        Get the balance sheet for a given ticker.

        Args:
            symbol: The stock ticker symbol.
            quarterly: If True, returns quarterly data, otherwise annual.

        Returns:
            A Pydantic model containing the balance sheet.
        """
        ticker = yf.Ticker(symbol)
        balance_df = (
            ticker.quarterly_balance_sheet if quarterly else ticker.balance_sheet
        )
        return self._dataframe_to_financial_statement(balance_df)

    def get_cash_flow(self, symbol: str, quarterly: bool = False) -> FinancialStatement:
        """
        Get the cash flow statement for a given ticker.

        Args:
            symbol: The stock ticker symbol.
            quarterly: If True, returns quarterly data, otherwise annual.

        Returns:
            A Pydantic model containing the cash flow statement.
        """
        ticker = yf.Ticker(symbol)
        cashflow_df = ticker.quarterly_cashflow if quarterly else ticker.cashflow
        return self._dataframe_to_financial_statement(cashflow_df)
