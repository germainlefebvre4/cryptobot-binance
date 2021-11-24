from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel

from app.schemas.market_currency import MarketCurrency


class BinanceMarket(BaseModel):
    market: List[MarketCurrency]
