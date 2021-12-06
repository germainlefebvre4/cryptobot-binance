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


class CRUDWalletAsset(CRUDBase[WalletAsset, WalletAssetCreate, WalletAssetUpdate]):
    def get(
        self, *,
        user_id: str,
        base_currency: str,
    ) -> WalletAssetResponse:
        key = f"markets:binance:wallet:{user_id}:{base_currency}"
        key_last_update = key + ":last_update"

        if slave.exists(key) and slave.exists(key_last_update):
            wallet = slave.hgetall(key)
            wallet_last_update = slave.get(key_last_update)
        else:
            wallet = None
            wallet_last_update = None

        return WalletAssetResponse(
            object=convert(wallet),
            last_update=wallet_last_update,
        )


    def get_multi_by_user(
        self, *,
        user_id: str,
        base_currency: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[WalletAssetResponse]:
        keys = slave.keys(f"markets:binance:wallet:{user_id}:{base_currency}:*")
        
        assets = []
        for key in keys:
            key_last_update = key + ":last_update"

            wallet = slave.hgetall(key)
            wallet_last_update = slave.get(key_last_update)

            asset = WalletAssetResponse(
                object=convert(wallet),
                last_update=wallet_last_update,
            )
            assets.append(asset)

        return assets


    def create(
        self, *,
        obj_in: WalletAssetCreate,
        user_id: str,
    ) -> WalletAssetResponse:
        key = f"markets:binance:wallet:{user_id}:{obj_in.asset}"
        key_last_update = key + ":last_update"
        data = jsonable_encoder(obj_in)
        last_update = datetime.now().isoformat()
        ttl_seconds = (datetime.today() + timedelta(minutes=30)).timestamp()

        master.hmset(key, data)
        master.expireat(key, int(ttl_seconds))

        master.set(key_last_update, last_update)
        master.expireat(key_last_update, int(ttl_seconds))
        
        wallet = slave.hgetall(key)
        wallet_last_update = slave.get(key_last_update)

        return WalletAssetResponse(
            object=convert(wallet),
            last_update=wallet_last_update,
        )


wallet_asset = CRUDWalletAsset(WalletAsset)
