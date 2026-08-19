from fastapi import APIRouter, Depends, HTTPException
import mysql.connector

from app.schemas import RegisterUser, LoginUser
from app.dependencies import get_db, get_current_user
from app.utils.security import hash_password, verify_password, create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register_user(user: RegisterUser, db=Depends(get_db)):
    cursor = db.cursor()

    try:
        # Check whether email already exists
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (user.email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = hash_password(user.password)

        # Insert user
        cursor.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
            """,
            (user.name, user.email, hashed_password)
        )

        db.commit()

        return {
            "message": "User registered successfully"
        }

    except mysql.connector.Error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

    finally:
        cursor.close()


@router.post("/login")
def login_user(user: LoginUser,db=Depends(get_db)):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            SELECT id, name, email, password
            FROM users
            WHERE email = %s
            """,(user.email,)
        )

        existing_user = cursor.fetchone()

        if not existing_user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        password_valid = verify_password(user.password, existing_user["password"])

        if not password_valid:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )
        access_token = create_access_token(existing_user["id"])
        return {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": existing_user["id"],
                "name": existing_user["name"],
                "email": existing_user["email"]
            }
        }

    finally:
        cursor.close()



@router.get("/profile")
def get_profile(user_id: int = Depends(get_current_user), db=Depends(get_db)):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            SELECT id, name, email, created_at
            FROM users
            WHERE id = %s
            """, (user_id,)
        )

        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    finally:
        cursor.close()