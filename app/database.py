import pymysql
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
    conn = pymysql.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn


if __name__ == "__main__":
    try:
        conn = get_db_connection()
        if conn:
            print("MYSQL connection is successful")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
