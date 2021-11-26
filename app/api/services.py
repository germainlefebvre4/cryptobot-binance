from typing import Optional

from app.schemas import MarketCurrency

from binance.client import Client


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

