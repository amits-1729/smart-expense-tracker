from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_db, get_current_user
from app.schemas import CategoryCreate


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
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT id FROM categories WHERE name = %s",
            (category.name,)
        )

        existing_category = cursor.fetchone()

        if existing_category:
            raise HTTPException(
                status_code=400,
                detail="Category already exists"
            )

        cursor.execute(
            """
            INSERT INTO categories (name)
            VALUES (%s)
            """,
            (category.name,)
        )

        db.commit()

        category_id = cursor.lastrowid

        return {
            "message": "Category created successfully",
            "category_id": category_id,
            "name": category.name
        }

    finally:
        cursor.close()


@router.get("")
def get_categories(
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, name
            FROM categories
            ORDER BY name
            """
        )

        categories = cursor.fetchall()

        return {
            "categories": categories
        }

    finally:
        cursor.close()


@router.get("/{category_id}")
def get_category(
    category_id: int,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, name
            FROM categories
            WHERE id = %s
            """,
            (category_id,)
        )

        category = cursor.fetchone()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        return category

    finally:
        cursor.close()


@router.put("/{category_id}")
def update_category(
    category_id: int,
    category: CategoryCreate,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        # Check whether category exists
        cursor.execute(
            """
            SELECT id
            FROM categories
            WHERE id = %s
            """,
            (category_id,)
        )

        existing_category = cursor.fetchone()

        if not existing_category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        # Check duplicate category name
        cursor.execute(
            """
            SELECT id
            FROM categories
            WHERE name = %s AND id != %s
            """,
            (category.name, category_id)
        )

        duplicate_category = cursor.fetchone()

        if duplicate_category:
            raise HTTPException(
                status_code=400,
                detail="Category already exists"
            )

        # Update category
        cursor.execute(
            """
            UPDATE categories
            SET name = %s
            WHERE id = %s
            """,
            (category.name, category_id)
        )

        db.commit()

        return {
            "message": "Category updated successfully",
            "category_id": category_id,
            "name": category.name
        }

    finally:
        cursor.close()


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            SELECT id
            FROM categories
            WHERE id = %s
            """,
            (category_id,)
        )

        existing_category = cursor.fetchone()

        if not existing_category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        cursor.execute(
            """
            DELETE FROM categories
            WHERE id = %s
            """,
            (category_id,)
        )

        db.commit()

        return {
            "message": "Category deleted successfully"
        }

    finally:
        cursor.close()