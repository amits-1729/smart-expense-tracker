from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated

from app.dependencies import get_db, get_current_user
from app.schemas import TransactionCreate, TransactionFilter, TransactionUpdate
from app.services.transaction_service import create_transaction_service, get_transactions_service, get_transaction_service, update_transaction_service, delete_transaction_service


router = APIRouter(
    prefix="/transactions",
    tags = ["Transactions"]
)


@router.post("")
def create_transaction(
    transaction: TransactionCreate,
    user_id: int = Depends(get_current_user),
    db = Depends(get_db)
):
    return create_transaction_service(
        db,
        user_id,
        transaction
    )



@router.get("")
def get_transactions(
    data : Annotated[TransactionFilter,Query()],
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    return get_transactions_service(
        db,
        user_id,
        data
    )
    


@router.get("/{transaction_id}")
def get_transaction(
    transaction_id: int,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    return get_transaction_service(
        db,
        user_id,
        transaction_id
    )
    


@router.put("/{transaction_id}")
def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    return update_transaction_service(
        db,
        user_id,
        transaction_id,
        transaction
    )



@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    return delete_transaction_service(
        db,
        user_id,
        transaction_id
    )
    