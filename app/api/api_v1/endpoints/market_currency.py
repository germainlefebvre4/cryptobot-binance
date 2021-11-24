from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import json
import math
import requests

from typing import Any, List, Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from app.core.config import settings

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.MarketCurrency])
def read_market_currencies(
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve market_currencies.
    """
    market_currencies = crud.market_currency.get_multi(skip=skip, limit=limit)

    return market_currencies


@router.post("/", response_model=schemas.MarketCurrency)
def create_market_currency(
    market_currency_in: schemas.MarketCurrencyCreate,
) -> Any:
    """
    Creat new market_currency.
    """
    market_currency = crud.market_currency.create(obj_in=market_currency_in)

    return market_currency


@router.get("/{base_currency}/{quote_currency}", response_model=schemas.MarketCurrency)
def read_market_currency(
    base_currency: str = Query(..., min_length=3, max_length=8),
    quote_currency: str = Query(..., min_length=3, max_length=8),
) -> Any:
    """
    Retrieve market_currency.
    """
    market_currency = crud.market_currency.get(
        base_currency=base_currency, quote_currency=quote_currency,
    )

    return market_currency
