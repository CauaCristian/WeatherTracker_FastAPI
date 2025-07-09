from src.app.models.favorite_city_model import FavoriteCityModel
from src.core.database.postgres import PostgresDatabase
class FavoriteCityRepository:
    def __init__(self):
        self.db = PostgresDatabase()
        self.session = self.db.get_session()

    def add_favorite_city(self, favorite_city:FavoriteCityModel)-> FavoriteCityModel:
        try:
            self.session.add(favorite_city)
            self.session.commit()
            self.session.refresh(favorite_city)
            return favorite_city
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error adding favorite city: {str(e)}")
        finally:
            self.session.close()

    def get_favorite_cities_by_user_id(self, user_id: int) -> list[FavoriteCityModel]:
        try:
            favorite_cities = self.session.query(FavoriteCityModel).filter(FavoriteCityModel.user_id == user_id).all()
            return favorite_cities
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error retrieving favorite cities: {str(e)}")
        finally:
            self.session.close()

    def delete_favorite_city(self, city_id: int):
        try:
            city = self.session.query(FavoriteCityModel).filter(FavoriteCityModel.id == city_id).first()
            if not city:
                raise Exception("City not found")
            self.session.delete(city)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error deleting favorite city: {str(e)}")
        finally:
            self.session.close()