from src.core.database.postgres import base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timezone
class WeatherHistoryModel(base):
    __tablename__ = 'weather_histories'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    city_name= Column(String, nullable=False)
    country = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    weather = Column(String, nullable=False)
    humidity = Column(Integer, nullable=False)
    temperature = Column(Float, nullable=False)
    temperature_feels_like = Column(Float, nullable=False)
    temperature_max= Column(Float, nullable=False)
    temperature_min= Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    datetime = Column(DateTime, nullable=False)

    def __init__(self, city_name, country, lat, lon, weather, humidity, temperature, temperature_feels_like, temperature_max, temperature_min, wind_speed, local_datetime = datetime.now(timezone.utc)):
        self.city_name = city_name
        self.country = country
        self.lat = lat
        self.lon = lon
        self.weather = weather
        self.humidity = humidity
        self.temperature = temperature
        self.temperature_feels_like = temperature_feels_like
        self.temperature_max = temperature_max
        self.temperature_min = temperature_min
        self.wind_speed = wind_speed
        self.datetime = local_datetime