import os
from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()


class Settings:
    def __init__(self):
        self.API_ID = os.environ.get("API_ID")
        self.API_HASH = os.environ.get("API_HASH")
        self.MY_USER_ID = os.environ.get("MY_USER_ID")
        self.DB_HOST = os.environ.get("DB_HOST")
        self.DB_PORT = os.environ.get("DB_PORT")
        self.DB_NAME = os.environ.get("DB_NAME")
        self.DB_USER = os.environ.get("DB_USER")
        self.DB_PASS = os.environ.get("DB_PASS")
        self.db_url = (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
app = Client("my_account", api_id=settings.API_ID, api_hash=settings.API_HASH)
