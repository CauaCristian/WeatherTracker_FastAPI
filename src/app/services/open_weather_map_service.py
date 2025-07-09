import requests
from dotenv import load_dotenv
import os

load_dotenv()

class OpenWeatherMapService:

    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.data_url = os.getenv("WEATHER_API_DATA_URL")
        self.geo_url = os.getenv("WEATHER_API_GEO_URL")
        from src.core.database.redis import RedisDatabase
        self.redis_database = RedisDatabase()
        self.redis_client = self.redis_database.get_client()

    async def get_city_coordinates(self, city_name: str) -> dict:
        try:
            valor = await self.redis_client.get(city_name)
            if valor:
                lat_str, lon_str = valor.decode().split(",")
                print("dado veio do cache")
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
            print("dado veio da api externa")
            return {
                "lat": data[0]["lat"],
                "lon": data[0]["lon"]
            }
        except requests.RequestException as e:
            raise Exception(f"Error fetching city coordinates: {str(e)}")

    async def get_weather_data(self, lat: float, lon: float) -> dict:
        try:
            valor = await self.redis_client.get(f"{lat},{lon}")
            if valor:
                print("dado veio do cache")
                return json.loads(valor.decode())
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
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Error fetching weather data: {str(e)}")