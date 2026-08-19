from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_db, get_current_user
from app.schemas import ExpenseCreate, ExpenseUpdate


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@router.post("")
def create_expense(
    expense: ExpenseCreate,
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
            (expense.category_id,)
        )

        category = cursor.fetchone()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        # Insert expense
        cursor.execute(
            """
            INSERT INTO expenses (
                user_id,
                category_id,
                amount,
                description,
                expense_date,
                payment_method
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                user_id,
                expense.category_id,
                expense.amount,
                expense.description,
                expense.expense_date,
                expense.payment_method
            )
        )

        db.commit()

        expense_id = cursor.lastrowid

        return {
            "message": "Expense created successfully",
            "expense_id": expense_id
        }

    finally:
        cursor.close()


@router.get("")
def get_expenses(
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            SELECT
                e.id,
                e.category_id,
                c.name AS category_name,
                e.amount,
                e.description,
                e.expense_date,
                e.payment_method,
                e.created_at
            FROM expenses e
            JOIN categories c
                ON e.category_id = c.id
            WHERE e.user_id = %s
            ORDER BY e.expense_date DESC, e.id DESC
            """,
            (user_id,)
        )

        expenses = cursor.fetchall()

        return {
            "expenses": expenses
        }

    finally:
        cursor.close()


@router.get("/{expense_id}")
def get_expense(
    expense_id: int,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            SELECT
                e.id,
                e.category_id,
                c.name AS category_name,
                e.amount,
                e.description,
                e.expense_date,
                e.payment_method,
                e.created_at
            FROM expenses e
            JOIN categories c
                ON e.category_id = c.id
            WHERE e.id = %s
            AND e.user_id = %s
            """,
            (expense_id, user_id)
        )

        expense = cursor.fetchone()

        if not expense:
            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        return expense

    finally:
        cursor.close()


@router.put("/{expense_id}")
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        # Check whether expense belongs to current user
        cursor.execute(
            """
            SELECT id
            FROM expenses
            WHERE id = %s
            AND user_id = %s
            """,
            (expense_id, user_id)
        )

        existing_expense = cursor.fetchone()

        if not existing_expense:
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
            (expense.category_id,)
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
            UPDATE expenses
            SET
                category_id = %s,
                amount = %s,
                description = %s,
                expense_date = %s,
                payment_method = %s
            WHERE id = %s
            AND user_id = %s
            """,
            (
                expense.category_id,
                expense.amount,
                expense.description,
                expense.expense_date,
                expense.payment_method,
                expense_id,
                user_id
            )
        )

        db.commit()

        return {
            "message": "Expense updated successfully",
            "expense_id": expense_id
        }

    finally:
        cursor.close()


@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        # Check whether expense belongs to current user
        cursor.execute(
            """
            SELECT id
            FROM expenses
            WHERE id = %s
            AND user_id = %s
            """,
            (expense_id, user_id)
        )

        existing_expense = cursor.fetchone()

        if not existing_expense:
            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        # Delete expense
        cursor.execute(
            """
            DELETE FROM expenses
            WHERE id = %s
            AND user_id = %s
            """,
            (expense_id, user_id)
        )

        db.commit()

        return {
            "message": "Expense deleted successfully"
        }

    finally:
        cursor.close()