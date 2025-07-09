import requests
from dotenv import load_dotenv
import os

load_dotenv()

class OpenWeatherMapService:

    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.data_url = os.getenv("WEATHER_API_DATA_URL")
        self.geo_url = os.getenv("WEATHER_API_GEO_URL")

    def get_city_coordinates(self, city_name: str) -> dict:
        try:
            response = requests.get(
                self.geo_url,
                params={"q": city_name+",076", "limit": 1,"appid": self.api_key}
            )
            response.raise_for_status()
            data = response.json()
            if not data:
                raise ValueError("City not found")
            return {
                "lat": data[0]["lat"],
                "lon": data[0]["lon"]
            }
        except requests.RequestException as e:
            raise Exception(f"Error fetching city coordinates: {str(e)}")

    def get_weather_data(self, lat: float, lon: float) -> dict:
        try:
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