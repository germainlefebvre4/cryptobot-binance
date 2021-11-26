from datetime import datetime, timedelta
import json

from typing import List, Dict, Union, Any

from fastapi.encoders import jsonable_encoder

from app.utils.string import convert
from app.utils.market_currency import get_redis_market_currency_key

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
        data_key = get_redis_market_currency_key(base_currency, quote_currency)
        if slave.exists(data_key):
            currency = slave.hgetall(data_key)
        else:
            currency = None
        return convert(currency)


    def get_multi(
        self, *,
        skip: int = 0,
        limit: int = 100
    ) -> List[MarketCurrency]:
        keys = slave.keys('markets:binance:currency:*')
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
        data_key = get_redis_market_currency_key(obj_in_data['base_currency'], obj_in_data['quote_currency'])
        master.hmset(data_key, obj_in_data)
        data_ttl_seconds = (datetime.today() + timedelta(minutes=5)).timestamp()
        master.expire(data_key, int(data_ttl_seconds))
        currency = slave.hgetall(data_key)
        return convert(currency)
        

market_currency = CRUDMarketCurrency(MarketCurrency)
