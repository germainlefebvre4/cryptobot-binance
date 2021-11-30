from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class UserTradeBase(BaseModel):
    symbol: str
    id: int
    orderId: int
    orderListId: int
    price: str
    qty: str
    quoteQty: str
    commission: str
    commissionAsset: str
    time: int
    isBuyer: bool
    isMaker: bool
    isBestMatch: bool

class UserTradeCreate(UserTradeBase):
    pass


class UserTradeUpdate(UserTradeBase):
    pass


class UserTrade(UserTradeBase):
    pass
