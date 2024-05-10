from typing import Optional

from pydantic import BaseModel


class PriceResponse(BaseModel):
    binance: Optional[float]
    bybit: Optional[float]


class CoinPriceResponse(BaseModel):
    name: str
    prices: PriceResponse


class ListCoinPriceResponse(BaseModel):
    root: list[CoinPriceResponse]

    def __iter__(self):
        return iter(self.__root__)
