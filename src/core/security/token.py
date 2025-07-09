from dotenv import load_dotenv
from jose import jwt
import os
from datetime import datetime, timedelta, timezone
from src.app.models.user_model import UserModel

load_dotenv()

class Token:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.expiration_time = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS"))
        self.jwt = jwt

    def create_access_token(self, user: UserModel) -> str:
        data = {
            "sub": user.id,
            "exp": datetime.now(timezone.utc) + timedelta(days=self.expiration_time)
        }
        return self.jwt.encode(data, self.secret_key, algorithm=self.algorithm)
    def verify_token(self, token):
        try:
            payload = self.jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except Exception as e:
            from fastapi import HTTPException
            raise HTTPException(status_code=401, detail="Invalid token") from e