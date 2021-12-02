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
from app.schemas import WalletAsset, WalletAssetCreate, WalletAssetUpdate, WalletAssetResponse


class CRUDBinanceAsset(CRUDBase[WalletAsset, WalletAssetCreate, WalletAssetUpdate]):

    def get_multi(
        self,
    ) -> List[WalletAsset]:
        key = f"markets:binance:assets"
        key_last_update = key + ":last_update"

        if slave.exists(key) and slave.exists(key_last_update):
            assets = slave.smembers(key)
            assets_last_update = slave.get(key_last_update)
        else:
            assets = None
            assets_last_update = None

        return convert(assets)


    def create_binance_assets(
        self, *,
        obj_in: List[str],
    ) -> WalletAsset:
        key = f"markets:binance:assets"
        key_last_update = key + ":last_update"
        data = jsonable_encoder(obj_in)
        last_update = datetime.now().isoformat()
        ttl_seconds = (datetime.today() + timedelta(days=1)).timestamp()

        master.sadd(key, *data)
        master.expire(key, int(ttl_seconds))

        master.set(key_last_update, last_update)
        master.expire(key_last_update, int(ttl_seconds))

        assets = slave.smembers(key)
        return convert(assets)


    def does_exist(
        self, *,
        currency: str,
    ) -> bool:
        key = f"markets:binance:assets"
        assets = slave.smembers(key)

        return any([convert(x) for x in assets if convert(x) == currency])


binance_asset = CRUDBinanceAsset(WalletAsset)
