"""
yfinance API Client wrapper.

This module provides a Python wrapper around the yfinance library,
returning Pydantic models for type safety.
"""

import yfinance as yf
from typing import List, Dict, Any
from datetime import date
import pandas as pd

from .models import (
    TickerInfo,
    HistoricalData,
    Dividend,
    Split,
    FinancialStatement,
    FinancialReport,
    EarningsData,
    EarningsCalendar,
    EarningsEstimate,
    RevenueEstimate,
    Recommendation,
    RecommendationSummary,
    UpgradeDowngrade,
    AnalystPriceTarget,
    EPSTrend,
    EPSRevisions,
    GrowthEstimates,
    MajorHolder,
    InstitutionalHolder,
    MutualFundHolder,
    InsiderTransaction,
    InsiderPurchase,
    InsiderRosterHolder,
    SustainabilityData,
    NewsArticle,
    SECFiling,
    FundData,
    FastInfo,
    SharesOutstanding,
    CapitalGain,
    Action,
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

    def get_fast_info(self, symbol: str) -> FastInfo:
        """
        Get fast info (quick access to key metrics) for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            FastInfo: A Pydantic model containing fast info data.
        """
        ticker = yf.Ticker(symbol)
        fast_info_dict = ticker.fast_info
        return FastInfo.model_validate(fast_info_dict)

    def get_earnings(self, symbol: str) -> List[EarningsData]:
        """
        Get earnings data for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of EarningsData models containing earnings information.
        """
        ticker = yf.Ticker(symbol)
        earnings_df = ticker.earnings
        if earnings_df.empty:
            return []
        earnings_df = earnings_df.reset_index()
        earnings_df.columns = [col.lower().replace(' ', '_') for col in earnings_df.columns]
        return [
            EarningsData.model_validate(row.to_dict())
            for _, row in earnings_df.iterrows()
        ]

    def get_calendar(self, symbol: str) -> List[EarningsCalendar]:
        """
        Get earnings calendar for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of EarningsCalendar models.
        """
        ticker = yf.Ticker(symbol)
        calendar_df = ticker.calendar
        if calendar_df is None or calendar_df.empty:
            return []
        calendar_df = calendar_df.reset_index(drop=True)
        return [
            EarningsCalendar.model_validate(row.to_dict())
            for _, row in calendar_df.iterrows()
        ]

    def get_earnings_dates(self, symbol: str) -> List[EarningsCalendar]:
        """
        Get earnings dates for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of EarningsCalendar models.
        """
        ticker = yf.Ticker(symbol)
        earnings_dates_df = ticker.earnings_dates
        if earnings_dates_df is None or earnings_dates_df.empty:
            return []
        earnings_dates_df = earnings_dates_df.reset_index()
        return [
            EarningsCalendar.model_validate(row.to_dict())
            for _, row in earnings_dates_df.iterrows()
        ]

    def get_earnings_estimate(self, symbol: str) -> List[EarningsEstimate]:
        """
        Get earnings estimates for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of EarningsEstimate models.
        """
        ticker = yf.Ticker(symbol)
        earnings_estimate_df = ticker.earnings_estimate
        if earnings_estimate_df is None or earnings_estimate_df.empty:
            return []
        earnings_estimate_df = earnings_estimate_df.reset_index()
        return [
            EarningsEstimate.model_validate(row.to_dict())
            for _, row in earnings_estimate_df.iterrows()
        ]

    def get_revenue_estimate(self, symbol: str) -> List[RevenueEstimate]:
        """
        Get revenue estimates for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of RevenueEstimate models.
        """
        ticker = yf.Ticker(symbol)
        revenue_estimate_df = ticker.revenue_estimate
        if revenue_estimate_df is None or revenue_estimate_df.empty:
            return []
        revenue_estimate_df = revenue_estimate_df.reset_index()
        return [
            RevenueEstimate.model_validate(row.to_dict())
            for _, row in revenue_estimate_df.iterrows()
        ]

    def get_recommendations(self, symbol: str) -> List[Recommendation]:
        """
        Get analyst recommendations for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of Recommendation models.
        """
        ticker = yf.Ticker(symbol)
        recommendations_df = ticker.recommendations
        if recommendations_df is None or recommendations_df.empty:
            return []
        recommendations_df = recommendations_df.reset_index()
        return [
            Recommendation.model_validate(row.to_dict())
            for _, row in recommendations_df.iterrows()
        ]

    def get_recommendations_summary(self, symbol: str) -> List[RecommendationSummary]:
        """
        Get analyst recommendations summary for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of RecommendationSummary models.
        """
        ticker = yf.Ticker(symbol)
        recommendations_summary_df = ticker.recommendations_summary
        if recommendations_summary_df is None or recommendations_summary_df.empty:
            return []
        recommendations_summary_df = recommendations_summary_df.reset_index()
        return [
            RecommendationSummary.model_validate(row.to_dict())
            for _, row in recommendations_summary_df.iterrows()
        ]

    def get_upgrades_downgrades(self, symbol: str) -> List[UpgradeDowngrade]:
        """
        Get analyst upgrades and downgrades for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of UpgradeDowngrade models.
        """
        ticker = yf.Ticker(symbol)
        upgrades_downgrades_df = ticker.upgrades_downgrades
        if upgrades_downgrades_df is None or upgrades_downgrades_df.empty:
            return []
        upgrades_downgrades_df = upgrades_downgrades_df.reset_index()
        return [
            UpgradeDowngrade.model_validate(row.to_dict())
            for _, row in upgrades_downgrades_df.iterrows()
        ]

    def get_analyst_price_targets(self, symbol: str) -> AnalystPriceTarget:
        """
        Get analyst price targets for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            AnalystPriceTarget: A Pydantic model containing price target data.
        """
        ticker = yf.Ticker(symbol)
        price_targets_dict = ticker.analyst_price_targets
        return AnalystPriceTarget.model_validate(price_targets_dict)

    def get_eps_trend(self, symbol: str) -> List[EPSTrend]:
        """
        Get EPS trend for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of EPSTrend models.
        """
        ticker = yf.Ticker(symbol)
        eps_trend_df = ticker.eps_trend
        if eps_trend_df is None or eps_trend_df.empty:
            return []
        eps_trend_df = eps_trend_df.reset_index()
        return [
            EPSTrend.model_validate(row.to_dict())
            for _, row in eps_trend_df.iterrows()
        ]

    def get_eps_revisions(self, symbol: str) -> List[EPSRevisions]:
        """
        Get EPS revisions for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of EPSRevisions models.
        """
        ticker = yf.Ticker(symbol)
        eps_revisions_df = ticker.eps_revisions
        if eps_revisions_df is None or eps_revisions_df.empty:
            return []
        eps_revisions_df = eps_revisions_df.reset_index()
        return [
            EPSRevisions.model_validate(row.to_dict())
            for _, row in eps_revisions_df.iterrows()
        ]

    def get_growth_estimates(self, symbol: str) -> List[GrowthEstimates]:
        """
        Get growth estimates for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of GrowthEstimates models.
        """
        ticker = yf.Ticker(symbol)
        growth_estimates_df = ticker.growth_estimates
        if growth_estimates_df is None or growth_estimates_df.empty:
            return []
        growth_estimates_df = growth_estimates_df.reset_index()
        return [
            GrowthEstimates.model_validate(row.to_dict())
            for _, row in growth_estimates_df.iterrows()
        ]

    def get_major_holders(self, symbol: str) -> MajorHolder:
        """
        Get major holders information for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            MajorHolder: A Pydantic model containing major holders data.
        """
        ticker = yf.Ticker(symbol)
        major_holders_df = ticker.major_holders
        if major_holders_df is None or major_holders_df.empty:
            return MajorHolder()
        # Convert DataFrame to dict format that matches our model
        major_holders_dict = {
            'insidersPercentHeld': major_holders_df.iloc[0, 0] if len(major_holders_df) > 0 else None,
            'institutionsPercentHeld': major_holders_df.iloc[1, 0] if len(major_holders_df) > 1 else None,
            'institutionsFloatPercentHeld': major_holders_df.iloc[2, 0] if len(major_holders_df) > 2 else None,
            'institutionsCount': major_holders_df.iloc[3, 0] if len(major_holders_df) > 3 else None,
        }
        return MajorHolder.model_validate(major_holders_dict)

    def get_institutional_holders(self, symbol: str) -> List[InstitutionalHolder]:
        """
        Get institutional holders for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of InstitutionalHolder models.
        """
        ticker = yf.Ticker(symbol)
        institutional_holders_df = ticker.institutional_holders
        if institutional_holders_df is None or institutional_holders_df.empty:
            return []
        institutional_holders_df = institutional_holders_df.reset_index(drop=True)
        return [
            InstitutionalHolder.model_validate(row.to_dict())
            for _, row in institutional_holders_df.iterrows()
        ]

    def get_mutualfund_holders(self, symbol: str) -> List[MutualFundHolder]:
        """
        Get mutual fund holders for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of MutualFundHolder models.
        """
        ticker = yf.Ticker(symbol)
        mutualfund_holders_df = ticker.mutualfund_holders
        if mutualfund_holders_df is None or mutualfund_holders_df.empty:
            return []
        mutualfund_holders_df = mutualfund_holders_df.reset_index(drop=True)
        return [
            MutualFundHolder.model_validate(row.to_dict())
            for _, row in mutualfund_holders_df.iterrows()
        ]

    def get_insider_transactions(self, symbol: str) -> List[InsiderTransaction]:
        """
        Get insider transactions for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of InsiderTransaction models.
        """
        ticker = yf.Ticker(symbol)
        insider_transactions_df = ticker.insider_transactions
        if insider_transactions_df is None or insider_transactions_df.empty:
            return []
        insider_transactions_df = insider_transactions_df.reset_index(drop=True)
        return [
            InsiderTransaction.model_validate(row.to_dict())
            for _, row in insider_transactions_df.iterrows()
        ]

    def get_insider_purchases(self, symbol: str) -> List[InsiderPurchase]:
        """
        Get insider purchases for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of InsiderPurchase models.
        """
        ticker = yf.Ticker(symbol)
        insider_purchases_df = ticker.insider_purchases
        if insider_purchases_df is None or insider_purchases_df.empty:
            return []
        insider_purchases_df = insider_purchases_df.reset_index()
        return [
            InsiderPurchase.model_validate(row.to_dict())
            for _, row in insider_purchases_df.iterrows()
        ]

    def get_insider_roster_holders(self, symbol: str) -> List[InsiderRosterHolder]:
        """
        Get insider roster holders for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of InsiderRosterHolder models.
        """
        ticker = yf.Ticker(symbol)
        insider_roster_holders_df = ticker.insider_roster_holders
        if insider_roster_holders_df is None or insider_roster_holders_df.empty:
            return []
        insider_roster_holders_df = insider_roster_holders_df.reset_index(drop=True)
        return [
            InsiderRosterHolder.model_validate(row.to_dict())
            for _, row in insider_roster_holders_df.iterrows()
        ]

    def get_sustainability(self, symbol: str) -> SustainabilityData:
        """
        Get sustainability (ESG) data for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            SustainabilityData: A Pydantic model containing ESG data.
        """
        ticker = yf.Ticker(symbol)
        sustainability_df = ticker.sustainability
        if sustainability_df is None or sustainability_df.empty:
            return SustainabilityData()
        # Convert DataFrame to dict
        sustainability_dict = sustainability_df.iloc[:, 0].to_dict()
        return SustainabilityData.model_validate(sustainability_dict)

    def get_news(self, symbol: str) -> List[NewsArticle]:
        """
        Get news articles for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of NewsArticle models.
        """
        ticker = yf.Ticker(symbol)
        news_list = ticker.news
        if not news_list:
            return []
        return [NewsArticle.model_validate(article) for article in news_list]

    def get_sec_filings(self, symbol: str) -> List[SECFiling]:
        """
        Get SEC filings for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of SECFiling models.
        """
        ticker = yf.Ticker(symbol)
        sec_filings_df = ticker.sec_filings
        if sec_filings_df is None or sec_filings_df.empty:
            return []
        sec_filings_df = sec_filings_df.reset_index(drop=True)
        return [
            SECFiling.model_validate(row.to_dict())
            for _, row in sec_filings_df.iterrows()
        ]

    def get_funds_data(self, symbol: str) -> FundData:
        """
        Get fund data for a given ticker (applies to ETFs and mutual funds).

        Args:
            symbol: The fund ticker symbol.

        Returns:
            FundData: A Pydantic model containing fund-specific data.
        """
        ticker = yf.Ticker(symbol)
        funds_data_dict = ticker.funds_data
        if not funds_data_dict:
            return FundData()
        return FundData.model_validate(funds_data_dict)

    def get_shares_full(self, symbol: str) -> List[SharesOutstanding]:
        """
        Get full shares outstanding history for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of SharesOutstanding models.
        """
        ticker = yf.Ticker(symbol)
        shares_df = ticker.get_shares_full()
        if shares_df is None or shares_df.empty:
            return []
        shares_df = shares_df.reset_index()
        shares_df.columns = ['date', 'shares']
        shares_df['date'] = shares_df['date'].dt.date
        return [
            SharesOutstanding.model_validate(row.to_dict())
            for _, row in shares_df.iterrows()
        ]

    def get_capital_gains(self, symbol: str) -> List[CapitalGain]:
        """
        Get capital gains for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of CapitalGain models.
        """
        ticker = yf.Ticker(symbol)
        capital_gains_series = ticker.capital_gains
        if capital_gains_series is None or capital_gains_series.empty:
            return []
        capital_gains_df = capital_gains_series.reset_index()
        capital_gains_df.columns = ['date', 'Capital Gains']
        capital_gains_df['date'] = capital_gains_df['date'].dt.date
        return [
            CapitalGain.model_validate(row.to_dict())
            for _, row in capital_gains_df.iterrows()
        ]

    def get_actions(self, symbol: str) -> List[Action]:
        """
        Get all stock actions (dividends and splits) for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A list of Action models.
        """
        ticker = yf.Ticker(symbol)
        actions_df = ticker.actions
        if actions_df is None or actions_df.empty:
            return []
        actions_df = actions_df.reset_index()
        actions_df['Date'] = actions_df['Date'].dt.date
        actions_df = actions_df.rename(columns={'Date': 'date'})
        return [
            Action.model_validate(row.to_dict())
            for _, row in actions_df.iterrows()
        ]

    def get_isin(self, symbol: str) -> str:
        """
        Get ISIN (International Securities Identification Number) for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            The ISIN string.
        """
        ticker = yf.Ticker(symbol)
        return ticker.isin

    def get_history_metadata(self, symbol: str) -> Dict[str, Any]:
        """
        Get history metadata for a given ticker.

        Args:
            symbol: The stock ticker symbol.

        Returns:
            A dictionary containing history metadata.
        """
        ticker = yf.Ticker(symbol)
        return ticker.get_history_metadata()
