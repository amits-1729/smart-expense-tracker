from fastapi import HTTPException
from app.schemas import AccountCreate
from app.repositories.account_repository import create_account, get_accounts



def create_account_service(
    db,
    user_id,
    data: AccountCreate
):
    cursor = db.cursor()

    try:
        account = get_accounts(cursor, user_id, data.name)
        if account:
            raise HTTPException(
                status_code=400,
                detail = "Account already exist"
            )

        account_id = create_account(cursor, user_id, data.name)
        
        db.commit()

        return {
            "message": "Account created successfully",
            "account_id": account_id
        }

    except Exception:
        db.rollback()
        raise
                
    finally:
        cursor.close()



def get_accounts_service(
    db,
    user_id
):
    cursor = db.cursor()
    try:
        accounts = get_accounts(cursor, user_id)
        return {
            "accounts":accounts
        }

    finally:
        cursor.close()