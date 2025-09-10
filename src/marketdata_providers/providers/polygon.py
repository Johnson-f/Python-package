"""
Polygon.io API Provider Implementation (Updated 2025)

This module provides an asynchronous interface to the Polygon.io stock market data API.
It includes comprehensive error handling, rate limiting, and data normalization.
All endpoints have been verified against the current Polygon.io API documentation and
updated to include the latest available endpoints.

Supported endpoints include:
- Real-time and historical stock data
- Options data and contract details
- Company fundamentals and financials
- Market news and events
- Full market snapshots and unified snapshots
- Technical indicators and market analytics
- Forex and cryptocurrency data
- Gainers/losers, market holidays, and conditions
- Reference data for tickers, exchanges, and conditions
"""

import aiohttp
import asyncio
import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, date, timedelta, timezone
from decimal import Decimal, InvalidOperation

from ..base import (
    MarketDataProvider, 
    StockQuote, 
    HistoricalPrice, 
    OptionQuote, 
    CompanyInfo,
    EconomicEvent
)

# Configure logger
logger = logging.getLogger(__name__)

# API Rate Limits (requests per minute)
POLYGON_RATE_LIMITS = {
    'free': 5,          # Free tier: 5 requests per minute
    'basic': 100,       # Basic tier: 100 requests per minute
    'starter': 100,     # Starter tier: 100 requests per minute
    'developer': 500,   # Developer tier: 500 requests per minute
    'advanced': 1000,   # Advanced tier: 1000 requests per minute
    'pro': 2000,        # Pro tier: 2000 requests per minute
    'enterprise': 5000  # Enterprise tier: 5000 requests per minute
}

# Default rate limit (free tier)
DEFAULT_RATE_LIMIT = POLYGON_RATE_LIMITS['free']

class Interval:
    """Standardized interval constants"""
    MIN_1 = "1min"
    MIN_5 = "5min"
    MIN_15 = "15min"
    MIN_30 = "30min"
    HOUR_1 = "1hour"
    HOUR_4 = "4hour"
    DAILY = "1day"
    WEEKLY = "1week"
    MONTHLY = "1month"


class PolygonProvider(MarketDataProvider):
    """
    Polygon.io API implementation with enhanced features and error handling.
    
    This provider supports:
    - Real-time and historical stock data
    - Options data
    - Company fundamentals
    - Market news and events
    - Comprehensive error handling and rate limiting
    
    Updated for 2025 API endpoints and structure.
    """
    
    def __init__(self, api_key: str, rate_limit_tier: str = 'free'):
        """
        Initialize the Polygon.io provider
        
        Args:
            api_key: Your Polygon.io API key
            rate_limit_tier: API rate limit tier ('free', 'basic', 'starter', 'developer', 'advanced', 'pro', 'enterprise')
        """
        super().__init__(api_key, "Polygon")
        self.base_url = "https://api.polygon.io"
        self.rate_limit = POLYGON_RATE_LIMITS.get(rate_limit_tier.lower(), DEFAULT_RATE_LIMIT)
        self.rate_limit_semaphore = asyncio.Semaphore(self.rate_limit)
        self.last_request_time = None
        self.request_count = 0
        self.rate_limit_reset = None
    
    def _safe_decimal(self, value: Any, default: Decimal = Decimal('0')) -> Decimal:
        """Safely convert value to Decimal"""
        if value is None:
            return default
        try:
            if isinstance(value, (int, float, Decimal)):
                return Decimal(str(value))
            if isinstance(value, str):
                # Remove any non-numeric characters except decimal point and minus
                clean_value = ''.join(c for c in value if c.isdigit() or c in '.-')
                return Decimal(clean_value) if clean_value else default
            return Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            return default
    
    def _safe_int(self, value: Any, default: int = 0) -> int:
        """Safely convert value to int"""
        try:
            return int(float(value)) if value is not None else default
        except (ValueError, TypeError):
            return default
    
    def _map_interval(self, interval: str) -> Tuple[str, int]:
        """
        Map standard interval to Polygon's timespan and multiplier
        
        Args:
            interval: Standard interval string (e.g., '1min', '1h', '1d')
            
        Returns:
            Tuple of (timespan, multiplier)
        """
        interval_mapping = {
            # Minutes
            '1min': ('minute', 1),
            '5min': ('minute', 5),
            '15min': ('minute', 15),
            '30min': ('minute', 30),
            # Hours
            '1h': ('hour', 1),
            '1hour': ('hour', 1),
            '4h': ('hour', 4),
            '4hour': ('hour', 4),
            # Days
            '1d': ('day', 1),
            'daily': ('day', 1),
            # Weeks
            '1w': ('week', 1),
            'weekly': ('week', 1),
            # Months
            '1m': ('month', 1),
            'monthly': ('month', 1),
            # Quarters
            '1q': ('quarter', 1),
            'quarterly': ('quarter', 1),
            # Years
            '1y': ('year', 1),
            'yearly': ('year', 1)
        }
        return interval_mapping.get(interval.lower(), ('day', 1))
    
    async def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        version: str = 'v3',
        retries: int = 3,
        backoff_factor: float = 0.5
    ) -> Optional[Union[Dict, List]]:
        """
        Make an API request to Polygon.io with retries and rate limiting
        
        Args:
            endpoint: API endpoint (without version prefix)
            params: Query parameters
            version: API version (v1, v2, v3, v4, etc.)
            retries: Number of retry attempts
            backoff_factor: Backoff factor for retries
            
        Returns:
            Parsed JSON response or None if request failed
        """
        if params is None:
            params = {}
            
        # Add API key to params (Polygon expects 'apiKey' query param)
        params['apiKey'] = self.api_key
        
        # Build URL
        if version:
            url = f"{self.base_url}/{version.lstrip('/')}/{endpoint.lstrip('/')}"
        else:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Implement rate limiting
        async with self.rate_limit_semaphore:
            # Check if we need to wait for rate limit reset
            if self.rate_limit_reset and datetime.now(timezone.utc) < self.rate_limit_reset:
                wait_time = (self.rate_limit_reset - datetime.now(timezone.utc)).total_seconds()
                if wait_time > 0:
                    logger.warning(f"Rate limit reached. Waiting {wait_time:.2f} seconds...")
                    await asyncio.sleep(wait_time)
            
            # Make the request with retries
            last_error = None
            for attempt in range(retries):
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, params=params) as response:
                            # Update rate limit tracking
                            self.last_request_time = datetime.now(timezone.utc)
                            self.request_count += 1
                            
                            # Handle rate limit headers if present
                            if 'X-RateLimit-Requests-Remaining' in response.headers:
                                remaining = int(response.headers['X-RateLimit-Requests-Remaining'])
                                if remaining <= 0 and 'X-RateLimit-Reset' in response.headers:
                                    reset_ts = int(response.headers['X-RateLimit-Reset'])
                                    self.rate_limit_reset = datetime.fromtimestamp(reset_ts / 1000, tz=timezone.utc)
                                    wait_time = (self.rate_limit_reset - self.last_request_time).total_seconds()
                                    if wait_time > 0:
                                        await asyncio.sleep(wait_time)
                                        continue
                            
                            # Handle response
                            if response.status == 200:
                                data = await response.json()
                                if isinstance(data, dict) and data.get('status') == 'ERROR':
                                    error_msg = data.get('error', 'Unknown error')
                                    self._log_error("API Error", error_msg)
                                    last_error = Exception(f"Polygon API Error: {error_msg}")
                                    continue
                                return data
                            
                            # Handle rate limiting (429)
                            elif response.status == 429:
                                retry_after = int(response.headers.get('X-RateLimit-Reset', 60))
                                logger.warning(f"Rate limited. Retry after {retry_after} seconds")
                                # Don't wait - let the Brain try another provider
                                raise Exception(f"Rate limit exceeded. Retry after {retry_after} seconds")
                            
                            # Handle other errors
                            else:
                                error_text = await response.text()
                                self._log_error(
                                    f"API Request Failed (HTTP {response.status})", 
                                    f"URL: {url}, Response: {error_text}"
                                )
                                last_error = Exception(f"HTTP {response.status}: {error_text}")
                                
                except aiohttp.ClientError as e:
                    last_error = e
                    self._log_error("HTTP Client Error", str(e))
                
                # Exponential backoff
                if attempt < retries - 1:
                    wait_time = backoff_factor * (2 ** attempt)
                    logger.warning(f"Retry {attempt + 1}/{retries} after {wait_time:.2f}s...")
                    await asyncio.sleep(wait_time)
            
            # All retries failed
            if last_error:
                self._log_error("Request Failed", f"All {retries} attempts failed: {str(last_error)}")
            return None
    
    async def get_quote(self, symbol: str) -> Optional[StockQuote]:
        """Get real-time stock quote using current Polygon.io endpoints"""
        if not symbol or not isinstance(symbol, str):
            self._log_error("Invalid Input", f"Invalid symbol: {symbol}")
            return None
        
        symbol = symbol.upper().strip()
        
        try:
            # Use the v2 single-ticker snapshot endpoint
            snapshot_endpoint = f"snapshot/locale/us/markets/stocks/tickers/{symbol}"
            snapshot_data = await self._make_request(snapshot_endpoint, version='v2')
            
            if not snapshot_data or 'ticker' not in snapshot_data:
                self._log_error("Data Unavailable", f"No snapshot data for {symbol}")
                return None
                
            result = snapshot_data['ticker']
            
            # Extract values from the snapshot response
            last_quote = result.get('lastQuote', result.get('last_quote', {}))
            last_trade = result.get('lastTrade', result.get('last_trade', {}))
            prev_daily_bar = result.get('prevDay', result.get('prev_daily_bar', {}))
            day_bar = result.get('day', {})
            
            # Get current price from last trade or derive from last quote
            last_price = None
            if last_trade:
                if 'p' in last_trade:
                    last_price = self._safe_decimal(last_trade.get('p'))
                elif 'price' in last_trade:
                    last_price = self._safe_decimal(last_trade.get('price'))
            if last_price is None and last_quote:
                # Try standard keys from snapshot
                ask = self._safe_decimal(last_quote.get('ask', last_quote.get('P')))
                bid = self._safe_decimal(last_quote.get('bid', last_quote.get('p')))
                if ask > 0 and bid > 0:
                    last_price = (ask + bid) / 2
            
            if not last_price:
                self._log_error("Price Unavailable", f"No price data available for {symbol}")
                return None
            
            # Get previous close for change calculation
            prev_close = None
            if prev_daily_bar and 'c' in prev_daily_bar:
                prev_close = self._safe_decimal(prev_daily_bar['c'])
            
            # Calculate change and change percent
            change = None
            change_percent = None
            if prev_close and prev_close > 0:
                change = last_price - prev_close
                change_percent = (change / prev_close) * 100
            
            # Get other market data
            volume = self._safe_int((day_bar or {}).get('v') or (prev_daily_bar or {}).get('v'))
            open_price = self._safe_decimal((day_bar or {}).get('o'))
            high = self._safe_decimal((day_bar or {}).get('h'))
            low = self._safe_decimal((day_bar or {}).get('l'))
            
            # Get timestamp
            def _to_dt(ts: Any) -> datetime:
                try:
                    ts_int = int(ts)
                    if ts_int > 1_000_000_000_000_000:  # ns
                        return datetime.fromtimestamp(ts_int / 1_000_000_000, tz=timezone.utc)
                    if ts_int > 1_000_000_000_000:  # ms
                        return datetime.fromtimestamp(ts_int / 1000, tz=timezone.utc)
                    if ts_int > 0:  # s
                        return datetime.fromtimestamp(ts_int, tz=timezone.utc)
                except Exception:
                    pass
                return datetime.now(timezone.utc)

            ts_src = None
            if isinstance(last_trade, dict):
                ts_src = last_trade.get('t') or last_trade.get('sip_timestamp')
            if ts_src is None and isinstance(last_quote, dict):
                ts_src = last_quote.get('t')
            timestamp = _to_dt(ts_src or 0)
            
            return StockQuote(
                symbol=symbol,
                price=last_price,
                change=change if change is not None else Decimal('0'),
                change_percent=change_percent if change_percent is not None else Decimal('0'),
                volume=volume,
                open=open_price,
                high=high,
                low=low,
                previous_close=prev_close,
                market_cap=None,  # Not available in snapshot
                pe_ratio=None,    # Not available in snapshot
                timestamp=timestamp,
                provider=self.name
            )
            
        except Exception as e:
            self._log_error("get_quote", f"Failed to fetch quote for {symbol}: {str(e)}")
            return None

    async def get_historical(
        self, 
        symbol: str, 
        start_date: Optional[date] = None, 
        end_date: Optional[date] = None,
        interval: str = "1d",
        limit: int = 5000,
        adjusted: bool = True,
        sort: str = "asc"
    ) -> List[HistoricalPrice]:
        """Get historical stock data using current v2 aggregates endpoint"""
        if not symbol or not isinstance(symbol, str):
            self._log_error("Invalid Input", f"Invalid symbol: {symbol}")
            return []
        
        symbol = symbol.upper().strip()
        end_date = end_date or date.today()
        start_date = start_date or (end_date - timedelta(days=365))
        
        if start_date > end_date:
            self._log_error("Invalid Date Range", f"Start date {start_date} is after end date {end_date}")
            return []
        
        # Validate date range based on interval
        max_days = 365 * 2  # Default for daily data
        if interval in ['1min', '5min', '15min', '30min']:
            max_days = 30  # Minute data limited to 30 days
        elif interval in ['1h', '4h']:
            max_days = 90  # Hour data limited to 90 days
        
        if (end_date - start_date).days > max_days:
            start_date = end_date - timedelta(days=max_days)
            logger.warning(f"Date range adjusted to {start_date} - {end_date} (max {max_days} days)")
        
        timespan, multiplier = self._map_interval(interval)
        
        try:
            all_prices = []
            current_start = start_date
            
            while current_start <= end_date and len(all_prices) < limit:
                # Calculate batch end date (max 2 years per request for daily, less for intraday)
                batch_days = 730 if timespan == 'day' else 90
                batch_end = min(
                    current_start + timedelta(days=batch_days),
                    end_date
                )
                
                # Use v2 aggregates endpoint (current standard)
                endpoint = (
                    f"aggs/ticker/{symbol}/range/"
                    f"{multiplier}/{timespan}/"
                    f"{current_start.strftime('%Y-%m-%d')}/"
                    f"{batch_end.strftime('%Y-%m-%d')}"
                )
                
                params = {
                    'adjusted': 'true' if adjusted else 'false',
                    'sort': sort,
                    'limit': min(50000, limit - len(all_prices)),
                }
                
                data = await self._make_request(endpoint, params, version='v2')
                
                if not data or 'results' not in data or not data['results']:
                    break
                
                for item in data['results']:
                    try:
                        # Convert timestamp to date
                        date_obj = datetime.fromtimestamp(item['t'] / 1000, tz=timezone.utc).date()
                        
                        open_price = self._safe_decimal(item.get('o'))
                        high_price = self._safe_decimal(item.get('h'))
                        low_price = self._safe_decimal(item.get('l'))
                        close_price = self._safe_decimal(item.get('c'))
                        volume = self._safe_int(item.get('v'))
                        
                        all_prices.append(HistoricalPrice(
                            date=date_obj,
                            open=open_price,
                            high=high_price,
                            low=low_price,
                            close=close_price,
                            volume=volume,
                            provider=self.name
                        ))
                    except Exception as e:
                        logger.warning(f"Error parsing historical data item: {str(e)}")
                        continue
                
                current_start = batch_end + timedelta(days=1)
            
            return sorted(all_prices, key=lambda x: x.date)
            
        except Exception as e:
            self._log_error("get_historical", f"Failed to fetch historical data for {symbol}: {str(e)}")
            return []

    async def get_company_info(self, symbol: str) -> Optional[CompanyInfo]:
        """Get company information using current v3 ticker details endpoint"""
        if not symbol or not isinstance(symbol, str):
            self._log_error("Invalid Input", f"Invalid symbol: {symbol}")
            return None
        
        symbol = symbol.upper().strip()
        
        try:
            # Use v3 ticker details endpoint (current standard)
            ticker_details_endpoint = f"reference/tickers/{symbol}"
            ticker_data = await self._make_request(ticker_details_endpoint, version='v3')
            
            if not ticker_data or 'results' not in ticker_data:
                self._log_error("Data Unavailable", f"No ticker details for {symbol}")
                return None
            
            result = ticker_data['results']
            
            # Extract address information
            address = result.get('address', {})
            headquarters = ""
            if address:
                parts = []
                if address.get('address1'):
                    parts.append(address['address1'])
                if address.get('city'):
                    parts.append(address['city'])
                if address.get('state'):
                    parts.append(address['state'])
                if address.get('postal_code'):
                    parts.append(address['postal_code'])
                headquarters = ", ".join(parts)
            
            # Parse market cap
            market_cap = result.get('market_cap')
            if isinstance(market_cap, str):
                try:
                    if market_cap.endswith('M'):
                        market_cap = float(market_cap[:-1]) * 1_000_000
                    elif market_cap.endswith('B'):
                        market_cap = float(market_cap[:-1]) * 1_000_000_000
                    elif market_cap.endswith('T'):
                        market_cap = float(market_cap[:-1]) * 1_000_000_000_000
                    market_cap = int(market_cap)
                except (ValueError, TypeError):
                    market_cap = None
            
            return CompanyInfo(
                symbol=symbol,
                name=result.get('name', ''),
                exchange=result.get('primary_exchange', ''),
                sector=result.get('sic_description', ''),  # SIC description as sector
                industry=result.get('industry', ''),
                market_cap=market_cap,
                employees=self._safe_int(result.get('total_employees')),
                description=result.get('description', '').strip(),
                website=result.get('homepage_url', ''),
                ceo=None,  # CEO info not in basic ticker details
                headquarters=headquarters,
                country=address.get('country', '') if address else '',
                phone=result.get('phone_number', ''),
                tags=result.get('tags', []),
                logo_url=None,  # Logo URL requires separate endpoint
                ipo_date=result.get('list_date'),
                currency=result.get('currency_name', 'USD'),
                pe_ratio=None,  # Financial ratios require separate endpoint
                peg_ratio=None,
                eps=None,
                dividend_yield=None,
                beta=None,
                is_etf=result.get('type', '').upper() == 'ETF',
                is_adr=result.get('composite_figi', '').startswith('BBG') if result.get('composite_figi') else False,
                is_fund=result.get('type', '').upper() in ['FUND', 'ETF'],
                updated_at=datetime.now(timezone.utc).isoformat(),
                provider=self.name
            )
            
        except Exception as e:
            self._log_error("get_company_info", f"Failed to fetch company info for {symbol}: {str(e)}")
            return None

    async def get_options_chain(
        self, 
        symbol: str, 
        expiration: Optional[Union[date, str]] = None,
        option_type: Optional[str] = None,
        strike_price: Optional[Union[float, int]] = None,
        limit: int = 1000,
        include_all_expirations: bool = False
    ) -> List[OptionQuote]:
        """Get options chain using current v3 options contracts endpoint"""
        if not symbol or not isinstance(symbol, str):
            self._log_error("Invalid Input", f"Invalid symbol: {symbol}")
            return []
        
        symbol = symbol.upper().strip()
        
        # Parse expiration date
        expiration_date = None
        if expiration and not include_all_expirations:
            if isinstance(expiration, str):
                try:
                    expiration_date = datetime.strptime(expiration, '%Y-%m-%d').date()
                except ValueError:
                    self._log_error("Invalid Date Format", "Expiration date must be in YYYY-MM-DD format")
                    return []
            elif isinstance(expiration, date):
                expiration_date = expiration
        
        # Validate option type
        if option_type and option_type.lower() not in ['call', 'put']:
            self._log_error("Invalid Option Type", "Option type must be 'call' or 'put'")
            return []
        
        try:
            all_options = []
            
            # Use v3 options contracts endpoint
            params = {
                'underlying_ticker': symbol,
                'limit': min(1000, limit),
                'sort': 'expiration_date',
                'order': 'asc'
            }
            
            if expiration_date and not include_all_expirations:
                params['expiration_date'] = expiration_date.strftime('%Y-%m-%d')
            
            if option_type:
                params['contract_type'] = option_type.lower()
            
            if strike_price is not None:
                params['strike_price'] = str(strike_price)
            
            data = await self._make_request("reference/options/contracts", params, version='v3')
            
            if not data or 'results' not in data or not data['results']:
                return []
            
            # Process options contracts
            for contract in data['results']:
                try:
                    # Parse expiration date
                    exp_date = datetime.strptime(contract['expiration_date'], '%Y-%m-%d').date()
                    
                    option_quote = OptionQuote(
                        symbol=contract.get('ticker', ''),
                        underlying_symbol=contract.get('underlying_ticker', symbol),
                        expiration_date=exp_date,
                        strike_price=self._safe_decimal(contract.get('strike_price')),
                        option_type=contract.get('contract_type', '').upper(),
                        bid=Decimal('0'),  # Real-time prices need separate endpoint
                        ask=Decimal('0'),
                        last_price=Decimal('0'),
                        volume=0,
                        open_interest=0,
                        implied_volatility=None,
                        delta=None,
                        gamma=None,
                        theta=None,
                        vega=None,
                        rho=None,
                        timestamp=datetime.now(timezone.utc),
                        provider=self.name
                    )
                    
                    all_options.append(option_quote)
                    
                except Exception as e:
                    logger.warning(f"Error parsing option contract: {str(e)}")
                    continue
            
            return all_options[:limit]
            
        except Exception as e:
            self._log_error("get_options_chain", f"Failed to fetch options chain for {symbol}: {str(e)}")
            return []

    async def get_market_status(self) -> Dict[str, Any]:
        """Get market status using current v1 market status endpoint"""
        try:
            # Use v1 market status endpoint (current standard)
            data = await self._make_request("marketstatus/now", version='v1')
            
            if not data:
                return self._default_market_status("API error")
            
            # Handle different response structures
            if isinstance(data, dict):
                if 'market' in data:
                    market = data['market']
                elif 'results' in data and data['results']:
                    market = data['results'][0] if isinstance(data['results'], list) else data['results']
                else:
                    market = data
                
                return {
                    'is_open': market.get('market') == 'open' or market.get('isOpen', False),
                    'status': market.get('market', 'unknown'),
                    'exchange': market.get('exchange', 'NYSE'),
                    'currency': market.get('currency', 'USD'),
                    'server_time': market.get('serverTime'),
                    'early_hours': market.get('earlyHours', False),
                    'after_hours': market.get('afterHours', False),
                    'provider': self.name,
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
            
            return self._default_market_status("unexpected response format")
            
        except Exception as e:
            self._log_error("get_market_status", f"Failed to get market status: {str(e)}")
            return self._default_market_status(f"error: {str(e)}")
    
    def _default_market_status(self, reason: str) -> Dict[str, Any]:
        """Return default market status"""
        return {
            'is_open': False,
            'status': 'unknown',
            'reason': reason,
            'provider': self.name,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

    async def get_news(
        self, 
        symbol: Optional[str] = None,
        limit: int = 10,
        published_after: Optional[Union[date, str]] = None,
        published_before: Optional[Union[date, str]] = None,
        order: str = 'desc'
    ) -> List[Dict[str, Any]]:
        """Get news using current v2 ticker news endpoint"""
        try:
            params = {
                'limit': max(1, min(1000, limit)),
                'order': order
            }
            
            # Add ticker filter if specified
            if symbol:
                params['ticker'] = symbol.upper().strip()
            
            # Add date filters
            if published_after:
                if isinstance(published_after, date):
                    params['published_utc.gte'] = published_after.strftime('%Y-%m-%d')
                elif isinstance(published_after, str):
                    params['published_utc.gte'] = published_after
            
            if published_before:
                if isinstance(published_before, date):
                    params['published_utc.lte'] = published_before.strftime('%Y-%m-%d')
                elif isinstance(published_before, str):
                    params['published_utc.lte'] = published_before
            
            # Use v2 ticker news endpoint
            data = await self._make_request("reference/news", params, version='v2')
            
            if not data or 'results' not in data or not data['results']:
                return []
            
            return data['results']
            
        except Exception as e:
            self._log_error("get_news", f"Failed to fetch news: {str(e)}")
            return []

    async def get_dividends(self, symbol: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get dividend data using current v3 dividends endpoint"""
        try:
            params = {
                'ticker': symbol.upper(),
                'limit': max(1, min(1000, limit))
            }
            
            data = await self._make_request("reference/dividends", params, version='v3')
            
            if not data or 'results' not in data or not data['results']:
                return []
            
            return data['results']
            
        except Exception as e:
            self._log_error("get_dividends", f"Failed to fetch dividends for {symbol}: {str(e)}")
            return []

    async def get_splits(self, symbol: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get stock splits using current v3 splits endpoint"""
        try:
            params = {
                'ticker': symbol.upper(),
                'limit': max(1, min(1000, limit))
            }
            
            data = await self._make_request("reference/splits", params, version='v3')
            
            if not data or 'results' not in data or not data['results']:
                return []
            
            return data['results']
            
        except Exception as e:
            self._log_error("get_splits", f"Failed to fetch splits for {symbol}: {str(e)}")
            return []

    async def get_market_holidays(self, year: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get market holidays using current v1 market holidays endpoint"""
        try:
            params = {}
            if year:
                params['year'] = year
            
            data = await self._make_request("marketstatus/upcoming", params, version='v1')
            
            if not data:
                return []
            
            # Handle different response structures
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'results' in data:
                return data['results'] if isinstance(data['results'], list) else [data['results']]
            
            return []
            
        except Exception as e:
            self._log_error("get_market_holidays", f"Failed to fetch market holidays: {str(e)}")
            return []

    async def get_earnings_calendar(
        self, 
        ticker: Optional[str] = None,
        date: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        fiscal_period: Optional[str] = None,
        limit: int = 100,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get earnings calendar data - NOTE: This requires a premium Polygon.io plan
        
        Args:
            ticker: Stock symbol to filter by
            date: Specific date (YYYY-MM-DD format)
            date_from: Start date for range query
            date_to: End date for range query  
            fiscal_period: Fiscal period (Q1, Q2, Q3, Q4, H1, H2, FY)
            limit: Maximum number of results
        
        Returns:
            Dictionary containing earnings data
        """
        # Polygon.io doesn't provide earnings calendar data in free tier
        # This endpoint doesn't exist in their API
        logger.info("Polygon.io earnings calendar requires premium plan and is not available in free tier")
        
        return {
            'status': 'not_available',
            'message': 'Earnings calendar data is not available through Polygon.io free tier',
            'ticker': ticker,
            'provider': self.name,
            'suggestion': 'Upgrade to premium plan or use alternative data source like Yahoo Finance, Alpha Vantage, or Finnhub'
        }

    async def get_financials(self, symbol: str, limit: int = 4) -> Optional[Dict[str, Any]]:
        """Get financial statements using current vX financials endpoint"""
        try:
            params = {
                'ticker': symbol.upper(),
                'limit': max(1, min(100, limit)),
                'timeframe': 'annual',
                'include_sources': 'true'
            }
            
            data = await self._make_request("reference/financials", params, version='vX')
            
            if not data or 'results' not in data or not data['results']:
                return None
            
            # Process financial data
            financials_data = data['results'][0] if data['results'] else {}
            financials = financials_data.get('financials', {})
            
            return {
                'symbol': symbol,
                'provider': self.name,
                'fiscal_year': financials_data.get('fiscal_year'),
                'fiscal_period': financials_data.get('fiscal_period'),
                'end_date': financials_data.get('end_date'),
                'filing_date': financials_data.get('filing_date'),
                'source_filing_url': financials_data.get('source_filing_url'),
                'source_filing_file_url': financials_data.get('source_filing_file_url'),
                
                # Income Statement
                'income_statement': {
                    'revenues': self._get_financial_value(financials, 'income_statement', 'revenues'),
                    'cost_of_revenue': self._get_financial_value(financials, 'income_statement', 'cost_of_revenue'),
                    'gross_profit': self._get_financial_value(financials, 'income_statement', 'gross_profit'),
                    'operating_expenses': self._get_financial_value(financials, 'income_statement', 'operating_expenses'),
                    'operating_income': self._get_financial_value(financials, 'income_statement', 'operating_income_loss'),
                    'net_income': self._get_financial_value(financials, 'income_statement', 'net_income_loss'),
                    'eps_basic': self._get_financial_value(financials, 'income_statement', 'basic_earnings_per_share'),
                    'eps_diluted': self._get_financial_value(financials, 'income_statement', 'diluted_earnings_per_share'),
                    'weighted_average_shares': self._get_financial_value(financials, 'income_statement', 'weighted_average_shares'),
                    'weighted_average_shares_diluted': self._get_financial_value(financials, 'income_statement', 'weighted_average_shares_diluted')
                },
                
                # Balance Sheet  
                'balance_sheet': {
                    'assets': self._get_financial_value(financials, 'balance_sheet', 'assets'),
                    'current_assets': self._get_financial_value(financials, 'balance_sheet', 'current_assets'),
                    'noncurrent_assets': self._get_financial_value(financials, 'balance_sheet', 'noncurrent_assets'),
                    'liabilities': self._get_financial_value(financials, 'balance_sheet', 'liabilities'),
                    'current_liabilities': self._get_financial_value(financials, 'balance_sheet', 'current_liabilities'),
                    'noncurrent_liabilities': self._get_financial_value(financials, 'balance_sheet', 'liabilities_noncurrent'),
                    'equity': self._get_financial_value(financials, 'balance_sheet', 'equity'),
                    'equity_attributable_to_parent': self._get_financial_value(financials, 'balance_sheet', 'equity_attributable_to_parent')
                },
                
                # Cash Flow Statement
                'cash_flow_statement': {
                    'net_cash_flow_from_operating_activities': self._get_financial_value(financials, 'cash_flow_statement', 'net_cash_flow_from_operating_activities'),
                    'net_cash_flow_from_investing_activities': self._get_financial_value(financials, 'cash_flow_statement', 'net_cash_flow_from_investing_activities'),
                    'net_cash_flow_from_financing_activities': self._get_financial_value(financials, 'cash_flow_statement', 'net_cash_flow_from_financing_activities'),
                    'net_cash_flow': self._get_financial_value(financials, 'cash_flow_statement', 'net_cash_flow')
                }
            }
            
        except Exception as e:
            self._log_error("get_financials", f"Failed to fetch financials for {symbol}: {str(e)}")
            return None
    
    def _get_financial_value(self, financials: Dict, statement: str, field: str) -> Optional[float]:
        """Extract financial value from nested structure"""
        try:
            statement_data = financials.get(statement, {})
            field_data = statement_data.get(field, {})
            
            if isinstance(field_data, dict):
                return field_data.get('value')
            return field_data
        except (AttributeError, KeyError):
            return None

    async def get_technical_indicators(
        self,
        symbol: str,
        indicator: str,
        timespan: str = 'day',
        adjusted: bool = True,
        window: int = 50,
        series_type: str = 'close',
        expand_underlying: bool = False,
        order: str = 'desc',
        limit: int = 5000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get technical indicators - NOTE: This requires a premium Polygon.io plan
        
        Available indicators: sma, ema, macd, rsi, etc.
        """
        try:
            params = {
                'ticker': symbol.upper(),
                'timespan': timespan,
                'adjusted': adjusted,
                'window': window,
                'series_type': series_type,
                'expand_underlying': expand_underlying,
                'order': order,
                'limit': max(1, min(5000, limit))
            }
            
            # Add any additional parameters
            params.update(kwargs)
            
            endpoint = f"indicators/{indicator.lower()}/{symbol.upper()}"
            data = await self._make_request(endpoint, params, version='v1')
            
            if data and 'results' in data:
                return {
                    'status': 'success',
                    'indicator': indicator,
                    'symbol': symbol,
                    'results': data['results'],
                    'next_url': data.get('next_url'),
                    'provider': self.name
                }
            
            return {
                'status': 'no_data',
                'indicator': indicator,
                'symbol': symbol,
                'provider': self.name
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Technical indicators may require premium plan: {str(e)}',
                'indicator': indicator,
                'symbol': symbol,
                'provider': self.name
            }

    async def get_forex_quote(self, from_currency: str, to_currency: str) -> Optional[Dict[str, Any]]:
        """Get real-time forex quote using v1 last quote endpoint (currencies)"""
        try:
            from_ccy = from_currency.upper()
            to_ccy = to_currency.upper()
            
            # Use v1 forex last quote endpoint
            data = await self._make_request(f"last_quote/currencies/{from_ccy}/{to_ccy}", version='v1')
            
            if not data:
                return None
            
            result = data.get('last') or data.get('results') or {}
            bid = self._safe_decimal(result.get('bid') or result.get('bp') or result.get('b'))
            ask = self._safe_decimal(result.get('ask') or result.get('ap') or result.get('a'))
            price = (bid + ask) / 2 if bid and ask and bid > 0 and ask > 0 else self._safe_decimal(result.get('price'))
            
            # Timestamp handling (seconds or milliseconds)
            ts = result.get('timestamp') or result.get('t') or 0
            try:
                ts_int = int(ts)
                ts_dt = datetime.fromtimestamp(ts_int / 1000, tz=timezone.utc) if ts_int > 1_000_000_000_000 else datetime.fromtimestamp(ts_int, tz=timezone.utc)
            except Exception:
                ts_dt = datetime.now(timezone.utc)
            
            return {
                'from_currency': from_ccy,
                'to_currency': to_ccy,
                'symbol': f"C:{from_ccy}{to_ccy}",
                'bid': bid,
                'ask': ask,
                'price': price,
                'timestamp': ts_dt,
                'provider': self.name
            }
            
        except Exception as e:
            self._log_error("get_forex_quote", f"Failed to fetch forex quote {from_currency}/{to_currency}: {str(e)}")
            return None

    async def get_crypto_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get real-time crypto last trade using v1 crypto endpoint"""
        try:
            raw = symbol.upper().replace('X:', '')
            base, quote = (raw, 'USD') if '/' not in raw else raw.split('/', 1)
            if raw.endswith('USD') and '/' not in raw:
                base, quote = raw[:-3], 'USD'
            
            # Use v1 crypto last trade endpoint
            data = await self._make_request(f"last/crypto/{base}/{quote}", version='v1')
            
            if not data:
                return None
            
            result = data.get('last') or data.get('results') or {}
            price = self._safe_decimal(result.get('price') or result.get('p'))
            size = self._safe_decimal(result.get('size') or result.get('s'))
            exch = result.get('exchange') or result.get('x')
            
            ts = result.get('timestamp') or result.get('t') or 0
            try:
                ts_int = int(ts)
                # Crypto timestamps sometimes in nanoseconds
                if ts_int > 1_000_000_000_000_000:
                    ts_dt = datetime.fromtimestamp(ts_int / 1_000_000_000, tz=timezone.utc)
                elif ts_int > 1_000_000_000_000:
                    ts_dt = datetime.fromtimestamp(ts_int / 1000, tz=timezone.utc)
                else:
                    ts_dt = datetime.fromtimestamp(ts_int, tz=timezone.utc)
            except Exception:
                ts_dt = datetime.now(timezone.utc)
            
            return {
                'symbol': f"X:{base}{quote}",
                'price': price,
                'size': size,
                'timestamp': ts_dt,
                'exchange': exch,
                'provider': self.name
            }
            
        except Exception as e:
            self._log_error("get_crypto_quote", f"Failed to fetch crypto quote {symbol}: {str(e)}")
            return None

    # Economic data methods - Polygon.io doesn't provide these directly
    async def get_economic_data(
        self,
        indicator: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 100,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Economic indicators are not available via Polygon.io
        Polygon.io focuses on market data (stocks, options, forex, crypto)
        """
        logger.warning("Economic indicators not available via Polygon.io")
        
        return {
            "status": "not_available",
            "message": "Economic data indicators are not available through Polygon.io API",
            "indicator": indicator,
            "provider": self.name,
            "suggestion": "Consider using FRED API, Alpha Vantage, or other economic data providers",
            "available_data_types": [
                "Stock market data (Real-time & Historical)",
                "Options data", 
                "Forex data",
                "Cryptocurrency data",
                "Market indices",
                "Company financials",
                "Technical indicators (Premium)",
                "News & market events"
            ]
        }
    
    async def get_economic_events(
        self,
        date: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        importance: Optional[str] = None,
        country: Optional[str] = None,
        limit: int = 100,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Economic events calendar is not available via Polygon.io
        """
        logger.warning("Economic events calendar not available via Polygon.io")
        
        return {
            "status": "not_available",
            "message": "Economic events calendar is not available through Polygon.io API",
            "provider": self.name,
            "alternatives": [
                "Trading Economics API",
                "Alpha Vantage Economic Data", 
                "FRED API (Federal Reserve Economic Data)",
                "Forex Factory Calendar",
                "Investing.com Economic Calendar API"
            ],
            "polygon_alternatives": {
                "earnings_calendar": "Available with premium plans",
                "market_holidays": "Available via market status endpoints",
                "stock_splits": "Available via reference/splits",
                "dividends": "Available via reference/dividends",
                "market_news": "Available via reference/news"
            }
        }

    async def search_tickers(
        self,
        search_query: str,
        market: str = 'stocks',
        active: bool = True,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Search for tickers using current v3 tickers endpoint"""
        try:
            params = {
                'search': search_query,
                'market': market,
                'active': active,
                'limit': max(1, min(1000, limit)),
                'sort': 'ticker',
                'order': 'asc'
            }
            
            data = await self._make_request("reference/tickers", params, version='v3')
            
            if not data or 'results' not in data or not data['results']:
                return []
            
            return data['results']
            
        except Exception as e:
            self._log_error("search_tickers", f"Failed to search tickers: {str(e)}")
            return []

    async def get_market_indices(self) -> List[Dict[str, Any]]:
        """Get major market indices data via v3 unified snapshot"""
        indices = [
            'I:SPX',   # S&P 500
            'I:DJI',   # Dow Jones
            'I:NDX',   # NASDAQ 100
            'I:RUT',   # Russell 2000
            'I:VIX'    # VIX
        ]
        try:
            params = { 'tickers': ','.join(indices) }
            data = await self._make_request("snapshot", params, version='v3')
            if not data or 'tickers' not in data:
                return []
            results: List[Dict[str, Any]] = []
            for t in data['tickers']:
                sym = t.get('ticker')
                if not sym:
                    continue
                results.append({
                    'symbol': sym,
                    'name': self._get_index_name(sym),
                    'data': t,
                    'provider': self.name
                })
            return results
        except Exception as e:
            logger.warning(f"Failed to fetch market indices snapshot: {str(e)}")
            return []
    
    def _get_index_name(self, symbol: str) -> str:
        """Get friendly name for market index"""
        index_names = {
            'I:SPX': 'S&P 500',
            'I:DJI': 'Dow Jones Industrial Average',
            'I:NDX': 'NASDAQ 100',
            'I:RUT': 'Russell 2000',
            'I:VIX': 'CBOE Volatility Index'
        }
        return index_names.get(symbol, symbol)

    def _process_options_data(self, contracts: List[Dict]) -> List[OptionQuote]:
        """Process raw options contract data into OptionQuote objects"""
        options = []
        
        for contract in contracts:
            try:
                exp_date = datetime.strptime(contract['expiration_date'], '%Y-%m-%d').date()
                
                option = OptionQuote(
                    symbol=contract.get('ticker', ''),
                    underlying_symbol=contract.get('underlying_ticker', ''),
                    expiration_date=exp_date,
                    strike_price=self._safe_decimal(contract.get('strike_price')),
                    option_type=contract.get('contract_type', '').upper(),
                    bid=Decimal('0'),  # Real-time pricing requires separate API call
                    ask=Decimal('0'),
                    last_price=Decimal('0'),
                    volume=0,
                    open_interest=0,
                    implied_volatility=None,
                    delta=None,
                    gamma=None,
                    theta=None,
                    vega=None,
                    rho=None,
                    timestamp=datetime.now(timezone.utc),
                    provider=self.name
                )
                
                options.append(option)
                
            except Exception as e:
                logger.warning(f"Error processing option contract: {str(e)}")
                continue
        
        return options

    # Utility methods for backward compatibility and convenience
    async def get_fundamentals(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Alias for get_financials for backward compatibility"""
        return await self.get_financials(symbol)
    
    async def get_earnings_transcript(
        self, 
        ticker: str,
        quarter: Optional[int] = None,
        year: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Earnings call transcripts are not available directly via Polygon.io
        """
        logger.warning("Earnings transcripts not directly available via Polygon.io API")
        
        return {
            "status": "not_available",
            "message": "Earnings transcripts are not directly available through Polygon.io API",
            "ticker": ticker,
            "quarter": quarter,
            "year": year,
            "provider": self.name,
            "suggestion": "Consider using alternative data sources like:",
            "alternatives": [
                "FactSet Transcripts",
                "Refinitiv (Thomson Reuters)",
                "S&P Global Market Intelligence",
                "Alpha Sense",
                "Earnings Cast"
            ]
        }

    async def batch_quotes(self, symbols: List[str]) -> Dict[str, Optional[StockQuote]]:
        """Get quotes for multiple symbols efficiently"""
        results = {}
        
        # Process in batches to respect rate limits
        batch_size = min(10, self.rate_limit // 2)  # Conservative batch size
        
        for i in range(0, len(symbols), batch_size):
            batch = symbols[i:i + batch_size]
            
            # Process batch concurrently
            tasks = [self.get_quote(symbol) for symbol in batch]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Store results
            for symbol, result in zip(batch, batch_results):
                if isinstance(result, Exception):
                    logger.warning(f"Error fetching quote for {symbol}: {str(result)}")
                    results[symbol] = None
                else:
                    results[symbol] = result
            
            # Rate limit pause between batches
            if i + batch_size < len(symbols):
                await asyncio.sleep(60 / self.rate_limit)
        
        return results

    async def get_exchange_info(self) -> List[Dict[str, Any]]:
        """Get information about supported exchanges"""
        try:
            data = await self._make_request("reference/exchanges", version='v3')
            
            if not data or 'results' not in data:
                return []
            
            return data['results']
            
        except Exception as e:
            self._log_error("get_exchange_info", f"Failed to fetch exchange info: {str(e)}")
            return []

    async def get_full_market_snapshot(self) -> List[Dict[str, Any]]:
        """Get a snapshot of the entire US stock market using v2 full market snapshot endpoint"""
        try:
            data = await self._make_request("snapshot/locale/us/markets/stocks/tickers", version='v2')
            
            if not data or 'tickers' not in data:
                return []
            
            return data['tickers']
            
        except Exception as e:
            self._log_error("get_full_market_snapshot", f"Failed to fetch full market snapshot: {str(e)}")
            return []

    async def get_unified_snapshot(self, symbols: List[str]) -> Dict[str, Any]:
        """Get unified snapshots for multiple symbols across asset classes"""
        try:
            if not symbols:
                return {}
            
            # Join symbols with commas for the API
            symbols_str = ','.join(symbols)
            params = {'tickers': symbols_str}
            
            data = await self._make_request("snapshot", params, version='v3')
            
            if not data or 'tickers' not in data:
                return {}
            
            # Convert to dict keyed by symbol
            result = {}
            for ticker_data in data['tickers']:
                symbol = ticker_data.get('ticker', '')
                if symbol:
                    result[symbol] = ticker_data
            
            return result
            
        except Exception as e:
            self._log_error("get_unified_snapshot", f"Failed to fetch unified snapshot: {str(e)}")
            return {}

    async def get_last_trade(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get the last trade for a specific symbol using v2 last trade endpoint"""
        if not symbol or not isinstance(symbol, str):
            self._log_error("Invalid Input", f"Invalid symbol: {symbol}")
            return None
        
        symbol = symbol.upper().strip()
        
        try:
            data = await self._make_request(f"last/trade/{symbol}", version='v2')
            
            if not data or 'results' not in data:
                return None
            
            result = data['results']
            return {
                'symbol': symbol,
                'price': self._safe_decimal(result.get('p', result.get('price'))),
                'size': self._safe_int(result.get('s', result.get('size'))),
                'timestamp': datetime.fromtimestamp(
                    result.get('t', result.get('timestamp', 0)) / 1000, 
                    tz=timezone.utc
                ),
                'exchange': result.get('x'),
                'conditions': result.get('c', result.get('conditions')),
                'trade_id': result.get('i', result.get('trade_id')),
                'provider': self.name
            }
            
        except Exception as e:
            self._log_error("get_last_trade", f"Failed to fetch last trade for {symbol}: {str(e)}")
            return None

    async def get_last_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get the last NBBO quote for a specific symbol using v2 last NBBO endpoint"""
        if not symbol or not isinstance(symbol, str):
            self._log_error("Invalid Input", f"Invalid symbol: {symbol}")
            return None
        
        symbol = symbol.upper().strip()
        
        try:
            data = await self._make_request(f"last/nbbo/{symbol}", version='v2')
            
            if not data or 'results' not in data:
                return None
            
            result = data['results']
            return {
                'symbol': symbol,
                'bid_price': self._safe_decimal(result.get('bid_price', result.get('p'))),
                'bid_size': self._safe_int(result.get('bid_size', result.get('s'))),
                'ask_price': self._safe_decimal(result.get('ask_price', result.get('P'))),
                'ask_size': self._safe_int(result.get('ask_size', result.get('S'))),
                'timestamp': datetime.fromtimestamp(
                    result.get('t', result.get('timestamp', 0)) / 1000, 
                    tz=timezone.utc
                ),
                'bid_exchange': result.get('bid_exchange', result.get('x')),
                'ask_exchange': result.get('ask_exchange', result.get('X')),
                'provider': self.name
            }
            
        except Exception as e:
            self._log_error("get_last_quote", f"Failed to fetch last quote for {symbol}: {str(e)}")
            return None

    async def get_daily_open_close(self, symbol: str, date: date) -> Optional[Dict[str, Any]]:
        """Get the daily open, high, low, close for a specific symbol and date"""
        if not symbol or not isinstance(symbol, str):
            self._log_error("Invalid Input", f"Invalid symbol: {symbol}")
            return None
        
        symbol = symbol.upper().strip()
        
        try:
            endpoint = f"open-close/{symbol}/{date.strftime('%Y-%m-%d')}"
            data = await self._make_request(endpoint, version='v1')
            
            if not data:
                return None
            
            return {
                'symbol': symbol,
                'date': date,
                'open': self._safe_decimal(data.get('open')),
                'high': self._safe_decimal(data.get('high')),
                'low': self._safe_decimal(data.get('low')),
                'close': self._safe_decimal(data.get('close')),
                'volume': self._safe_int(data.get('volume')),
                'after_hours': self._safe_decimal(data.get('afterHours')),
                'pre_market': self._safe_decimal(data.get('preMarket')),
                'provider': self.name
            }
            
        except Exception as e:
            self._log_error("get_daily_open_close", f"Failed to fetch daily open/close for {symbol}: {str(e)}")
            return None

    async def get_gainers_losers(self, direction: str = 'gainers', limit: int = 20) -> List[Dict[str, Any]]:
        """Get top gainers or losers for the day"""
        try:
            if direction not in ['gainers', 'losers']:
                direction = 'gainers'
            
            params = {'limit': max(1, min(1000, limit))}
            data = await self._make_request(f"snapshot/locale/us/markets/stocks/{direction}", params, version='v2')
            
            if not data or 'tickers' not in data:
                return []
            
            return data['tickers']
            
        except Exception as e:
            self._log_error("get_gainers_losers", f"Failed to fetch {direction}: {str(e)}")
            return []

    async def get_conditions(self, asset_class: str = 'stocks', tick_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get reference data for trade/quote conditions (v3/reference/conditions)"""
        try:
            params = {'asset_class': asset_class}
            if tick_type:
                params['type'] = tick_type
            
            data = await self._make_request("reference/conditions", params, version='v3')
            
            if not data or 'results' not in data:
                return []
            
            return data['results']
            
        except Exception as e:
            self._log_error("get_conditions", f"Failed to fetch conditions for {asset_class}: {str(e)}")
            return []

    async def get_ticker_types(self) -> List[Dict[str, Any]]:
        """Get all available ticker types"""
        try:
            data = await self._make_request("reference/tickers/types", version='v3')
            
            if not data or 'results' not in data:
                return []
            
            return data['results']
            
        except Exception as e:
            self._log_error("get_ticker_types", f"Failed to fetch ticker types: {str(e)}")
            return []

    async def get_option_contract_details(self, option_symbol: str) -> Optional[Dict[str, Any]]:
        """Get details for a specific options contract"""
        if not option_symbol or not isinstance(option_symbol, str):
            self._log_error("Invalid Input", f"Invalid option symbol: {option_symbol}")
            return None
        
        option_symbol = option_symbol.upper().strip()
        
        try:
            data = await self._make_request(f"reference/options/contracts/{option_symbol}", version='v3')
            
            if not data or 'results' not in data:
                return None
            
            result = data['results']
            return {
                'contract_symbol': result.get('ticker'),
                'underlying_symbol': result.get('underlying_ticker'),
                'expiration_date': result.get('expiration_date'),
                'strike_price': self._safe_decimal(result.get('strike_price')),
                'contract_type': result.get('contract_type'),
                'exercise_style': result.get('exercise_style'),
                'shares_per_contract': self._safe_int(result.get('shares_per_contract')),
                'primary_exchange': result.get('primary_exchange'),
                'cfi': result.get('cfi'),
                'provider': self.name
            }
            
        except Exception as e:
            self._log_error("get_option_contract_details", f"Failed to fetch option contract details for {option_symbol}: {str(e)}")
            return None

    async def get_market_conditions(self) -> Dict[str, Any]:
        """Get current market conditions summary"""
        try:
            # Get market status
            market_status = await self.get_market_status()
            
            # Get major indices
            indices = await self.get_market_indices()
            
            # Get VIX (volatility index) if available
            vix_data = None
            for index in indices:
                if index['symbol'] == 'I:VIX':
                    vix_data = index['data']
                    break
            
            return {
                'market_status': market_status,
                'major_indices': indices,
                'volatility_index': vix_data,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'provider': self.name
            }
            
        except Exception as e:
            self._log_error("get_market_conditions", f"Failed to get market conditions: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'provider': self.name
            }