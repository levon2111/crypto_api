from fastapi import APIRouter, HTTPException

from app.models.crypto import CoinPriceResponse, ListCoinPriceResponse
from app.services.exchange_api import get_coin_prices, get_price_for_coin

router = APIRouter()


@router.get("/api/prices", response_model=ListCoinPriceResponse)
async def read_prices():
    return ListCoinPriceResponse(root=await get_coin_prices())


@router.get("/api/prices/{coin_name}", response_model=CoinPriceResponse)
async def read_price_by_coin(coin_name: str):
    result = await get_price_for_coin(coin_name)
    if not result:
        raise HTTPException(status_code=404, detail="Coin not found")
    return CoinPriceResponse(**result)
