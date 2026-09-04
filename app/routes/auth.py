from fastapi import APIRouter, Depends

from app.schemas import (
    RegisterUser,
    LoginUser,
    ForgotPasswordRequest,
    ResetPasswordRequest
)

from app.dependencies import (
    get_db,
    get_current_user
)

from app.services.auth_service import (
    register_user_service,
    login_user_service,
    get_profile_service,
    forgot_password_service,
    reset_password_service
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register_user(
    user: RegisterUser,
    db=Depends(get_db)
):
    return register_user_service(db,user)


@router.post("/login")
def login_user(
    user: LoginUser,
    db=Depends(get_db)
):
    return login_user_service(db, user)



@router.get("/profile")
def get_profile(
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    return get_profile_service(db, user_id)


# @router.post("/forgot-password")
# def forgot_password(
#     data: ForgotPasswordRequest,
#     db=Depends(get_db)
# ):
#     return forgot_password_service(db, data)



# @router.post("/reset-password")
# def reset_password(
#     data: ResetPasswordRequest,
#     db=Depends(get_db)
# ):
#     return reset_password_service(db, data)
