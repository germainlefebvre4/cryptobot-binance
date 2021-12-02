from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class MarketCurrencyBase(BaseModel):
    base_currency: str
    quote_currency: str
    price: float


class MarketCurrencyCreate(MarketCurrencyBase):
    pass


class MarketCurrencyUpdate(MarketCurrencyBase):
    pass


class MarketCurrency(MarketCurrencyBase):
    pass


class MarketCurrencyResponse(BaseModel):
    object: Optional[MarketCurrency] = None
    last_update: Optional[datetime] = None
