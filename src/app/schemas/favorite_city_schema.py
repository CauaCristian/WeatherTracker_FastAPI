from pydantic import BaseModel


class FavoriteCityCreate(BaseModel):
    user_id: int
    city_name: str

class FavoriteCityResponse(BaseModel):
    id: int
    user_id: int
    city_name: str
    lon: float
    lat: float
    model_config = {'from_attributes': True}

