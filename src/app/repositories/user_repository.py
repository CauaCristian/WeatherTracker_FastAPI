from src.app.models.user_model import UserModel
from src.core.database.postgres import PostgresDatabase
from fastapi import HTTPException

class UserRepository:
    def __init__(self):
        self.db = PostgresDatabase()
        self.session = self.db.get_session()

    def user_create(self, user:UserModel):
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            self.session.close()

    def get_user_by_email(self, email: str) -> UserModel:
        try:
            user = self.session.query(UserModel).filter(UserModel.email == email).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            self.session.close()