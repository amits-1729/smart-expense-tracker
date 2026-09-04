import pymysql
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SECRET_KEY: str
    # EMAIL_ADDRESS: str
    # EMAIL_APP_PASSWORD: str
    # FRONTEND_URL: str

    class Config:
        env_file = ".env"


settings = Settings()

def get_db_connection():

    conn = pymysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4",
        connect_timeout=10
    )

    return conn



# if __name__ == "__main__":
#     try:
#         conn = get_db_connection()
#         if conn:
#             print("MYSQL connection is successful")
#         cursor = conn.cursor()
#         cursor.execute("SELECT VERSION() AS version")

#         print(cursor.fetchone())

#         cursor.close()
#         conn.close()

#     except Exception as e:
#         print(f"Error: {e}")
