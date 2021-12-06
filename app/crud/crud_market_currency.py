from datetime import datetime, timedelta
import json

from typing import List, Dict, Union, Any

from fastapi.encoders import jsonable_encoder

from app.utils.string import convert

from app.cache.session import master, slave

from app.core.config import settings
from app.crud.base import CRUDBase
from app.schemas import MarketCurrency, MarketCurrencyCreate, MarketCurrencyUpdate, MarketCurrencyResponse


class CRUDMarketCurrency(CRUDBase[MarketCurrency, MarketCurrencyCreate, MarketCurrencyUpdate]):
    def get(
        self, *,
        base_currency: str,
        quote_currency: str,
    ) -> MarketCurrencyResponse:
        key = f"markets:binance:currency:{base_currency}:{quote_currency}"
        key_last_update = key + ":last_update"
        
        if slave.exists(key) and slave.exists(key_last_update):
            currency = slave.hgetall(key)
            currency_last_update = slave.get(key_last_update)
        else:
            currency = None
            currency_last_update = None

        return MarketCurrencyResponse(
            object=convert(currency),
            last_update=currency_last_update,
        )

    def create(
        self, *,
        obj_in: MarketCurrencyCreate,
    ) -> MarketCurrencyResponse:
        key = f"markets:binance:currency:{obj_in.base_currency}:{obj_in.quote_currency}"
        key_last_update = key + ":last_update"
        data = jsonable_encoder(obj_in)
        last_update = datetime.now().isoformat()
        ttl_seconds = (datetime.today() + timedelta(minutes=5)).timestamp()

        master.hmset(key, data)
        master.expireat(key, int(ttl_seconds))

        master.set(key_last_update, last_update)
        master.expireat(key_last_update, int(ttl_seconds))

        currency = slave.hgetall(key)

        return MarketCurrencyResponse(
            object=convert(currency),
            last_update=last_update,
        )
        

market_currency = CRUDMarketCurrency(MarketCurrency)
