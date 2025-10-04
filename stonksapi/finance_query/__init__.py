"""
Finance Query API wrapper with comprehensive market data access.

This module provides a type-safe wrapper around the Finance Query API.
"""

from .client import FinanceQueryClient
from .models import (
    # Core Models
    MarketHours,
    DetailedQuote,
    SimpleQuote,
    SimilarStock,
    HistoricalDataPoint,
    MarketMover,
    StockNews,
    SymbolSearchResult,
    SectorPerformance,
    
    # Enums
    StatementType,
    Frequency,
    HolderType,
    
    # Financial Statement Models
    FinancialStatement,
    
    # Holders Models
    MajorHoldersBreakdown,
    InstitutionalHolder,
    MutualFundHolder,
    InsiderTransaction,
    InsiderPurchase,
    InsiderRosterMember,
    HoldersData,
    
    # Earnings Models
    TranscriptMetadata,
    TranscriptItem,
    EarningsTranscript,
    
    # Technical Indicators Models
    SMAData,
    EMAData,
    WMAData,
    VWMAData,
    RSIData,
    SRSIData,
    STOCHData,
    CCIData,
    MACDData,
    ADXData,
    AROONData,
    BBANDSData,
    OBVData,
    SuperTrendData,
    IchimokuData,
    TechnicalIndicator,
    
    # Market Models
    MarketIndex,
)

__all__ = [
    "FinanceQueryClient",
    
    # Core Models
    "MarketHours",
    "DetailedQuote", 
    "SimpleQuote",
    "SimilarStock",
    "HistoricalDataPoint",
    "MarketMover",
    "StockNews",
    "SymbolSearchResult",
    "SectorPerformance",
    
    # Enums
    "StatementType",
    "Frequency",
    "HolderType",
    
    # Financial Statement Models
    "FinancialStatement",
    
    # Holders Models
    "MajorHoldersBreakdown",
    "InstitutionalHolder",
    "MutualFundHolder", 
    "InsiderTransaction",
    "InsiderPurchase",
    "InsiderRosterMember",
    "HoldersData",
    
    # Earnings Models
    "TranscriptMetadata",
    "TranscriptItem",
    "EarningsTranscript",
    
    # Technical Indicators Models
    "SMAData",
    "EMAData",
    "WMAData",
    "VWMAData",
    "RSIData",
    "SRSIData",
    "STOCHData",
    "CCIData",
    "MACDData",
    "ADXData",
    "AROONData",
    "BBANDSData",
    "OBVData",
    "SuperTrendData",
    "IchimokuData",
    "TechnicalIndicator",
    
    # Market Models
    "MarketIndex",
]