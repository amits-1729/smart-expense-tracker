from fastapi import APIRouter, Depends, HTTPException

from app.schemas import AccountCreate
from app.dependencies import get_current_user, get_db

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
    cursor = db.cursor()

    try:
        cursor.execute("SELECT id FROM accounts WHERE user_id = %s AND name = %s",(user_id, data.name))

        account = cursor.fetchone()
        if account:
            raise HTTPException(
                status_code=400,
                detail = "Account already exist"
            )

        query = "INSERT INTO accounts (user_id, name) VALUES (%s, %s);"
        params = [user_id, data.name]

        cursor.execute(query,params)
        db.commit()

        account_id = cursor.lastrowid
        return {
            "message": "Account created successfully",
            "account_id": account_id
        }

    finally:
        cursor.close()


@router.get("")
def get_account(
    user_id: int = Depends(get_current_user),
    db = Depends(get_db)
):
    cursor = db.cursor()
    try:
        query = """
                SELECT id, name, balance
                FROM accounts
                WHERE user_id = %s
                ORDER BY balance DESC
            """
        params = [user_id]

        cursor.execute(query,params)
        accounts = cursor.fetchall()
        return {
            "accounts":accounts
        }

    finally:
        cursor.close()