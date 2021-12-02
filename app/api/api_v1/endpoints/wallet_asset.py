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


@router.get("/{base_currency}", response_model=schemas.WalletAssetResponse)
def read_wallet_asset(
    user_id: int = Query(..., ge=1),
    base_currency: str = Query(..., min_length=3, max_length=8),
) -> Any:
    """
    Retrieve wallet_asset.
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
    wallet_asset = crud.wallet_asset.get(
        base_currency=base_currency,
        user_id=user_id,
    )
    if wallet_asset.object is None:
        wallet_assets_in = services.get_binance_wallet_assets_volume(
            binance_account=binance_account,
        )
        for wallet_asset in wallet_assets_in:
            crud.wallet_asset.create(obj_in=wallet_asset, user_id=user_id)

    wallet_asset = crud.wallet_asset.get(
        base_currency=base_currency,
        user_id=user_id,
    )

    return wallet_asset
