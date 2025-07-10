import requests
from dotenv import load_dotenv
import os
from src.app.models.weather_history_model import WeatherHistoryModel
from src.app.schemas.weather_schema import WeatherResponse, WeatherHistoryCreate
from datetime import datetime, timedelta, timezone
from src.core.database.redis import RedisDatabase
from src.app.repositories.weather_history_repository import WeatherHistoryRepository

load_dotenv()

class OpenWeatherMapService:

    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.data_url = os.getenv("WEATHER_API_DATA_URL")
        self.geo_url = os.getenv("WEATHER_API_GEO_URL")
        self.weather_history_repository = WeatherHistoryRepository()
        self.redis_database = RedisDatabase()
        self.redis_client = self.redis_database.get_client()

    async def get_city_coordinates(self, city_name: str) -> dict:
        try:
            valor = await self.redis_client.get(city_name)
            if valor:
                lat_str, lon_str = valor.decode().split(",")
                print("dado veio do cache de coordenadas")
                return {
                    "lat": float(lat_str),
                    "lon": float(lon_str)
                }
            response = requests.get(
                self.geo_url,
                params={"q": city_name+",076", "limit": 1,"appid": self.api_key}
            )
            response.raise_for_status()
            data = response.json()
            if not data:
                raise ValueError("City not found")
            import json
            await self.redis_client.set(city_name, f"{data[0]['lat']},{data[0]['lon']}", ex=1800)  # Cache de 30 minutos
            print("dado veio da api externa de coordenadas")
            return {
                "lat": data[0]["lat"],
                "lon": data[0]["lon"]
            }
        except requests.RequestException as e:
            raise Exception(f"Error fetching city coordinates: {str(e)}")


    async def get_weather_data(self, lat: float, lon: float) -> WeatherResponse:
        try:
            valor = await self.redis_client.get(f"{lat},{lon}")
            if valor:
                city_name,country,lat,lon,weather,humidity,temperature,temperature_feels_like,temperature_max,temperature_min,wind_speed = valor.decode().split(",")
                weather_response = WeatherResponse(
                    id=0,
                    city_name=city_name,
                    country=country,
                    lat=float(lat),
                    lon=float(lon),
                    weather=weather,
                    humidity=int(humidity),
                    temperature=float(temperature),
                    temperature_feels_like=float(temperature_feels_like),
                    temperature_max=float(temperature_max),
                    temperature_min=float(temperature_min),
                    wind_speed=float(wind_speed),
                    recorded_at=datetime.now(timezone.utc)
                )
                print("dado veio do cache de clima")
                return weather_response
            response = requests.get(
                self.data_url,
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "lang": "pt_br",
                    "units": "metric"
                }
            )
            response.raise_for_status()
            data = response.json()
            print("dado veio da api externa de clima")
            weather_history_model = WeatherHistoryModel(
                city_name=data["name"],
                country=data["sys"]["country"],
                lat=data["coord"]["lat"],
                lon=data["coord"]["lon"],
                weather=data["weather"][0]["description"],
                humidity=data["main"]["humidity"],
                temperature=data["main"]["temp"],
                temperature_feels_like=data["main"]["feels_like"],
                temperature_max=data["main"]["temp_max"],
                temperature_min=data["main"]["temp_min"],
                wind_speed=data["wind"]["speed"],
            )
            weather_history_model = self.weather_history_repository.add_weather_history(weather_history_model)
            await self.redis_client.set(f"{lat},{lon}",f"{data['name']},{data['sys']['country']},{data['coord']['lat']},{data['coord']['lon']},{data['weather'][0]['description']},{data['main']['humidity']},{data['main']['temp']},{data['main']['feels_like']},{data['main']['temp_max']},{data['main']['temp_min']},{data['wind']['speed']}", ex=1800)  # Cache de 30 minutos
            return WeatherResponse(
                id=weather_history_model.id,
                city_name=data["name"],
                country=data["sys"]["country"],
                lat=data["coord"]["lat"],
                lon=data["coord"]["lon"],
                weather=data["weather"][0]["description"],
                humidity=data["main"]["humidity"],
                temperature=data["main"]["temp"],
                temperature_feels_like=data["main"]["feels_like"],
                temperature_max=data["main"]["temp_max"],
                temperature_min=data["main"]["temp_min"],
                wind_speed=data["wind"]["speed"],
                recorded_at= datetime.now(timezone.utc)
            )
        except requests.RequestException as e:
            raise Exception(f"Error fetching weather data: {str(e)}")