from fastapi import HTTPException

from app.schemas import CategoryCreate
from app.repositories.category_repository import get_categories, create_category, get_category, update_category, delete_category



def create_category_service(
    db,
    user_id,
    category: CategoryCreate
):
    cursor = db.cursor()
    try:
        existing_category  = get_categories(cursor,user_id,category.name)
        
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
        category = get_category(cursor, user_id, category_id)
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
        existing_category = get_category(cursor, user_id, category_id)
        if not existing_category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        duplicate_category = get_categories(cursor, user_id, category.name)
        if duplicate_category:
            raise HTTPException(
                status_code=400,
                detail="Category already exists"
            )

        update_category(cursor, category_id, category.name)

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

        existing_category = get_category(cursor, user_id, category_id)
        if not existing_category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
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