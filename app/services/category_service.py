from fastapi import HTTPException
from app.schemas import CategoryCreate

from app.repositories.transaction_repository import get_transaction_by_catgory

from app.repositories.budget_repository import get_budget_by_catgory

from app.repositories.category_repository import (
    get_category_by_name,
    get_categories,
    get_category_by_id,
    create_category, update_category, delete_category
)


def create_category_service(
    db,
    user_id,
    category: CategoryCreate
):
    cursor = db.cursor()
    try:
        existing_category  = get_category_by_name(cursor,user_id,category.name)
        if existing_category:
            raise HTTPException(
                status_code=400,
                detail="Category already exists"
            )
        category_id = create_category(cursor, user_id, category.name)

        db.commit()
        return {
            "message": "Category created successfully",
            "category_id": category_id,
            "name": category.name
        }

    except Exception:
        db.rollback()
        raise
                
    finally:
        cursor.close()


def get_categories_service(db, user_id):
    cursor = db.cursor()
    try:
        categories = get_categories(cursor, user_id)
        return {
            "categories": categories
        }

    finally:
        cursor.close()


def get_category_service(db, user_id, category_id):
    cursor = db.cursor()
    try:
        category = get_category_by_id(cursor, user_id, category_id)
        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        return {
            "category": category
        }

    finally:
        cursor.close()


def update_category_service(
    db,
    user_id,
    category_id,
    category: CategoryCreate
):
    cursor = db.cursor()

    try:
        existing_category = get_category_by_id(cursor, user_id, category_id)
        if not existing_category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        if existing_category["user_id"] is None:
            raise HTTPException(
                status_code=403,
                detail="Default categories can't be updated"
            )

        duplicate_category = get_category_by_name(cursor, user_id, category.name)
        if duplicate_category:
            raise HTTPException(
                status_code=400,
                detail="Category already exists"
            )

        update_category(cursor, user_id, category_id, category.name)

        db.commit()
        return {
            "message": "Category updated successfully",
            "category_id": category_id,
            "name": category.name
        }

    except Exception:
        db.rollback()
        raise
                
    finally:
        cursor.close()


def delete_category_service(
    db,
    user_id,
    category_id
):
    cursor = db.cursor()
    try:
        existing_category = get_category_by_id(cursor, user_id, category_id)
        if not existing_category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        if existing_category["user_id"] is None:
            raise HTTPException(
                status_code=403,
                detail="Default categories can't be deleted"
            )

        any_transaction = get_transaction_by_catgory(cursor, user_id, category_id)
        if any_transaction:
            raise HTTPException(
                status_code=403,
                detail="Category can't be deleted because you have transaction with this category"
            )

        any_budget = get_budget_by_catgory(cursor, user_id, category_id)
        if any_budget:
            raise HTTPException(
                status_code=403,
                detail="Category can't be deleted because you have budget with this category"
            )

        delete_category(cursor, user_id, category_id)

        db.commit()
        return {
            "message": "Category deleted successfully"
        }

    except Exception:
        db.rollback()
        raise
                
    finally:
        cursor.close()