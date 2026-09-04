import pymysql
from fastapi import HTTPException

from app.schemas import (
    RegisterUser,
    LoginUser,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from app.repositories.auth_repository import (
    get_user,
    register_user,
    get_user_by_id,
    reset_password
)

from app.utils.security import (
    hash_password, verify_password, create_access_token, create_password_reset_token, decode_password_reset_token
)

from app.database import settings

from app.utils.email_utils import send_reset_email




def register_user_service(
    db,
    user: RegisterUser
):
    cursor = db.cursor()
    try:
        existing_user = get_user(cursor, user.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        hashed_password = hash_password(user.password)

        register_user(cursor, user, hashed_password)
        db.commit()

        return {
            "message": "User registered successfully"
        }

    except pymysql.MySQLError:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

    finally:
        cursor.close()



def login_user_service(
    db,
    user: LoginUser
):
    cursor = db.cursor()
    try:
        existing_user = get_user(cursor,user.email)
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



def get_profile_service(
    db,
    user_id: int
):
    cursor = db.cursor()

    try:
        user = get_user_by_id(cursor, user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    finally:
        cursor.close()



def forgot_password_service(
    db,
    data: ForgotPasswordRequest
):

    cursor = db.cursor()
    try:
        user = get_user(cursor, data.email)
        if user:
            reset_token = create_password_reset_token(
                user["id"]
            )

            reset_link = (
                f"{settings.FRONTEND_URL}"
                f"?token={reset_token}"
            )
            send_reset_email(
                user["email"],
                reset_link
            )

            # print("PASSWORD RESET LINK:")
            # print(reset_link)

        return {
            "message": (
                "If an account exists with this email, "
                "a password reset link has been sent."
            )
        }

    finally:
        cursor.close()



def reset_password_service(
    db,
    data: ResetPasswordRequest
):

    try:
        user_id = decode_password_reset_token(
            data.token
        )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token"
        )

    cursor = db.cursor()

    try:
        user = get_user_by_id(cursor, user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        hashed_password = hash_password(data.new_password)
        reset_password(cursor, user_id, hashed_password)

        db.commit()
        return {
            "message": "Password reset successfully"
        }

    except:
        db.rollback()
        raise

    finally:
        cursor.close()