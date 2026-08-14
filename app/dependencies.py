from app.database import get_db_connection


def get_db():
    connection = get_db_connection()

    try:
        yield connection
    finally:
        connection.close()