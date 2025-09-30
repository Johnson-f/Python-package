"""
Stonksapi - A comprehensive financial data API package.

This package provides unified access to multiple financial data providers
with strongly-typed Pydantic models.

Submodules:
    - alpha_vantage: Alpha Vantage API wrapper
    - yfinance: Yahoo Finance wrapper
    - polygon: Polygon.io wrapper  
    - finnhub: Finnhub wrapper
    - defeatbeat_api: DefeatBeta wrapper

Example:
    >>> from stonksapi.alpha_vantage import AlphaVantageClient
    >>> client = AlphaVantageClient(api_key="your_key")
    >>> quote = client.get_quote("AAPL")
"""

__version__ = "0.1.0"

__all__ = ["__version__"]
