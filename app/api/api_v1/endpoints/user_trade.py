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
