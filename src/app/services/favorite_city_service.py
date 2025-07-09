from src.app.models.favorite_city_model import FavoriteCityModel
from src.app.schemas.favorite_city_schema import FavoriteCityCreate, FavoriteCityResponse
from src.app.repositories.favorite_city_repository import FavoriteCityRepository
from src.app.services.open_weather_map_service import OpenWeatherMapService

class FavoriteCityService:
    def __init__(self):
        self.favorite_city_repository = FavoriteCityRepository()
        self.open_weather_map_service = OpenWeatherMapService()

    async def add_favorite_city(self, favorite_city: FavoriteCityCreate) -> FavoriteCityResponse:
        try:
            info = await self.open_weather_map_service.get_city_coordinates(favorite_city.city_name)
            new_favorite_city = FavoriteCityModel(
                user_id=favorite_city.user_id,
                city_name=favorite_city.city_name,
                lon=info['lon'],
                lat=info['lat'],
            )
            new_favorite_city = self.favorite_city_repository.add_favorite_city(
                new_favorite_city
            )
            return FavoriteCityResponse.from_orm(new_favorite_city)
        except Exception as e:
            raise Exception(f"Error adding favorite city: {str(e)}")

    def get_favorite_cities_by_user_id(self, user_id: int) -> list[FavoriteCityResponse]:
        try:
            favorite_cities = self.favorite_city_repository.get_favorite_cities_by_user_id(user_id)
            return [FavoriteCityResponse.from_orm(city) for city in favorite_cities]
        except Exception as e:
            raise Exception(f"Error retrieving favorite cities: {str(e)}")

    def delete_favorite_city(self, city_id: int):
        try:
            self.favorite_city_repository.delete_favorite_city(city_id)
        except Exception as e:
            raise Exception(f"Error deleting favorite city: {str(e)}")