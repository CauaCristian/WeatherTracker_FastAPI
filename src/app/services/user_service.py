from src.app.repositories.user_repository import UserRepository
from src.app.schemas.user_schema import UserCreate, UserResponse
from fastapi import HTTPException
from src.app.models.user_model import UserModel

from src.core.security.bcrypt import Bcrypt

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.bcrypt = Bcrypt()

    def create_user(self, user: UserCreate):
        try:
            new_user = UserModel(**user.model_dump())
            new_user.password = self.bcrypt.hash_password(new_user.password)
            created_user = self.user_repository.user_create(new_user)
            return UserResponse.from_orm(created_user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))