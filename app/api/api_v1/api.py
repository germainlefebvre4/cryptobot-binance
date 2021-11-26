from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    market_currency,
)

api_router = APIRouter()
api_router.include_router(market_currency.router, prefix="/markets/binance/currencies", tags=["currency"])
