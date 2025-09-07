"""Market data providers implementation"""

from .alpha_vantage import AlphaVantageProvider
from .finnhub import FinnhubProvider
from .polygon import PolygonProvider
from .twelve_data import TwelveDataProvider
from .fmp import FMPProvider
from .tiingo import TiingoProvider
from .api_ninjas import APINinjasProvider 
from .fiscal import FiscalAIProvider
from .fred import FREDProvider
from .newsapi import NewsAPIProvider
from .newsapi_ai import NewsAPIAIProvider
from .currents_api import CurrentsAPIProvider
from .mediastack import MediaStackProvider
from .gnews import GNewsProvider
try:
    from .yahoo_finance import YahooFinanceProvider
    YAHOO_AVAILABLE = True
except ImportError:
    YahooFinanceProvider = None
    YAHOO_AVAILABLE = False

__all__ = [
    'AlphaVantageProvider',
    'FinnhubProvider',
    'PolygonProvider',
    'TwelveDataProvider',
    'FMPProvider',
    'TiingoProvider',
    'APINinjasProvider',
    'FiscalAIProvider',
    'FREDProvider',
    'NewsAPIProvider',
    'NewsAPIAIProvider',
    'CurrentsAPIProvider',
    'MediaStackProvider',
    'GNewsProvider',
]

# Only add YahooFinanceProvider to __all__ if it's available
if YAHOO_AVAILABLE and YahooFinanceProvider is not None:
    __all__.append('YahooFinanceProvider')
