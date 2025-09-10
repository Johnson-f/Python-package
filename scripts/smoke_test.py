#!/usr/bin/env python3
"""
Simple smoke test for providers using AAPL.

Reads API keys from environment variables:
- TWELVEDATA_API_KEY
- FMP_API_KEY
- POLYGON_API_KEY
- FINNHUB_API_KEY
- ALPHAVANTAGE_API_KEY
- FISCAL_API_KEY

Run:
  python scripts/smoke_test.py

Notes:
- Each provider section is skipped if its API key is missing.
- Keeps calls minimal to respect free-tier rate limits.
"""
import os
import sys
import asyncio
from datetime import date, timedelta

# Ensure src/ is importable
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(ROOT, 'src')
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from marketdata_providers.providers.twelve_data import TwelveDataProvider  # type: ignore
from marketdata_providers.providers.fmp import FMPProvider  # type: ignore
from marketdata_providers.providers.polygon import PolygonProvider  # type: ignore
from marketdata_providers.providers.finnhub import FinnhubProvider  # type: ignore
from marketdata_providers.providers.alpha_vantage import AlphaVantageProvider  # type: ignore
from marketdata_providers.providers.fiscal import FiscalAIProvider  # type: ignore


async def test_twelvedata():
    api_key = os.getenv('TWELVEDATA_API_KEY')
    if not api_key:
        print('[TwelveData] Skipped (TWELVEDATA_API_KEY not set)')
        return
    print('[TwelveData] Starting smoke test...')
    provider = TwelveDataProvider(api_key)
    quote = await provider.get_quote('AAPL')
    print('  Quote:', quote)
    end = date.today()
    start = end - timedelta(days=7)
    hist = await provider.get_historical('AAPL', start_date=start, end_date=end, interval='1day', limit=50)
    print(f'  Historical count: {len(hist)}')
    await provider.close()
    print('[TwelveData] OK')


async def test_fmp():
    api_key = os.getenv('FMP_API_KEY')
    if not api_key:
        print('[FMP] Skipped (FMP_API_KEY not set)')
        return
    print('[FMP] Starting smoke test...')
    provider = FMPProvider(api_key)
    quote = await provider.get_quote('AAPL')
    print('  Quote:', quote)
    end = date.today()
    start = end - timedelta(days=14)
    hist = await provider.get_historical('AAPL', start_date=start, end_date=end, interval='1day')
    print(f'  Historical count: {len(hist)}')
    print('[FMP] OK')


async def test_polygon():
    api_key = os.getenv('POLYGON_API_KEY')
    if not api_key:
        print('[Polygon] Skipped (POLYGON_API_KEY not set)')
        return
    print('[Polygon] Starting smoke test...')
    provider = PolygonProvider(api_key)
    quote = await provider.get_quote('AAPL')
    print('  Quote:', quote)
    print('[Polygon] OK')


async def main():
    await test_twelvedata()
    await test_fmp()
    await test_polygon()
    await test_finnhub()
    await test_alpha_vantage()
    await test_fiscal()


async def test_finnhub():
    api_key = os.getenv('FINNHUB_API_KEY')
    if not api_key:
        print('[Finnhub] Skipped (FINNHUB_API_KEY not set)')
        return
    print('[Finnhub] Starting smoke test...')
    provider = FinnhubProvider(api_key)
    quote = await provider.get_quote('AAPL')
    print('  Quote:', quote)
    end = date.today()
    start = end - timedelta(days=7)
    hist = await provider.get_historical('AAPL', start_date=start, end_date=end, interval='1d')
    print(f'  Historical count: {len(hist)}')
    print('[Finnhub] OK')


async def test_alpha_vantage():
    api_key = os.getenv('ALPHAVANTAGE_API_KEY')
    if not api_key:
        print('[AlphaVantage] Skipped (ALPHAVANTAGE_API_KEY not set)')
        return
    print('[AlphaVantage] Starting smoke test...')
    provider = AlphaVantageProvider(api_key)
    quote = await provider.get_quote('AAPL')
    print('  Quote:', quote)
    end = date.today()
    start = end - timedelta(days=14)
    hist = await provider.get_historical('AAPL', start, end, interval='1d')
    print(f'  Historical count: {len(hist or [])}')
    print('[AlphaVantage] OK')


async def test_fiscal():
    api_key = os.getenv('FISCAL_API_KEY')
    if not api_key:
        print('[FiscalAI] Skipped (FISCAL_API_KEY not set)')
        return
    print('[FiscalAI] Starting smoke test...')
    provider = FiscalAIProvider(api_key)
    quote = await provider.get_quote('AAPL')
    print('  Quote:', quote)
    end = date.today()
    start = end - timedelta(days=7)
    hist = await provider.get_historical('AAPL', start_date=start, end_date=end, interval='1d')
    print(f'  Historical count: {len(hist)}')
    await provider.close()
    print('[FiscalAI] OK')


if __name__ == '__main__':
    asyncio.run(main())
