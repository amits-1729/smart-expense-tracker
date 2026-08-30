from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated

from app.dependencies import get_db, get_current_user
from app.schemas import BudgetCreate, BudgetUpdate, BudgetFilter

from app.services.budget_service import create_budget_service, get_budgets_service, get_budget_service, update_budget_service, delete_budget_service, get_budget_status_service


router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)


@router.post("")
def create_budget(
    budget: BudgetCreate,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    return create_budget_service(
        db,
        user_id,
        budget
    )
 


@router.get("")
def get_budgets(
    data: Annotated[BudgetFilter, Query()],
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    return get_budgets_service(
        db,
        user_id,
        data
    )



@router.get("/status")
def get_budget_status(
    month: int,
    year: int,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    return get_budget_status_service(
        db,
        user_id,
        month,
        year
    )



@router.get("/{budget_id}")
def get_budget(
    budget_id: int,
    user_id: int = Depends(get_current_user),
    db = Depends(get_db)
):
    return get_budget_service(db, user_id, budget_id)



    
@router.put("/{budget_id}")
def update_budget(
    budget_id: int,
    budget: BudgetUpdate,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    return update_budget_service(
        db,
        user_id,
        budget_id,
        budget
    )


    


@router.delete("/{budget_id}")
def delete_expense(
    budget_id: int,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    return delete_budget_service(
        db,
        user_id,
        budget_id
    )

