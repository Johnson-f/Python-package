"""Alpha Vantage API Provider Implementation - Complete Version"""

import aiohttp
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from decimal import Decimal
from ..base import (
    MarketDataProvider, 
    StockQuote, 
    HistoricalPrice, 
    OptionQuote, 
    CompanyInfo,
    EconomicEvent
)


class AlphaVantageProvider(MarketDataProvider):
    """Alpha Vantage API implementation with all available endpoints"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, "AlphaVantage")
        self.base_url = "https://www.alphavantage.co/query"
        self.analytics_url = "https://alphavantageapi.co"
    
    def _standardize_interval(self, interval: str) -> str:
        """Convert interval to Alpha Vantage format"""
        interval_map = {
            "1min": "1min",
            "5min": "5min", 
            "15min": "15min",
            "30min": "30min",
            "60min": "60min",
            "daily": "DAILY",
            "weekly": "WEEKLY",
            "monthly": "MONTHLY"
        }
        return interval_map.get(interval.lower(), "DAILY")
    
    async def _make_request(self, params: Dict[str, Any], base_url: Optional[str] = None) -> Optional[Dict]:
        """Make API request to Alpha Vantage"""
        params['apikey'] = self.api_key
        url = base_url or self.base_url
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "Error Message" in data or "Note" in data:
                            error_msg = data.get("Error Message", data.get("Note"))
                            self._log_error("API Request", Exception(error_msg))
                            return None
                        return data
                    else:
                        self._log_error("API Request", Exception(f"HTTP {response.status}"))
                        return None
        except Exception as e:
            self._log_error("_make_request", e)
            return None
    
    def _safe_decimal(self, value: str, default: Decimal = Decimal('0')) -> Decimal:
        """Safely convert string to Decimal"""
        try:
            if not value or value == "None":
                return default
            # Remove % if present
            clean_value = value.rstrip('%') if isinstance(value, str) else str(value)
            return Decimal(clean_value)
        except (ValueError, TypeError, AttributeError):
            return default
    
    def _safe_int(self, value: str, default: int = 0) -> int:
        """Safely convert string to int"""
        try:
            if not value or value == "None":
                return default
            return int(float(value))  # Handle cases like "1.0"
        except (ValueError, TypeError):
            return default
    
    # Core Time Series Data APIs
    async def get_quote(self, symbol: str) -> Optional[StockQuote]:
        """Get current quote using GLOBAL_QUOTE function"""
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol
        }
        
        data = await self._make_request(params)
        if not data or 'Global Quote' not in data:
            return None
        
        try:
            quote_data = data['Global Quote']
            
            if not quote_data.get('05. price'):
                return None
            
            return StockQuote(
                symbol=symbol,
                price=self._safe_decimal(quote_data.get('05. price', '0')),
                change=self._safe_decimal(quote_data.get('09. change', '0')),
                change_percent=self._safe_decimal(quote_data.get('10. change percent', '0')),
                volume=self._safe_int(quote_data.get('06. volume', '0')),
                open=self._safe_decimal(quote_data.get('02. open', '0')),
                high=self._safe_decimal(quote_data.get('03. high', '0')),
                low=self._safe_decimal(quote_data.get('04. low', '0')),
                previous_close=self._safe_decimal(quote_data.get('08. previous close', '0')),
                timestamp=datetime.now(),
                provider=self.name
            )
        except Exception as e:
            self._log_error("get_quote", e)
            return None
    
    async def get_realtime_bulk_quotes(self, symbols: List[str]) -> Optional[List[StockQuote]]:
        """Get realtime bulk quotes for up to 100 symbols (Premium feature)"""
        if len(symbols) > 100:
            symbols = symbols[:100]
            
        params = {
            'function': 'REALTIME_BULK_QUOTES',
            'symbol': ','.join(symbols)
        }
        
        data = await self._make_request(params)
        if not data or 'stock_quotes' not in data:
            return None
            
        quotes = []
        for quote_data in data['stock_quotes']:
            try:
                quotes.append(StockQuote(
                    symbol=quote_data.get('symbol', ''),
                    price=self._safe_decimal(quote_data.get('price', '0')),
                    change=self._safe_decimal(quote_data.get('change', '0')),
                    change_percent=self._safe_decimal(quote_data.get('change_percent', '0')),
                    volume=self._safe_int(quote_data.get('volume', '0')),
                    open=self._safe_decimal(quote_data.get('open', '0')),
                    high=self._safe_decimal(quote_data.get('high', '0')),
                    low=self._safe_decimal(quote_data.get('low', '0')),
                    previous_close=self._safe_decimal(quote_data.get('previous_close', '0')),
                    timestamp=datetime.now(),
                    provider=self.name
                ))
            except Exception as e:
                self._log_error(f"parse_bulk_quote_{quote_data.get('symbol', 'unknown')}", e)
                continue
                
        return quotes
    
    async def get_historical(
        self, 
        symbol: str, 
        start_date: date, 
        end_date: date,
        interval: str = "1d"
    ) -> Optional[List[HistoricalPrice]]:
        """Get historical prices using TIME_SERIES_DAILY_ADJUSTED"""
        params = {
            'function': 'TIME_SERIES_DAILY_ADJUSTED',
            'symbol': symbol,
            'outputsize': 'full'
        }
        
        data = await self._make_request(params)
        if not data or 'Time Series (Daily)' not in data:
            return None
        
        try:
            time_series = data['Time Series (Daily)']
            prices = []
            
            for date_str, values in time_series.items():
                try:
                    price_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    
                    if not (start_date <= price_date <= end_date):
                        continue
                    
                    prices.append(HistoricalPrice(
                        symbol=symbol,
                        date=price_date,
                        open=self._safe_decimal(values.get('1. open', '0')),
                        high=self._safe_decimal(values.get('2. high', '0')),
                        low=self._safe_decimal(values.get('3. low', '0')),
                        close=self._safe_decimal(values.get('4. close', '0')),
                        volume=self._safe_int(values.get('6. volume', '0')),
                        adjusted_close=self._safe_decimal(values.get('5. adjusted close', '0')),
                        dividend=self._safe_decimal(values.get('7. dividend amount', '0')),
                        split=self._safe_decimal(values.get('8. split coefficient', '1')),
                        provider=self.name
                    ))
                except Exception as e:
                    self._log_error(f"parse_historical_date_{date_str}", e)
                    continue
            
            return sorted(prices, key=lambda x: x.date)
        except Exception as e:
            self._log_error("get_historical", e)
            return None
    
    async def get_weekly_data(self, symbol: str, adjusted: bool = True) -> Optional[Dict[str, Any]]:
        """Get weekly time series data"""
        function = 'TIME_SERIES_WEEKLY_ADJUSTED' if adjusted else 'TIME_SERIES_WEEKLY'
        params = {
            'function': function,
            'symbol': symbol
        }
        
        return await self._make_request(params)
    
    async def get_monthly_data(self, symbol: str, adjusted: bool = True) -> Optional[Dict[str, Any]]:
        """Get monthly time series data"""
        function = 'TIME_SERIES_MONTHLY_ADJUSTED' if adjusted else 'TIME_SERIES_MONTHLY'
        params = {
            'function': function,
            'symbol': symbol
        }
        
        return await self._make_request(params)
    
    async def get_intraday(
        self, 
        symbol: str, 
        interval: str = "5min",
        month: Optional[str] = None,
        extended_hours: bool = True,
        adjusted: bool = True,
        outputsize: str = "compact"
    ) -> Optional[List[HistoricalPrice]]:
        """Get intraday prices with full Alpha Vantage parameters"""
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': interval,
            'adjusted': str(adjusted).lower(),
            'extended_hours': str(extended_hours).lower(),
            'outputsize': outputsize
        }
        
        if month:
            params['month'] = month
        
        data = await self._make_request(params)
        if not data:
            return None
        
        try:
            time_series_key = f'Time Series ({interval})'
            if time_series_key not in data:
                return None
            
            time_series = data[time_series_key]
            prices = []
            
            for datetime_str, values in time_series.items():
                try:
                    price_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                    
                    prices.append(HistoricalPrice(
                        symbol=symbol,
                        date=price_datetime.date(),
                        open=self._safe_decimal(values.get('1. open', '0')),
                        high=self._safe_decimal(values.get('2. high', '0')),
                        low=self._safe_decimal(values.get('3. low', '0')),
                        close=self._safe_decimal(values.get('4. close', '0')),
                        volume=self._safe_int(values.get('5. volume', '0')),
                        provider=self.name
                    ))
                except Exception as e:
                    self._log_error(f"parse_intraday_datetime_{datetime_str}", e)
                    continue
            
            return sorted(prices, key=lambda x: x.date, reverse=True)
        except Exception as e:
            self._log_error("get_intraday", e)
            return None
    
    # Options Data APIs
    async def get_realtime_options(
        self, 
        symbol: str, 
        require_greeks: bool = False,
        contract: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get realtime options data (Premium feature)"""
        params = {
            'function': 'REALTIME_OPTIONS',
            'symbol': symbol,
            'require_greeks': str(require_greeks).lower()
        }
        
        if contract:
            params['contract'] = contract
            
        return await self._make_request(params)
    
    async def get_historical_options(
        self, 
        symbol: str, 
        date: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get historical options chain for a specific date"""
        params = {
            'function': 'HISTORICAL_OPTIONS',
            'symbol': symbol
        }
        
        if date:
            params['date'] = date
            
        return await self._make_request(params)
    
    async def get_options_chain(
        self, 
        symbol: str, 
        expiration: Optional[date] = None
    ) -> Optional[List[OptionQuote]]:
        """Get options chain data using realtime options endpoint"""
        options_data = await self.get_realtime_options(symbol, require_greeks=True)
        
        if not options_data or 'data' not in options_data:
            return None
            
        try:
            option_quotes = []
            for option in options_data['data']:
                option_quotes.append(OptionQuote(
                    symbol=symbol,
                    contract_symbol=option.get('contractID', ''),
                    option_type=option.get('type', ''),
                    strike=self._safe_decimal(option.get('strike', '0')),
                    expiration=datetime.strptime(option.get('expiration', ''), '%Y-%m-%d').date(),
                    bid=self._safe_decimal(option.get('bid', '0')),
                    ask=self._safe_decimal(option.get('ask', '0')),
                    last_price=self._safe_decimal(option.get('lastPrice', '0')),
                    volume=self._safe_int(option.get('volume', '0')),
                    open_interest=self._safe_int(option.get('openInterest', '0')),
                    implied_volatility=self._safe_decimal(option.get('impliedVolatility', '0')),
                    delta=self._safe_decimal(option.get('delta', '0')),
                    gamma=self._safe_decimal(option.get('gamma', '0')),
                    theta=self._safe_decimal(option.get('theta', '0')),
                    vega=self._safe_decimal(option.get('vega', '0')),
                    rho=self._safe_decimal(option.get('rho', '0')),
                    provider=self.name
                ))
            
            return option_quotes
        except Exception as e:
            self._log_error("get_options_chain", e)
            return None
    
    # Utility Functions
    async def symbol_search(self, keywords: str) -> Optional[Dict[str, Any]]:
        """Search for symbols based on keywords"""
        params = {
            'function': 'SYMBOL_SEARCH',
            'keywords': keywords
        }
        
        return await self._make_request(params)
    
    async def get_market_status(self) -> Optional[Dict[str, Any]]:
        """Get global market open/close status"""
        params = {
            'function': 'MARKET_STATUS'
        }
        
        return await self._make_request(params)
    
    # Alpha Intelligence APIs
    async def get_news(
        self, 
        symbol: Optional[str] = None,
        topics: Optional[List[str]] = None,
        time_from: Optional[str] = None,
        time_to: Optional[str] = None,
        sort: str = "LATEST",
        limit: int = 50
    ) -> Optional[List[Dict[str, Any]]]:
        """Get news & sentiment data"""
        params = {
            'function': 'NEWS_SENTIMENT',
            'sort': sort,
            'limit': min(limit, 1000)
        }
        
        if symbol:
            params['tickers'] = symbol
        if topics:
            params['topics'] = ','.join(topics)
        if time_from:
            params['time_from'] = time_from
        if time_to:
            params['time_to'] = time_to
            
        data = await self._make_request(params)
        if not data or 'feed' not in data:
            return None
            
        return data['feed'][:limit]
    
    async def get_earnings_call_transcript(self, symbol: str, quarter: str) -> Optional[Dict[str, Any]]:
        """Get earnings call transcript for a specific quarter"""
        params = {
            'function': 'EARNINGS_CALL_TRANSCRIPT',
            'symbol': symbol,
            'quarter': quarter  # Format: YYYYQM (e.g., 2024Q1)
        }
        
        return await self._make_request(params)
    
    async def get_top_gainers_losers(self) -> Optional[Dict[str, Any]]:
        """Get top gainers, losers, and most active tickers"""
        params = {
            'function': 'TOP_GAINERS_LOSERS'
        }
        
        return await self._make_request(params)
    
    async def get_insider_transactions(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get insider transactions for a symbol"""
        params = {
            'function': 'INSIDER_TRANSACTIONS',
            'symbol': symbol
        }
        
        return await self._make_request(params)
    
    # Advanced Analytics APIs
    async def get_analytics_fixed_window(
        self,
        symbols: List[str],
        range_start: Optional[str] = None,
        range_end: Optional[str] = None,
        interval: str = "DAILY",
        ohlc: str = "close",
        calculations: List[str] = ["MEAN", "STDDEV"]
    ) -> Optional[Dict[str, Any]]:
        """Get advanced analytics for fixed window"""
        params = {
            'function': 'ANALYTICS_FIXED_WINDOW',
            'SYMBOLS': ','.join(symbols[:50]),  # Max 50 for premium, 5 for free
            'INTERVAL': interval,
            'OHLC': ohlc,
            'CALCULATIONS': ','.join(calculations)
        }
        
        if range_start:
            params['RANGE'] = range_start
        if range_end:
            params['RANGE'] = range_end  # Second RANGE parameter
            
        return await self._make_request(params, f"{self.analytics_url}/timeseries/analytics")
    
    async def get_analytics_sliding_window(
        self,
        symbols: List[str],
        window_size: int,
        range_param: Optional[str] = None,
        interval: str = "DAILY",
        ohlc: str = "close",
        calculations: List[str] = ["MEAN"]
    ) -> Optional[Dict[str, Any]]:
        """Get advanced analytics for sliding window"""
        params = {
            'function': 'ANALYTICS_SLIDING_WINDOW',
            'SYMBOLS': ','.join(symbols[:50]),
            'WINDOW_SIZE': window_size,
            'INTERVAL': interval,
            'OHLC': ohlc,
            'CALCULATIONS': ','.join(calculations)
        }
        
        if range_param:
            params['RANGE'] = range_param
            
        return await self._make_request(params, f"{self.analytics_url}/timeseries/running_analytics")
    
    # Fundamental Data APIs
    async def get_company_info(self, symbol: str) -> Optional[CompanyInfo]:
        """Get company overview information"""
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol
        }
        
        data = await self._make_request(params)
        if not data or 'Symbol' not in data:
            return None
        
        try:
            def clean_address(*parts):
                cleaned = [part.strip() for part in parts if part and part.strip() and part.strip() != "None"]
                return ", ".join(cleaned) if cleaned else None
            
            return CompanyInfo(
                symbol=symbol,
                name=data.get('Name', ''),
                exchange=data.get('Exchange'),
                sector=data.get('Sector'),
                industry=data.get('Industry'),
                market_cap=self._safe_int(data.get('MarketCapitalization', '0')) or None,
                employees=self._safe_int(data.get('FullTimeEmployees', '0')) or None,
                description=data.get('Description'),
                website=data.get('OfficialSite'),
                ceo=data.get('CEO'),
                headquarters=clean_address(
                    data.get('Address', ''),
                    data.get('City', ''),
                    data.get('Country', '')
                ),
                founded=data.get('FiscalYearEnd'),
                pe_ratio=self._safe_decimal(data.get('PERatio', '0')) or None,
                pb_ratio=self._safe_decimal(data.get('PriceToBookRatio', '0')) or None,
                dividend_yield=self._safe_decimal(data.get('DividendYield', '0')) or None,
                revenue=self._safe_int(data.get('RevenueTTM', '0')) or None,
                net_income=self._safe_int(data.get('NetIncomeTTM', '0')) or None,
                provider=self.name
            )
        except Exception as e:
            self._log_error("get_company_info", e)
            return None
    
    async def get_income_statement(
        self, 
        symbol: str,
        period: str = "annual"  # "annual" or "quarterly"
    ) -> Optional[Dict[str, Any]]:
        """Get income statement data"""
        params = {
            'function': 'INCOME_STATEMENT',
            'symbol': symbol,
            'period': period
        }
        
        return await self._make_request(params)
    
    async def get_balance_sheet(
        self, 
        symbol: str,
        period: str = "annual"
    ) -> Optional[Dict[str, Any]]:
        """Get balance sheet data"""
        params = {
            'function': 'BALANCE_SHEET',
            'symbol': symbol,
            'period': period
        }
        
        return await self._make_request(params)
    
    async def get_cash_flow(
        self, 
        symbol: str,
        period: str = "annual"
    ) -> Optional[Dict[str, Any]]:
        """Get cash flow statement data"""
        params = {
            'function': 'CASH_FLOW',
            'symbol': symbol,
            'period': period
        }
        
        return await self._make_request(params)
    
    async def get_earnings(
        self, 
        symbol: str,
        horizon: str = 'quarterly',
        include_upcoming: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get earnings data"""
        params = {
            'function': 'EARNINGS',
            'symbol': symbol
        }
        
        return await self._make_request(params)
    
    async def get_fundamentals(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get fundamental data from OVERVIEW function"""
        return await self.get_company_overview(symbol)
    
    async def get_company_overview(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get company overview (alias for fundamentals)"""
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol
        }
        
        data = await self._make_request(params)
        if not data:
            return None
        
        # Return structured fundamental metrics
        fundamentals = {
            'symbol': symbol,
            'provider': self.name,
            'pe_ratio': self._safe_decimal(data.get('PERatio', '0')) or None,
            'peg_ratio': self._safe_decimal(data.get('PEGRatio', '0')) or None,
            'book_value': self._safe_decimal(data.get('BookValue', '0')) or None,
            'dividend_yield': self._safe_decimal(data.get('DividendYield', '0')) or None,
            'eps': self._safe_decimal(data.get('EPS', '0')) or None,
            'revenue_per_share': self._safe_decimal(data.get('RevenuePerShareTTM', '0')) or None,
            'profit_margin': self._safe_decimal(data.get('ProfitMargin', '0')) or None,
            'operating_margin': self._safe_decimal(data.get('OperatingMarginTTM', '0')) or None,
            'return_on_assets': self._safe_decimal(data.get('ReturnOnAssetsTTM', '0')) or None,
            'return_on_equity': self._safe_decimal(data.get('ReturnOnEquityTTM', '0')) or None,
            'revenue': self._safe_decimal(data.get('RevenueTTM', '0')) or None,
            'gross_profit': self._safe_decimal(data.get('GrossProfitTTM', '0')) or None,
            'ebitda': self._safe_decimal(data.get('EBITDA', '0')) or None,
            'beta': self._safe_decimal(data.get('Beta', '0')) or None,
            '52_week_high': self._safe_decimal(data.get('52WeekHigh', '0')) or None,
            '52_week_low': self._safe_decimal(data.get('52WeekLow', '0')) or None,
            '50_day_ma': self._safe_decimal(data.get('50DayMovingAverage', '0')) or None,
            '200_day_ma': self._safe_decimal(data.get('200DayMovingAverage', '0')) or None
        }
        
        return fundamentals
    
    # Currency APIs
    async def get_fx_intraday(
        self, 
        from_symbol: str, 
        to_symbol: str,
        interval: str = "5min",
        outputsize: str = "compact"
    ) -> Optional[Dict[str, Any]]:
        """Get intraday forex data"""
        params = {
            'function': 'FX_INTRADAY',
            'from_symbol': from_symbol,
            'to_symbol': to_symbol,
            'interval': interval,
            'outputsize': outputsize
        }
        
        return await self._make_request(params)
    
    async def get_fx_daily(
        self, 
        from_symbol: str, 
        to_symbol: str,
        outputsize: str = "compact"
    ) -> Optional[Dict[str, Any]]:
        """Get daily forex data"""
        params = {
            'function': 'FX_DAILY',
            'from_symbol': from_symbol,
            'to_symbol': to_symbol,
            'outputsize': outputsize
        }
        
        return await self._make_request(params)
    
    async def get_currency_exchange_rate(
        self, 
        from_currency: str, 
        to_currency: str
    ) -> Optional[Dict[str, Any]]:
        """Get current currency exchange rate"""
        params = {
            'function': 'CURRENCY_EXCHANGE_RATE',
            'from_currency': from_currency,
            'to_currency': to_currency
        }
        
        return await self._make_request(params)
    
    # Cryptocurrency APIs
    async def get_crypto_intraday(
        self,
        symbol: str,
        market: str = "USD",
        interval: str = "5min"
    ) -> Optional[Dict[str, Any]]:
        """Get intraday cryptocurrency data"""
        params = {
            'function': 'CRYPTO_INTRADAY',
            'symbol': symbol,
            'market': market,
            'interval': interval
        }
        
        return await self._make_request(params)
    
    async def get_crypto_daily(
        self,
        symbol: str,
        market: str = "USD"
    ) -> Optional[Dict[str, Any]]:
        """Get daily cryptocurrency data"""
        params = {
            'function': 'DIGITAL_CURRENCY_DAILY',
            'symbol': symbol,
            'market': market
        }
        
        return await self._make_request(params)
    
    # Commodities APIs
    async def get_commodity_data(self, function: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Get commodity data (WTI, BRENT, NATURAL_GAS)"""
        params = {
            'function': function.upper(),
            **kwargs
        }
        
        return await self._make_request(params)
    
    # Economic Indicators APIs
    async def get_economic_indicator(
        self, 
        indicator: str,
        interval: str = "monthly"
    ) -> Optional[Dict[str, Any]]:
        """Get individual economic indicators"""
        # Map common indicator names to Alpha Vantage functions
        indicator_map = {
            'gdp': 'REAL_GDP',
            'inflation': 'INFLATION',
            'unemployment': 'UNEMPLOYMENT',
            'fed_funds_rate': 'FEDERAL_FUNDS_RATE',
            'cpi': 'CPI',
            'treasury_yield': 'TREASURY_YIELD',
            'retail_sales': 'RETAIL_SALES',
            'nonfarm_payroll': 'NONFARM_PAYROLL'
        }
        
        function = indicator_map.get(indicator.lower(), indicator.upper())
        
        params = {
            'function': function,
            'interval': interval
        }
        
        return await self._make_request(params)
    
    async def get_economic_events(
        self,
        countries: Optional[List[str]] = None,
        importance: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 50
    ) -> List[EconomicEvent]:
        """Alpha Vantage doesn't provide an economic calendar endpoint"""
        self._log_info("Alpha Vantage does not provide an economic calendar endpoint")
        self._log_info("Use individual economic indicators like REAL_GDP, INFLATION, UNEMPLOYMENT, etc.")
        return []
    
    # Technical Indicators APIs
    async def get_technical_indicators(
        self, 
        symbol: str, 
        indicator: str,
        interval: str = "daily",
        time_period: int = 20,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Get technical indicators"""
        # Map indicator names to Alpha Vantage function names
        indicator_map = {
            'sma': 'SMA',
            'ema': 'EMA',
            'wma': 'WMA',
            'dema': 'DEMA',
            'tema': 'TEMA',
            'trima': 'TRIMA',
            'kama': 'KAMA',
            'mama': 'MAMA',
            'vwap': 'VWAP',
            'macd': 'MACD',
            'macdext': 'MACDEXT',
            'stoch': 'STOCH',
            'stochf': 'STOCHF',
            'rsi': 'RSI',
            'stochrsi': 'STOCHRSI',
            'willr': 'WILLR',
            'adx': 'ADX',
            'adxr': 'ADXR',
            'apo': 'APO',
            'ppo': 'PPO',
            'mom': 'MOM',
            'bop': 'BOP',
            'cci': 'CCI',
            'cmo': 'CMO',
            'roc': 'ROC',
            'rocr': 'ROCR',
            'aroon': 'AROON',
            'aroonosc': 'AROONOSC',
            'mfi': 'MFI',
            'trix': 'TRIX',
            'ultosc': 'ULTOSC',
            'dx': 'DX',
            'minus_di': 'MINUS_DI',
            'plus_di': 'PLUS_DI',
            'minus_dm': 'MINUS_DM',
            'plus_dm': 'PLUS_DM',
            'bbands': 'BBANDS',
            'midpoint': 'MIDPOINT',
            'midprice': 'MIDPRICE',
            'sar': 'SAR',
            'trange': 'TRANGE',
            'atr': 'ATR',
            'natr': 'NATR',
            'ad': 'AD',
            'adosc': 'ADOSC',
            'obv': 'OBV',
            'ht_trendline': 'HT_TRENDLINE',
            'ht_sine': 'HT_SINE',
            'ht_trendmode': 'HT_TRENDMODE',
            'ht_dcperiod': 'HT_DCPERIOD',
            'ht_dcphase': 'HT_DCPHASE',
            'ht_phasor': 'HT_PHASOR'
        }
        
        av_function = indicator_map.get(indicator.lower())
        if not av_function:
            self._log_error("get_technical_indicators", Exception(f"Unsupported indicator: {indicator}"))
            return None
        
        params = {
            'function': av_function,
            'symbol': symbol,
            'interval': self._standardize_interval(interval),
            'time_period': time_period,
            'series_type': kwargs.get('series_type', 'close')
        }
        
        # Add any additional parameters specific to certain indicators
        if indicator.lower() == 'macd':
            params.update({
                'fastperiod': kwargs.get('fastperiod', 12),
                'slowperiod': kwargs.get('slowperiod', 26),
                'signalperiod': kwargs.get('signalperiod', 9)
            })
        elif indicator.lower() == 'bbands':
            params.update({
                'nbdevup': kwargs.get('nbdevup', 2),
                'nbdevdn': kwargs.get('nbdevdn', 2),
                'matype': kwargs.get('matype', 0)
            })
        elif indicator.lower() == 'stoch':
            params.update({
                'fastkperiod': kwargs.get('fastkperiod', 5),
                'slowkperiod': kwargs.get('slowkperiod', 3),
                'slowdperiod': kwargs.get('slowdperiod', 3),
                'slowkmatype': kwargs.get('slowkmatype', 0),
                'slowdmatype': kwargs.get('slowdmatype', 0)
            })
        elif indicator.lower() == 'aroon':
            params.update({
                'time_period': kwargs.get('time_period', 14)
            })
        elif indicator.lower() == 'ultosc':
            params.update({
                'timeperiod1': kwargs.get('timeperiod1', 7),
                'timeperiod2': kwargs.get('timeperiod2', 14),
                'timeperiod3': kwargs.get('timeperiod3', 28)
            })
        
        return await self._make_request(params)
    
    # Additional Financial Statement APIs
    async def get_listing_status(self, date: Optional[str] = None, state: str = "active") -> Optional[Dict[str, Any]]:
        """Get listing and delisting information"""
        params = {
            'function': 'LISTING_STATUS',
            'state': state  # 'active' or 'delisted'
        }
        
        if date:
            params['date'] = date
            
        return await self._make_request(params)
    
    async def get_earnings_calendar(self, horizon: str = "3month") -> Optional[Dict[str, Any]]:
        """Get earnings calendar (Premium feature)"""
        params = {
            'function': 'EARNINGS_CALENDAR',
            'horizon': horizon
        }
        
        return await self._make_request(params)
    
    async def get_ipo_calendar(self) -> Optional[Dict[str, Any]]:
        """Get IPO calendar (Premium feature)"""
        params = {
            'function': 'IPO_CALENDAR'
        }
        
        return await self._make_request(params)
    
    # Sector Performance APIs
    async def get_sector_performance(self) -> Optional[Dict[str, Any]]:
        """Get sector performance data"""
        params = {
            'function': 'SECTOR'
        }
        
        return await self._make_request(params)
    
    # Commodity APIs - Specific functions
    async def get_wti_crude(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get WTI crude oil prices"""
        return await self.get_commodity_data('WTI', interval=interval)
    
    async def get_brent_crude(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get Brent crude oil prices"""
        return await self.get_commodity_data('BRENT', interval=interval)
    
    async def get_natural_gas(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get natural gas prices"""
        return await self.get_commodity_data('NATURAL_GAS', interval=interval)
    
    async def get_copper(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get copper prices"""
        return await self.get_commodity_data('COPPER', interval=interval)
    
    async def get_aluminum(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get aluminum prices"""
        return await self.get_commodity_data('ALUMINUM', interval=interval)
    
    async def get_wheat(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get wheat prices"""
        return await self.get_commodity_data('WHEAT', interval=interval)
    
    async def get_corn(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get corn prices"""
        return await self.get_commodity_data('CORN', interval=interval)
    
    async def get_cotton(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get cotton prices"""
        return await self.get_commodity_data('COTTON', interval=interval)
    
    async def get_sugar(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get sugar prices"""
        return await self.get_commodity_data('SUGAR', interval=interval)
    
    async def get_coffee(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get coffee prices"""
        return await self.get_commodity_data('COFFEE', interval=interval)
    
    async def get_all_commodities(self, interval: str = "monthly") -> Dict[str, Any]:
        """Get all available commodity data"""
        commodities = ['WTI', 'BRENT', 'NATURAL_GAS', 'COPPER', 'ALUMINUM', 
                      'WHEAT', 'CORN', 'COTTON', 'SUGAR', 'COFFEE']
        
        results = {}
        for commodity in commodities:
            try:
                data = await self.get_commodity_data(commodity, interval=interval)
                if data:
                    results[commodity.lower()] = data
            except Exception as e:
                self._log_error(f"get_{commodity.lower()}", e)
                
        return results
    
    # Economic Indicators - Specific functions
    async def get_real_gdp(self, interval: str = "annual") -> Optional[Dict[str, Any]]:
        """Get Real GDP data"""
        return await self.get_economic_indicator('REAL_GDP', interval)
    
    async def get_real_gdp_per_capita(self) -> Optional[Dict[str, Any]]:
        """Get Real GDP per capita"""
        return await self.get_economic_indicator('REAL_GDP_PER_CAPITA')
    
    async def get_treasury_yield(self, interval: str = "monthly", maturity: str = "10year") -> Optional[Dict[str, Any]]:
        """Get Treasury yield data"""
        params = {
            'function': 'TREASURY_YIELD',
            'interval': interval,
            'maturity': maturity  # 3month, 2year, 5year, 7year, 10year, 30year
        }
        
        return await self._make_request(params)
    
    async def get_federal_funds_rate(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get Federal Funds Rate"""
        return await self.get_economic_indicator('FEDERAL_FUNDS_RATE', interval)
    
    async def get_cpi(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get Consumer Price Index"""
        return await self.get_economic_indicator('CPI', interval)
    
    async def get_inflation(self) -> Optional[Dict[str, Any]]:
        """Get inflation data"""
        return await self.get_economic_indicator('INFLATION')
    
    async def get_retail_sales(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get retail sales data"""
        return await self.get_economic_indicator('RETAIL_SALES', interval)
    
    async def get_durables(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get durable goods orders"""
        return await self.get_economic_indicator('DURABLES', interval)
    
    async def get_unemployment_rate(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get unemployment rate"""
        return await self.get_economic_indicator('UNEMPLOYMENT', interval)
    
    async def get_nonfarm_payroll(self, interval: str = "monthly") -> Optional[Dict[str, Any]]:
        """Get nonfarm payroll data"""
        return await self.get_economic_indicator('NONFARM_PAYROLL', interval)
    
    # ETF and Mutual Fund APIs
    async def get_etf_profile(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get ETF profile information"""
        params = {
            'function': 'ETF_PROFILE',
            'symbol': symbol
        }
        
        return await self._make_request(params)
    
    async def get_mutual_fund_profile(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get mutual fund profile"""
        params = {
            'function': 'MUTUAL_FUND_PROFILE',
            'symbol': symbol
        }
        
        return await self._make_request(params)
    
    # Batch Processing Helper Methods
    async def get_multiple_quotes(self, symbols: List[str]) -> List[Optional[StockQuote]]:
        """Get quotes for multiple symbols"""
        quotes = []
        
        # Use bulk quotes if available (premium) and symbols <= 100
        if len(symbols) <= 100:
            try:
                bulk_quotes = await self.get_realtime_bulk_quotes(symbols)
                if bulk_quotes:
                    return bulk_quotes
            except Exception as e:
                self._log_error("get_multiple_quotes_bulk", e)
        
        # Fallback to individual requests
        for symbol in symbols:
            try:
                quote = await self.get_quote(symbol)
                quotes.append(quote)
            except Exception as e:
                self._log_error(f"get_quote_{symbol}", e)
                quotes.append(None)
                
        return quotes
    
    async def get_multiple_company_info(self, symbols: List[str]) -> List[Optional[CompanyInfo]]:
        """Get company info for multiple symbols"""
        companies = []
        
        for symbol in symbols:
            try:
                company = await self.get_company_info(symbol)
                companies.append(company)
            except Exception as e:
                self._log_error(f"get_company_info_{symbol}", e)
                companies.append(None)
                
        return companies
    
    # Helper methods for data validation and formatting
    def _validate_symbol(self, symbol: str) -> bool:
        """Validate symbol format"""
        if not symbol or len(symbol) > 20:
            return False
        return symbol.replace('.', '').replace('-', '').isalnum()
    
    def _format_date_range(self, start_date: date, end_date: date) -> tuple:
        """Format date range for API requests"""
        return (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    
    # Legacy method aliases for backward compatibility
    async def get_earnings_transcript(self, symbol: str, year: str, quarter: str):
        """Legacy method - use get_earnings_call_transcript instead"""
        quarter_format = f"{year}Q{quarter}"
        return await self.get_earnings_call_transcript(symbol, quarter_format)
    
    async def get_economic_data(self, function: str, **kwargs):
        """Generic method for economic data"""
        return await self.get_economic_indicator(function, **kwargs)
    
    # Rate limiting and error handling improvements
    async def _make_request_with_retry(
        self, 
        params: Dict[str, Any], 
        max_retries: int = 3,
        base_url: Optional[str] = None
    ) -> Optional[Dict]:
        """Make API request with retry logic"""
        for attempt in range(max_retries):
            try:
                result = await self._make_request(params, base_url)
                if result:
                    return result
                    
                # If we got rate limited, wait and retry
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    
            except Exception as e:
                self._log_error(f"request_attempt_{attempt + 1}", e)
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
        
        return None
    
    # Data caching methods (if needed)
    def _should_cache_data(self, function: str) -> bool:
        """Determine if data should be cached based on function type"""
        # Cache fundamental data, company info, etc. but not real-time quotes
        cacheable_functions = [
            'OVERVIEW', 'INCOME_STATEMENT', 'BALANCE_SHEET', 'CASH_FLOW',
            'EARNINGS', 'SYMBOL_SEARCH', 'ETF_PROFILE', 'MUTUAL_FUND_PROFILE'
        ]
        return function in cacheable_functions
    
    def get_supported_indicators(self) -> List[str]:
        """Get list of supported technical indicators"""
        return [
            'SMA', 'EMA', 'WMA', 'DEMA', 'TEMA', 'TRIMA', 'KAMA', 'MAMA', 'VWAP',
            'MACD', 'MACDEXT', 'STOCH', 'STOCHF', 'RSI', 'STOCHRSI', 'WILLR',
            'ADX', 'ADXR', 'APO', 'PPO', 'MOM', 'BOP', 'CCI', 'CMO', 'ROC', 'ROCR',
            'AROON', 'AROONOSC', 'MFI', 'TRIX', 'ULTOSC', 'DX', 'MINUS_DI', 'PLUS_DI',
            'MINUS_DM', 'PLUS_DM', 'BBANDS', 'MIDPOINT', 'MIDPRICE', 'SAR', 'TRANGE',
            'ATR', 'NATR', 'AD', 'ADOSC', 'OBV', 'HT_TRENDLINE', 'HT_SINE',
            'HT_TRENDMODE', 'HT_DCPERIOD', 'HT_DCPHASE', 'HT_PHASOR'
        ]
    
    def get_supported_commodities(self) -> List[str]:
        """Get list of supported commodities"""
        return [
            'WTI', 'BRENT', 'NATURAL_GAS', 'COPPER', 'ALUMINUM',
            'WHEAT', 'CORN', 'COTTON', 'SUGAR', 'COFFEE'
        ]
    
    def get_supported_economic_indicators(self) -> List[str]:
        """Get list of supported economic indicators"""
        return [
            'REAL_GDP', 'REAL_GDP_PER_CAPITA', 'TREASURY_YIELD', 'FEDERAL_FUNDS_RATE',
            'CPI', 'INFLATION', 'RETAIL_SALES', 'DURABLES', 'UNEMPLOYMENT', 'NONFARM_PAYROLL'
        ]