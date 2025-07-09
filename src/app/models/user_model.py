from sqlalchemy import Column, Integer, String
from src.core.database.postgres import base

class UserModel(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True,nullable=False)
    username = Column(String, unique=True, index=True,nullable=False)
    email = Column(String, unique=True, index=True,nullable=False)
    password = Column(String,nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password