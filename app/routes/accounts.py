from fastapi import APIRouter, Depends, HTTPException

from app.schemas import AccountCreate
from app.dependencies import get_current_user, get_db
from app.services.account_service import create_account_service, get_accounts_service

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

@router.post("")
def create_account(
    data: AccountCreate,
    user_id: int = Depends(get_current_user),
    db = Depends(get_db)
):
    return create_account_service(db, user_id, data)



@router.get("")
def get_account(
    user_id: int = Depends(get_current_user),
    db = Depends(get_db)
):
    return get_accounts_service(
        db,
        user_id
    )
