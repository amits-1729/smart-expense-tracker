import pymysql

from dbutils.pooled_db import PooledDB
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SECRET_KEY: str
    EMAIL_ADDRESS: str
    EMAIL_APP_PASSWORD: str
    FRONTEND_URL: str

    class Config:
        env_file = ".env"


settings = Settings()


pool = PooledDB(
    creator=pymysql,
    maxconnections=10,
    blocking=True,

    host=settings.DB_HOST,
    port=settings.DB_PORT,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME,

    cursorclass=pymysql.cursors.DictCursor,
    charset="utf8mb4",
    connect_timeout=10
)


def get_db_connection():
    return pool.connection()