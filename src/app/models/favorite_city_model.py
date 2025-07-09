from sqlalchemy import Column, Integer, String, ForeignKey,Float
from src.core.database.postgres import base
class FavoriteCityModel(base):
    __tablename__ = 'favorite_cities'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    city_name = Column(String, nullable=False)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)

    def __init__(self, user_id, city_name, lon, lat):
        self.user_id = user_id
        self.city_name = city_name
        self.lon = lon
        self.lat = lat