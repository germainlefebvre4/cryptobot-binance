
def get_redis_market_currency_key(
    base_currency: str,
    quote_currency: str
    ) -> str:
    return f"markets:binance:currency:{base_currency}:{quote_currency}"
