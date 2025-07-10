from fastapi import APIRouter

from src.app.schemas.weather_schema import WeatherResponse
from src.app.services.open_weather_map_service import OpenWeatherMapService

weather_router = APIRouter()
open_weather_map_service = OpenWeatherMapService()

@weather_router.get("/get_weather_data/{city_name}", response_model=WeatherResponse,status_code=200)
async def get_weather_data(city_name: str):
    try:
        coordinates = await open_weather_map_service.get_city_coordinates(city_name)
        weather_data = await open_weather_map_service.get_weather_data(coordinates['lat'], coordinates['lon'])
        return weather_data
    except Exception as e:
        raise Exception(f"Error retrieving weather data: {str(e)}")
