from fastapi import APIRouter

from src.app.schemas.auth_schema import AuthResponse, Signin
from src.app.schemas.user_schema import UserResponse, UserCreate
from src.app.services.auth_service import AuthService
from src.app.services.user_service import UserService

user_router = APIRouter()
user_service = UserService()
auth_service = AuthService()
@user_router.post("/signup", response_model=UserResponse,status_code=201)
async def create_user(user:UserCreate):
    return user_service.create_user(user)

@user_router.post("/signin", response_model=AuthResponse,status_code=200)
async def signin_user(auth: Signin):
    return auth_service.signin_user(auth)