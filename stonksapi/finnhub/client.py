import os
import finnhub
from typing import Optional, List

from .models import (
    CompanyProfile,
    Quote,
    MarketNews,
)


class FinnhubClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("FINNHUB_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either as an argument or as a FINNHUB_API_KEY environment variable."
            )
        self._client = finnhub.Client(api_key=self.api_key)

    def get_company_profile(self, ticker: str) -> CompanyProfile:
        """
        Get company profile.
        https://finnhub.io/docs/api/company-profile2
        """
        resp = self._client.company_profile2(symbol=ticker)
        return CompanyProfile.model_validate(resp)

    def get_quote(self, ticker: str) -> Quote:
        """
        Get quote data.
        https://finnhub.io/docs/api/quote
        """
        resp = self._client.quote(symbol=ticker)
        return Quote.model_validate(resp)

    def get_market_news(self, category: str, min_id: int = 0) -> List[MarketNews]:
        """
        Get market news.
        https://finnhub.io/docs/api/market-news
        """
        resp = self._client.general_news(category, min_id=min_id)
        return [MarketNews.model_validate(news) for news in resp]
