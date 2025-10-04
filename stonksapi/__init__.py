"""
Stonksapi - A comprehensive financial data API package.

This package provides unified access to multiple financial data providers
with strongly-typed Pydantic models.

Example:
    >>> from stonksapi import StonksApiClient, TickerInfo, Quote
    >>> client = StonksApiClient()
    >>> ticker_info: TickerInfo = client.get_ticker_info("AAPL")
    >>> quote: Quote = client.get_quote("AAPL")
"""

__version__ = "0.4.0"

from .client import StonksApiClient
from .models import (
    # Unified Models
    TickerInfo,
    Quote,
    HistoricalData,
    NewsArticle,

    # YFinance Models - Core
    FastInfo,
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
    SustainabilityData,
    SECFiling,
    FundData,
    SharesOutstanding,
    CapitalGain,
    Action,

    # Finance Query Models - Core
    DetailedQuote,
    SimpleQuote,
    SimilarStock,
    HistoricalDataPoint,
    StockNews,
    SymbolSearchResult,
    
    # Financial Statements
    FinancialStatement,
    
    # Holders Models (both providers have these)
    InstitutionalHolder,
    MutualFundHolder,
    InsiderTransaction,
    InsiderPurchase,
    InsiderRosterHolder,
    
    # Finance Query Specific
    MajorHoldersBreakdown,
    InsiderRosterMember,
    HoldersData,
    EarningsTranscript,
    TranscriptItem,
    TranscriptMetadata,
    TechnicalIndicator,
    MarketIndex,
    
    # Technical Indicators
    SMAData,
    EMAData,
    RSIData,
    MACDData,
    BBANDSData,
    
    # Enums
    StatementType,
    Frequency,
    HolderType,

    # Other Models  
    Dividend,
    Split,
    MarketHours,
    MarketMover,
    SectorPerformance,
)

__all__ = [
    "StonksApiClient",
    
    # Unified Models
    "TickerInfo",
    "Quote", 
    "HistoricalData",
    "NewsArticle",
    
    # YFinance Models - Core
    "FastInfo",
    "EarningsData",
    "EarningsCalendar", 
    "EarningsEstimate",
    "RevenueEstimate",
    "Recommendation",
    "RecommendationSummary",
    "UpgradeDowngrade",
    "AnalystPriceTarget",
    "EPSTrend",
    "EPSRevisions",
    "GrowthEstimates",
    "MajorHolder",
    "SustainabilityData",
    "SECFiling",
    "FundData",
    "SharesOutstanding",
    "CapitalGain",
    "Action",
    
    # Finance Query Models - Core
    "DetailedQuote",
    "SimpleQuote",
    "SimilarStock",
    "HistoricalDataPoint",
    "StockNews",
    "SymbolSearchResult",
    
    # Financial Statements
    "FinancialStatement",
    
    # Holders Models
    "InstitutionalHolder",
    "MutualFundHolder",
    "InsiderTransaction", 
    "InsiderPurchase",
    "InsiderRosterHolder",
    "MajorHoldersBreakdown",
    "InsiderRosterMember",
    "HoldersData",
    
    # Earnings and Analysis
    "EarningsTranscript",
    "TranscriptItem",
    "TranscriptMetadata",
    "TechnicalIndicator",
    "MarketIndex",
    
    # Technical Indicators
    "SMAData",
    "EMAData", 
    "RSIData",
    "MACDData",
    "BBANDSData",
    
    # Enums
    "StatementType",
    "Frequency",
    "HolderType",
    
    # Other Models
    "Dividend",
    "Split", 
    "MarketHours",
    "MarketMover",
    "SectorPerformance",
]