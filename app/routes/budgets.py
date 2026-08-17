from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_db, get_current_user
from app.schemas import BudgetCreate, BudgetUpdate


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
    cursor = db.cursor()

    try:
        # Check whether category exists
        cursor.execute(
            """
            SELECT id
            FROM categories
            WHERE id = %s
            """,
            (budget.category_id,)
        )

        category = cursor.fetchone()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        # Check duplicate budget
        cursor.execute(
            """
            SELECT id
            FROM budgets
            WHERE user_id = %s
            AND category_id = %s
            AND month = %s
            """,
            (
                user_id,
                budget.category_id,
                budget.month
            )
        )

        existing_budget = cursor.fetchone()

        if existing_budget:
            raise HTTPException(
                status_code=400,
                detail="Budget already exists for this category and month"
            )

        # Insert budget
        cursor.execute(
            """
            INSERT INTO budgets (
                user_id,
                category_id,
                amount,
                month,
                year
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                user_id,
                budget.category_id,
                budget.amount,
                budget.month,
                2026
            )
        )

        db.commit()

        budget_id = cursor.lastrowid

        return {
            "message": "Budget created successfully",
            "budget_id": budget_id
        }

    finally:
        cursor.close()


@router.get("")
def get_budgets(
    user_id: int = Depends(get_current_user),
    db = Depends(get_db)
):
    cursor = db.cursor(dictionary = True)
    try:
        cursor.execute(
            """
            SELECT 
            b.id, b.category_id,
            c.name as category_name,
            b.amount, b.month, b.year,
            b.created_at
            FROM  budgets b 
            JOIN categories c 
            ON b.category_id = c.id
            WHERE b.user_id = %s
            ORDER BY b.month
            """, (user_id,)
        )
        budgets = cursor.fetchall()
        return{
            "budgets": budgets
        }

    finally:
        cursor.close()



@router.get("/{budget_id}")
def get_budget(
    budget_id: int,
    user_id: int = Depends(get_current_user),
    db = Depends(get_db)
):
    cursor = db.cursor(dictionary = True)
    try:
        cursor.execute(
            """
            SELECT 
            b.id, b.category_id, c.name as category_name,
            b.amount, b.month, b.year, b.created_at
            FROM budgets b
            JOIN categories c ON b.category_id = c.id
            WHERE b.user_id = %s
            AND b.id = %s
            """,(user_id, budget_id)
        )
        budget = cursor.fetchone()

        if not budget:
            raise HTTPException(
                status_code=404,
                detail = "Budget not found"
            )
        
        return budget

    finally:
        cursor.close()


@router.put("/{budget_id}")
def update_budget(
    budget_id: int,
    budget: BudgetUpdate,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        # Check whether expense belongs to current user
        cursor.execute(
            """
            SELECT id
            FROM budgets
            WHERE id = %s AND user_id = %s
            """,
            (budget_id, user_id)
        )

        existing_budget = cursor.fetchone()

        if not existing_budget:
            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        # Check whether category exists
        cursor.execute(
            """
            SELECT id
            FROM categories
            WHERE id = %s
            """,
            (budget.category_id,)
        )

        category = cursor.fetchone()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        # Update expense
        cursor.execute(
            """
            UPDATE budgets
            SET
                category_id = %s,
                amount = %s,
                month = %s
            WHERE id = %s
            AND user_id = %s
            """,
            (
                budget.category_id,
                budget.amount,
                budget.month,
                budget_id,
                user_id
            )
        )

        db.commit()

        return {
            "message": "Budget updated successfully",
            "expense_id": budget_id
        }

    finally:
        cursor.close()


@router.delete("/{budget_id}")
def delete_expense(
    budget_id: int,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        # Check whether expense belongs to current user
        cursor.execute(
            """
            SELECT id
            FROM Budgets
            WHERE id = %s
            AND user_id = %s
            """,
            (budget_id, user_id)
        )

        existing_budget = cursor.fetchone()

        if not existing_budget:
            raise HTTPException(
                status_code=404,
                detail="Budget not found"
            )

        # Delete expense
        cursor.execute(
            """
            DELETE FROM budgets
            WHERE id = %s
            AND user_id = %s
            """,
            (budget_id, user_id)
        )

        db.commit()

        return {
            "message": "Budget deleted successfully"
        }

    finally:
        cursor.close()