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


class CRUDWalletAsset(CRUDBase[WalletAsset, WalletAssetCreate, WalletAssetUpdate]):
    def get(
        self, *,
        user_id: str,
        base_currency: str,
    ) -> WalletAsset:
        data_key = f"markets:binance:wallet:{user_id}:{base_currency}"
        if slave.exists(data_key):
            asset = slave.hgetall(data_key)
        else:
            asset = None
        return convert(asset)


    def get_multi_by_user(
        self, *,
        user_id: str,
        base_currency: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[WalletAsset]:
        keys = slave.keys(f"markets:binance:wallet:{user_id}:{base_currency}:*")
        assets = []
        for key in keys:
            hm = slave.hgetall(key)
            assets.append(convert(hm))

        return assets


    def create(
        self, *,
        obj_in: WalletAssetCreate,
        user_id: str,
    ) -> WalletAsset:
        obj_in_data = jsonable_encoder(obj_in)
        data_key = f"markets:binance:wallet:{user_id}:{obj_in_data['asset']}"
        master.hmset(data_key, obj_in_data)
        data_ttl_seconds = (datetime.today() + timedelta(minutes=30)).timestamp()
        master.expire(data_key, int(data_ttl_seconds))
        currency = slave.hgetall(data_key)
        return convert(currency)


wallet_asset = CRUDWalletAsset(WalletAsset)
