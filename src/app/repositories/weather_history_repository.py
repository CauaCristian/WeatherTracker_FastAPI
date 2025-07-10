from src.core.database.postgres import PostgresDatabase
from fastapi import HTTPException
from src.app.models.weather_history_model import WeatherHistoryModel

class WeatherHistoryRepository:
    def __init__(self):
        self.db = PostgresDatabase()
        self.session = self.db.get_session()

    def get_weather_history(self, city_name: str) -> list[WeatherHistoryModel]:
        try:
            weather_history = self.session.query(WeatherHistoryModel).filter(WeatherHistoryModel.city_name == city_name).all()
            if not weather_history:
                raise HTTPException(status_code=404, detail="Weather history not found")
            return weather_history
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            self.session.close()

    def add_weather_history(self, weather_history: WeatherHistoryModel) -> WeatherHistoryModel:
        try:
            self.session.add(weather_history)
            self.session.commit()
            self.session.refresh(weather_history)
            return weather_history
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            self.session.close()