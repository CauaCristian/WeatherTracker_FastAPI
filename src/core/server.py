from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.auth_controller import user_router
from src.api.v1.favorite_city_controller import favorite_city_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(favorite_city_router, prefix="/api/v1/favorite_city",tags=["favorite_city"])
