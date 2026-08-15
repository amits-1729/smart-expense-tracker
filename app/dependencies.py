from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import get_db_connection
from app.utils.security import decode_access_token

security = HTTPBearer()

def get_db():
    connection = get_db_connection()

    try:
        yield connection
    finally:
        connection.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        user_id = decode_access_token(token)
        return user_id

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )