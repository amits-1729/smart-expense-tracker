from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_db, get_current_user
from app.schemas import CategoryCreate
from app.services.category_service import create_category_service, get_categories_service, get_category_service, update_category_service, delete_category_service


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("")
def create_category(
    category: CategoryCreate,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    return create_category_service(
        db,
        user_id,
        category
    )


@router.get("")
def get_categories(
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    return get_categories_service(db,user_id)



@router.get("/{category_id}")
def get_category(
    category_id: int,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    return get_category_service(db,user_id,category_id)



@router.put("/{category_id}")
def update_category(
    category_id: int,
    category: CategoryCreate,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    return update_category_service(
        db,
        user_id,
        category_id,
        category
    )



@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    return delete_category_service(
        db,
        user_id,
        category_id
    )
