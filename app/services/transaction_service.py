from fastapi import HTTPException

from app.schemas import TransactionCreate, TransactionFilter, TransactionUpdate
from app.repositories.transaction_repository import (
    get_category, get_account, create_transaction, update_account_balance,
    get_transactions, get_transaction, update_transaction, delete_transaction
)


def create_transaction_service(
    db,
    user_id: int,
    transaction: TransactionCreate
):
    cursor = db.cursor()

    try:
        if transaction.type == "EXPENSE":
            category = get_category(cursor,transaction.category_id)
            if not category: 
                raise HTTPException(
                    status_code=404,
                    detail="Category not found" 
                )
        account = get_account(cursor, transaction.account_id, user_id)
        if not account: 
            raise HTTPException(
                status_code=404,
                detail="Account not found" 
            )
        
        txn_id = create_transaction( cursor, user_id, transaction)
        update_account_balance(cursor, user_id, transaction.account_id, transaction.amount, transaction.type )

        db.commit()
        return {
            "message": "Transaction added successfully",
            "transaction_id": txn_id
        }
    
    except Exception:
        db.rollback()
        raise
    
    finally:
        cursor.close()




def get_transactions_service(
    db,
    user_id: int,
    data: TransactionFilter
):
    cursor = db.cursor()

    try:
        transactions = get_transactions(cursor,user_id, data)

        return {
            "transactions": transactions
        }

    finally:
        cursor.close()



def get_transaction_service(
    db,
    user_id: int,
    transaction_id: int,
):
    cursor = db.cursor()
    try:
        transaction = get_transaction(cursor, user_id, transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        return {
            "transaction": transaction
        }

    finally:
        cursor.close()


def update_transaction_service(
    db,
    user_id,
    transaction_id,
    transaction: TransactionUpdate
):
    cursor = db.cursor()
    try:
        existing_transaction = get_transaction(cursor, user_id, transaction_id)
        if not existing_transaction:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )
        
        if transaction.type == "EXPENSE":
            category = get_category(cursor, transaction.category_id)
            if not category: 
                raise HTTPException(
                    status_code=404,
                    detail="Category not found" 
                )

        account = get_account(cursor, transaction.account_id, user_id)
        if not account: 
            raise HTTPException(
                status_code=404,
                detail="Account not found" 
            )

        txn_id = update_transaction(cursor, user_id, transaction_id, transaction)

        update_account_balance(cursor, user_id, existing_transaction["account_id"], -existing_transaction["amount"], existing_transaction["type"])

        update_account_balance(cursor, user_id, transaction.account_id, transaction.amount, transaction.type )
        
        db.commit()
        return {
            "message": "Transaction updated successfully",
            "transaction_id": txn_id
        }


    except Exception:
        db.rollback()
        raise
        
    finally:
        cursor.close()


def delete_transaction_service(
    db,
    user_id,
    transaction_id
):
    cursor = db.cursor()
    try:
        existing_transaction = get_transaction(cursor, user_id, transaction_id)
        if not existing_transaction:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )
        
        delete_transaction(cursor, user_id, transaction_id)

        update_account_balance(cursor, user_id, existing_transaction["account_id"], -existing_transaction["amount"], existing_transaction["type"])

        db.commit()
        return {
            "message": "Transaction deleted successfully"
        }

    except Exception:
            db.rollback()
            raise
            
    finally:
        cursor.close()
    