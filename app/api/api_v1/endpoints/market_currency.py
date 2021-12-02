from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import json
import math
import requests

from typing import Any, List, Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from app.core.config import settings

from app import crud, schemas
from app.api import deps, services

router = APIRouter()


@router.get("/{base_currency}/{quote_currency}/price", response_model=schemas.MarketCurrencyResponse)
def read_market_currency(
    base_currency: str = Query(..., min_length=3, max_length=8),
    quote_currency: str = Query(..., min_length=3, max_length=8),
    user_id: int = Query(..., ge=1),
) -> Any:
    """
    Retrieve market_currency.
    """
    import logging
    logger = logging.getLogger("app")
    logger.info("base_currency: %s", base_currency)
    
    binance_account = services.get_binance_account_by_id(user_id=user_id)

    # Check and update Binance list of available assets
    binance_assets = crud.binance_asset.get_multi()
    if binance_assets is None:
        assets = services.get_binance_assets(
            binance_account=binance_account
        )
        if assets is None:
            raise HTTPException(status_code=404, detail="Binance assets not found")
        else:
            crud.binance_asset.create_binance_assets(obj_in=assets)

    # Check if asset belongs to Binance assets
    if not crud.binance_asset.does_exist(currency=base_currency):
        raise HTTPException(status_code=404, detail="Binance asset not found")
    if not crud.binance_asset.does_exist(currency=quote_currency):
        raise HTTPException(status_code=404, detail="Binance asset not found")


    market_currency = crud.market_currency.get(
        base_currency=base_currency, quote_currency=quote_currency,
    )
    if market_currency.last_update is None:
        market_currency_in = services.get_binance_currency_price(base_currency, quote_currency)
        market_currency = crud.market_currency.create(obj_in=market_currency_in)

    return market_currency
