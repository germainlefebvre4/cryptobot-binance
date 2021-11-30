from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class WalletAssetBase(BaseModel):
    asset: str
    free: float
    locked: float


class WalletAssetCreate(WalletAssetBase):
    pass


class WalletAssetUpdate(WalletAssetBase):
    pass


class WalletAsset(WalletAssetBase):
    pass
