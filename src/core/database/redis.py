import redis.asyncio as redis
from dotenv import load_dotenv
import os

load_dotenv()

class RedisDatabase:
    def __init__(self):
        self.port = int(os.getenv('REDIS_PORT'))
        self.host = os.getenv('REDIS_HOST')
        self.db = os.getenv('REDIS_DB')
        self.client = redis.Redis(host=self.host, port=self.port, db=self.db)

    def get_client(self):
        return self.client