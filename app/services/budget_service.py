from fastapi import HTTPException
from app.schemas import BudgetCreate, BudgetFilter, BudgetUpdate
from app.repositories.category_repository import get_category
from app.repositories.budget_repository import get_budget, create_budget, get_budgets, get_budget_by_id, update_budget, delete_budget, get_budget_status




def create_budget_service(
    db,
    user_id,
    budget: BudgetCreate,
):
    
    cursor = db.cursor()

    try:
        # Check whether category exists
        category = get_category(cursor, user_id, budget.category_id)
        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        # Check duplicate budget
        existing_budget = get_budget(cursor, user_id, budget.month, budget.category_id)
        if existing_budget:
            raise HTTPException(
                status_code=400,
                detail="Budget already exists for this category and month"
            )

        # Insert budget
        budget_id = create_budget(cursor, user_id, budget.month, budget.category_id, budget.amount)

        db.commit()
        return {
            "message": "Budget created successfully",
            "budget_id": budget_id
        }

    except Exception:
        db.rollback()
        raise
                
    finally:
        cursor.close()



def get_budgets_service(
    db,
    user_id: int,
    data: BudgetFilter
):
    cursor = db.cursor()

    try:

        budgets = get_budgets(cursor, user_id, data)
        return {
            "budgets": budgets
        }

    finally:
        cursor.close()


def get_budget_service(
    db,
    user_id: int,
    budget_id: int,
):
    cursor = db.cursor()
    try:

        budget = get_budget_by_id(cursor, user_id, budget_id)
        if not budget:
            raise HTTPException(
                status_code=404,
                detail = "Budget not found"
            )
        
        return budget

    finally:
        cursor.close()



def update_budget_service(
    db,
    user_id: int,
    budget_id: int,
    budget: BudgetUpdate
):
    cursor = db.cursor()

    try:
        # Check whether budget belongs to current user
        existing_budget = get_budget_by_id(cursor, user_id, budget_id)
        if not existing_budget:
            raise HTTPException(
                status_code=404,
                detail="Budget not found"
            )

        # Check whether category exists
        category = get_category(cursor, user_id, budget.category_id)
        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        # Update expense
        update_budget(cursor, user_id, budget_id, budget)

        db.commit()
        return {
            "message": "Budget updated successfully",
            "expense_id": budget_id
        }

    except Exception:
        db.rollback()
        raise
                
    finally:
        cursor.close()



def delete_budget_service(
    db,
    user_id: int,
    budget_id: int
):
    cursor = db.cursor()

    try:
        # Check whether budget belongs to current user
        existing_budget = get_budget_by_id(cursor, user_id, budget_id)
        if not existing_budget:
            raise HTTPException(
                status_code=404,
                detail="Budget not found"
            )

        # Delete budget
        delete_budget(cursor, user_id, budget_id)
        
        db.commit()
        return {
            "message": "Budget deleted successfully"
        }

    except Exception:
        db.rollback()
        raise
                
    finally:
        cursor.close()





def get_budget_status_service(
    db,
    user_id: int,
    month: int,
    year: int
):
    cursor = db.cursor()

    try:

        budgets = get_budget_status(
            cursor,
            user_id,
            month,
            year
        )

        result = []

        for budget in budgets:

            budget_amount = budget["budget"]
            spent = budget["spent"] or 0

            remaining = budget_amount - spent

            if budget_amount > 0:
                percentage_used = round(
                    (spent / budget_amount) * 100,
                    2
                )
            else:
                percentage_used = 0

            if percentage_used >= 100:
                status = "EXCEEDED"

            elif percentage_used >= 80:
                status = "WARNING"

            else:
                status = "SAFE"

            result.append({
                "category_id": budget["category_id"],
                "category_name": budget["category_name"],
                "budget": budget_amount,
                "spent": spent,
                "remaining": remaining,
                "percentage_used": percentage_used,
                "status": status
            })

        return {
            "month": month,
            "year": year,
            "budgets": result
        }

    finally:
        cursor.close()