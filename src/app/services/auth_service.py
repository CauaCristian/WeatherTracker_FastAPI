from fastapi import HTTPException

from src.app.repositories.user_repository import UserRepository
from src.app.schemas.auth_schema import Signin, AuthResponse
from src.core.security.bcrypt import Bcrypt
from src.core.security.token import Token


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.bcript = Bcrypt()
        self.token = Token()

    def signin_user(self, auth: Signin):
        try:
            user = self.user_repository.get_user_by_email(auth.email)
            if not self.bcript.verify_password(auth.password, user.password):
                raise HTTPException(status_code=400, detail="Invalid password")
            return AuthResponse(
                access_token=self.token.create_access_token(user)
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid credentials") from e