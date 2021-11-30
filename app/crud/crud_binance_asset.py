from datetime import datetime, timedelta
import json

from typing import List, Dict, Union, Any

from fastapi.encoders import jsonable_encoder

from app.utils.string import convert

from app.cache.session import master, slave
from app.cache.session import master as cache_write
from app.cache.session import slave as cache_read

from app.core.config import settings
from app.crud.base import CRUDBase
from app.schemas import WalletAsset, WalletAssetCreate, WalletAssetUpdate


class CRUDBinanceAsset(CRUDBase[WalletAsset, WalletAssetCreate, WalletAssetUpdate]):

    def create_binance_assets(
        self, *,
        obj_in: List[str],
    ) -> WalletAsset:
        obj_in_data = jsonable_encoder(obj_in)
        data_key = f"markets:binance:assets"
        master.sadd(data_key, *obj_in_data)
        data_ttl_seconds = (datetime.today() + timedelta(minutes=30)).timestamp()
        master.expire(data_key, int(data_ttl_seconds))
        assets = slave.hgetall(data_key)
        return convert(assets)


    def get_binance_assets(
        self,
    ) -> List[str]:
        data_key = f"markets:binance:assets"
        if slave.exists(data_key):
            assets = slave.smembers(data_key)
        else:
            assets = None
        # print("get_binance_assets", convert(assets))
        return convert(assets)


    def create_binance_asset(
        self, *,
        obj_in: str,
    ) -> WalletAsset:
        obj_in_data = jsonable_encoder(obj_in)
        data_key = f"markets:binance:assets:{obj_in_data}"
        print(data_key)
        master.set(data_key, "True")
        data_ttl_seconds = (datetime.today() + timedelta(minutes=30)).timestamp()
        master.expire(data_key, int(data_ttl_seconds))
        assets = slave.hgetall(data_key)
        return convert(assets)


    def does_exist(
        self, *,
        base_currency: str,
    ) -> bool:
        data_key = f"markets:binance:assets"
        assets = slave.smembers(data_key)
        return any([convert(x) for x in assets if convert(x) == base_currency])


binance_asset = CRUDBinanceAsset(WalletAsset)
