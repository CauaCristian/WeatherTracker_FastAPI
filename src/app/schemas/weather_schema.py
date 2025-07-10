from pydantic import BaseModel
from datetime import datetime,timezone

class WeatherHistoryCreate(BaseModel):
    city_name: str
    country: str
    lat: float
    lon: float
    weather: str
    humidity: int
    temperature: float
    temperature_feels_like: float
    temperature_max: float
    temperature_min: float
    wind_speed: float

class WeatherResponse(BaseModel):
    id: int
    city_name: str
    country: str
    lat: float
    lon: float
    weather: str
    humidity: int
    temperature: float
    temperature_feels_like: float
    temperature_max: float
    temperature_min: float
    wind_speed: float
    recorded_at: datetime
    model_config = {"from_attributes": True}