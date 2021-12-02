from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel


class BinanceAccountBase(BaseModel):
    binance_api_url: str = "https://api.binance.com"
    binance_api_key: str
    binance_api_secret: str


class BinanceAccountCreate(BinanceAccountBase):
    binance_api_key: str
    binance_api_secret: str


class BinanceAccountUpdate(BaseModel):
    binance_api_key: str
    binance_api_secret: str


class BinanceAccountDelete(BinanceAccountBase):
    id: int

    class Config:
        orm_mode = True


class BinanceAccountInDBBase(BinanceAccountBase):
    id: int
    
    created_on: Optional[datetime]
    updated_on: Optional[datetime]

    class Config:
        orm_mode = True


class BinanceAccount(BinanceAccountInDBBase):
    pass


class BinanceAccountInDB(BinanceAccountInDBBase):
    pass
