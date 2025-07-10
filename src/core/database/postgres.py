from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

base = declarative_base()

load_dotenv()

class PostgresDatabase:
    def __init__(self):
        self.engine = create_engine(os.getenv("POSTGRES_URL"))
        self.session = sessionmaker(autoflush=False, autocommit= False,bind=self.engine)

    def get_session(self):
        return self.session()