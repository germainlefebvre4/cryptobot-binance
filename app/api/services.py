from typing import Optional, List
import requests
from datetime import datetime

from fastapi import Query

from app.core.config import settings

from app.schemas import (
    MarketCurrency, WalletAsset,
)
from app.schemas.binance_account import BinanceAccount

from binance.client import Client


def get_binance_account_by_id(
    user_id: int,
):
    response = requests.get(f"{settings.API_URL}/binance/accounts/?user_id={user_id}",
        headers = {
            f"{settings.API_KEY_NAME}": f"{settings.API_KEY}"
        },
    )
    return response.json()[0]


def get_binance_currency_price(
    base_currency: str,
    quote_currency: str,
    ) -> Optional[MarketCurrency]:
    client = Client()
    currency_price = float(client.get_symbol_ticker(symbol=f"{base_currency}{quote_currency}")['price'])

    return MarketCurrency(
        base_currency=base_currency,
        quote_currency=quote_currency,
        price=currency_price,
    )


def get_binance_wallet_asset_volume(
    binance_account: BinanceAccount,
    base_currency: str,
    ) -> Optional[WalletAsset]:
    client = Client(binance_account['binance_api_key'], binance_account['binance_api_secret'])

    try:
        asset_balance = client.get_asset_balance(asset=base_currency)
    except:
        raise Exception("Error getting asset balance")

    return WalletAsset(
        asset=base_currency,
        free=asset_balance['free'],
        locked=asset_balance['locked'],
    )


def get_binance_wallet_assets_volume(
    binance_account: BinanceAccount,
    ) -> Optional[List[MarketCurrency]]:
    client = Client(binance_account['binance_api_key'], binance_account['binance_api_secret'])

    try:
        assets_balance = client.get_account()['balances']
    except:
        raise Exception("Error getting asset balance")

    assets = []
    for asset in assets_balance:
        print(asset)
        assets.append(WalletAsset(
            asset=asset['asset'],
            free=asset['free'],
            locked=asset['locked'],
        ))

    return assets


def get_binance_assets(
    binance_account: BinanceAccount,
    ) -> Optional[List[MarketCurrency]]:
    client = Client(binance_account['binance_api_key'], binance_account['binance_api_secret'])

    try:
        binance_assets = client.get_account()['balances']
        assets = [x['asset'] for x in binance_assets]
    except:
        raise Exception("Error getting assets")

    return assets


def get_binance_user_currency_trades(
    binance_account: BinanceAccount,
    base_currency: str,
    quote_currency: str,
    # start_time: str = Query(None, '[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}'),
    # end_time: str = Query(None, '[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}'),
    ) -> Optional[List[MarketCurrency]]:
    client = Client(binance_account['binance_api_key'], binance_account['binance_api_secret'])

    # Format start/end time for query param
    # if start_time:
    #     start_time = int(datetime.strptime(start_time, '%Y-%m-%d').timestamp()*1000)
    # if end_time:
    #     end_time = int(datetime.strptime(end_time, '%Y-%m-%d').timestamp()*1000)

    try:
        trades = client.get_my_trades(
            symbol=f"{base_currency}{quote_currency}",
        )
    except:
        raise Exception("Error getting trades")

    return trades
