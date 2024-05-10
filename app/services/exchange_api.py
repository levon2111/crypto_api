import httpx

from app.services.constants import BINANCE_API_URL, BYBIT_API_URL


async def fetch_prices_from_binance():
    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_API_URL)
        return {item["symbol"]: float(item["price"]) for item in response.json()}


async def fetch_prices_from_bybit():
    async with httpx.AsyncClient() as client:
        response = await client.get(BYBIT_API_URL)
        return {item["symbol"]: float(item["last_price"]) for item in response.json()["result"]}


async def get_coin_prices():
    binance_prices = await fetch_prices_from_binance()
    bybit_prices = await fetch_prices_from_bybit()

    coins = set(binance_prices.keys()) | set(bybit_prices.keys())
    return [
        {
            "name": coin,
            "prices": {
                "binance": binance_prices.get(coin, None),
                "bybit": bybit_prices.get(coin, None)
            }
        } for coin in coins
    ]


async def get_price_for_coin(coin_name):
    binance_prices = await fetch_prices_from_binance()
    bybit_prices = await fetch_prices_from_bybit()

    if coin_name in binance_prices or coin_name in bybit_prices:
        return {
            "name": coin_name,
            "prices": {
                "binance": binance_prices.get(coin_name, "N/A"),
                "bybit": bybit_prices.get(coin_name, "N/A")
            }
        }
    return None
