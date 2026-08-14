import mysql.connector
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()



def get_db_connection():
    conn = mysql.connector.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME
    )
    return conn


# if __name__ == "__main__":
#     conn = get_db_connection()
#     if conn.is_connected():
#         print("MYSQL connection is successful")
#     conn.close()