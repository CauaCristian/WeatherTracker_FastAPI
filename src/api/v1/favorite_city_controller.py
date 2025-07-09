from fastapi import APIRouter

from src.app.schemas.favorite_city_schema import FavoriteCityCreate
from src.app.services.favorite_city_service import FavoriteCityService
favorite_city_router = APIRouter()
favorite_city_service = FavoriteCityService()

@favorite_city_router.post("/add_favorite-city", status_code=201)
async def add_favorite_city(city: FavoriteCityCreate):
    return await favorite_city_service.add_favorite_city(city)