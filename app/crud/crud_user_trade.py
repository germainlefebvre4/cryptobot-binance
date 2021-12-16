from datetime import datetime, timedelta
import json

from pydantic import ValidationError
from typing import List, Dict, Union, Any

from fastapi.encoders import jsonable_encoder

from app.utils.string import convert

from app.cache.session import master, slave
from app.cache.session import master as cache_write
from app.cache.session import slave as cache_read

from app.core.config import settings
from app.crud.base import CRUDBase
from app.schemas import UserTrade, UserTradeCreate, UserTradeUpdate


class CRUDUserTrade(CRUDBase[UserTrade, UserTradeCreate, UserTradeUpdate]):
    def get_multi(
        self, *,
        user_id: str,
        base_currency: str,
        quote_currency: str,
        limit: int = 100,
        skip: int = 0,
    ) -> List[UserTrade]:
        data_key = f"markets:binance:user:{user_id}:currency:{base_currency}:{quote_currency}:trades"
        if slave.exists(data_key):
            trades_str = slave.get(data_key)
            trades = convert(json.loads(trades_str))[-limit:]
        else:
            trades = None
        return trades


    def create(
        self, *,
        obj_in: UserTradeCreate,
        user_id: str,
        base_currency: str,
        quote_currency: str,
    ) -> List[UserTrade]:
        obj_in_data = json.dumps(obj_in)
        data_key = f"markets:binance:user:{user_id}:currency:{base_currency}:{quote_currency}:trades"
        master.set(data_key, obj_in_data)
        data_ttl_seconds = (datetime.today() + timedelta(minutes=30)).timestamp()
        master.expireat(data_key, int(data_ttl_seconds))
        trades_str = slave.get(data_key)
        try:
            trades = convert(json.loads(trades_str))
        except ValidationError as e:
            raise dict(detail="Incorrect format", error=e)

        return trades


user_trade = CRUDUserTrade(UserTrade)
