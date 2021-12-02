from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    market_currency, wallet_asset, user_trade
)

api_router = APIRouter()
api_router.include_router(market_currency.router, prefix="/currency", tags=["currency"])
api_router.include_router(wallet_asset.router, prefix="/wallet", tags=["wallet"])
api_router.include_router(user_trade.router, prefix="/trades", tags=["trades"])
