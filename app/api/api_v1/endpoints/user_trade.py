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


@router.get("/{base_currency}/{quote_currency}", response_model=List[schemas.UserTrade])
def read_user_trade(
    user_id: str,
    base_currency: str = Query(..., min_length=3, max_length=8),
    quote_currency: str = Query(..., min_length=3, max_length=8),
    # start_time: str = Query(None, '[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}'),
    # end_time: str = Query(None, '[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}'),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve user_trade.
    """
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

    # Retrieve the user wallet asset
    user_trades = crud.user_trade.get_multi(
        base_currency=base_currency,
        quote_currency=quote_currency,
        user_id=user_id,
    )
    if user_trades is None:
        user_trades_in = services.get_binance_user_currency_trades(
            binance_account=binance_account,
            base_currency=base_currency,
            quote_currency=quote_currency,
        )
        crud.user_trade.create(
            user_id=user_id,
            base_currency=base_currency,
            quote_currency=quote_currency,
            obj_in=user_trades_in,
        )

    user_trades = crud.user_trade.get_multi(
        base_currency=base_currency,
        quote_currency=quote_currency,
        user_id=user_id,
        # start_time=start_time,
        # end_time=end_time,
        skip=skip,
        limit=limit,
    )

    return user_trades


@router.get("/{base_currency}/{quote_currency}/last", response_model=schemas.UserTrade)
def read_last_user_trade(
    user_id: str,
    base_currency: str = Query(..., min_length=3, max_length=8),
    quote_currency: str = Query(..., min_length=3, max_length=8),
) -> Any:
    """
    Retrieve last_user_trade.
    """
    binance_account = services.get_binance_account_by_id(user_id=user_id)

    # Check and update Binance list of available assets
    binance_assets = crud.binance_asset.get_multi()
    if binance_assets is None:
        try:
            assets = services.get_binance_assets(
                binance_account=binance_account
            )
        except:
            return {}
        if assets is None:
            raise HTTPException(status_code=404, detail="Binance assets not found")
        else:
            crud.binance_asset.create_binance_assets(obj_in=assets)

    # Check if asset belongs to Binance assets
    if not crud.binance_asset.does_exist(currency=base_currency):
        raise HTTPException(status_code=404, detail="Binance asset not found")

    # Retrieve the user wallet asset
    user_trades = crud.user_trade.get_multi(
        base_currency=base_currency,
        quote_currency=quote_currency,
        user_id=user_id,
    )
    if user_trades is None:
        user_trades_in = services.get_binance_user_currency_trades(
            binance_account=binance_account,
            base_currency=base_currency,
            quote_currency=quote_currency,
        )
        crud.user_trade.create(
            user_id=user_id,
            base_currency=base_currency,
            quote_currency=quote_currency,
            obj_in=user_trades_in,
        )

    last_user_trade = crud.user_trade.get_multi(
        base_currency=base_currency,
        quote_currency=quote_currency,
        user_id=user_id,
        skip=0,
        limit=1,
    )[-1:][0]

    return last_user_trade
