from datetime import datetime
import json

from typing import List, Dict, Union, Any

from fastapi.encoders import jsonable_encoder

from app.utils import convert

from app.cache.session import master, slave
from app.cache.session import master as cache_write
from app.cache.session import slave as cache_read

from app.core.config import settings
from app.crud.base import CRUDBase
from app.schemas import MarketCurrency, MarketCurrencyCreate, MarketCurrencyUpdate


class CRUDMarketCurrency(CRUDBase[MarketCurrency, MarketCurrencyCreate, MarketCurrencyUpdate]):
    def get(
        self, *,
        base_currency: str,
        quote_currency: str,
    ) -> MarketCurrency:
        currency = slave.hgetall(f'currency:{base_currency}:{quote_currency}')
        return convert(currency)


    def get_multi(
        self, *,
        skip: int = 0,
        limit: int = 100
    ) -> List[MarketCurrency]:
        # data = dict(base_currency="AVAX", quote_currency="BUSD", price=100.0)
        # master.hmset('currency:AVAX:BUSD', data)
        keys = slave.keys('currency:*')
        currencies = []
        for key in keys:
            hm = slave.hgetall(key)
            currencies.append(convert(hm))

        return currencies


    def create(
        self, *,
        obj_in: MarketCurrencyCreate,
    ) -> MarketCurrency:
        obj_in_data = jsonable_encoder(obj_in)
        master.hmset(f"currency:{obj_in_data['base_currency']}:{obj_in_data['quote_currency']}", obj_in_data)
        currency = slave.hgetall(f"currency:{obj_in_data['base_currency']}:{obj_in_data['quote_currency']}")
        return convert(currency)
        

market_currency = CRUDMarketCurrency(MarketCurrency)
