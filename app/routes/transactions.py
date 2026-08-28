from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated

from app.dependencies import get_db, get_current_user
from app.schemas import TransactionCreate, TransactionFilter, TransactionUpdate


router = APIRouter(
    prefix="/transactions",
    tags = ["Transactions"]
)


@router.post("")
def create_transaction(
    txn: TransactionCreate,
    user_id: int = Depends(get_current_user),
    db = Depends(get_db)
):
    cursor = db.cursor()

    try:
        if txn.type == "EXPENSE":
            cursor.execute(
                """
                SELECT id
                FROM categories
                WHERE id = %s
                """,
                (txn.category_id,)
            )

            category = cursor.fetchone()

            if not category:
                raise HTTPException(
                    status_code=404,
                    detail="Category not found"
                )

        cursor.execute(
            """
            SELECT id
            FROM accounts
            WHERE id = %s
            """,
            (txn.account_id,)
        )

        account = cursor.fetchone()

        if not account:
            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        query = """
                INSERT INTO transactions (
                user_id, account_id, category_id, type, amount, description, transaction_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        params = [user_id, txn.account_id, txn.category_id, txn.type, txn.amount, txn.description, txn.transaction_date]

        cursor.execute(query,params)

        if txn.type == 'EXPENSE':
            cursor.execute("UPDATE accounts SET balance = balance-%s WHERE id = %s AND user_id = %s",(txn.amount,txn.account_id,user_id))
        else:
            cursor.execute("UPDATE accounts SET balance = balance+%s WHERE id = %s AND user_id = %s",(txn.amount,txn.account_id,user_id))

        db.commit()

        txn_id = cursor.lastrowid

        return {
            "message": "Transaction added successfully",
            "transaction_id" : txn_id
        }

    finally:
        cursor.close()


@router.get("")
def get_transactions(
    data : Annotated[TransactionFilter,Query()],
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    cursor = db.cursor()
    try:

        query = """
                SELECT
                t.id, t.category_id, c.name AS category_name,
                t.account_id, a.name AS account_name,
                t.type, t.amount, t.description, t.transaction_date,
                t.created_at
                FROM transactions t LEFT JOIN categories c
                ON t.category_id = c.id
                JOIN accounts a
                ON t.account_id = a.id
                WHERE t.user_id = %s
                """

        params = [user_id]

        if(data.start_date):
            query += " AND t.transaction_date >= %s"
            params.append(data.start_date)

        if(data.end_date):
            query += " AND t.transaction_date <= %s"
            params.append(data.end_date)

        if(data.min_amount):
            query += " AND t.amount >= %s"
            params.append(data.min_amount)

        if(data.max_amount):
            query += " AND t.amount <= %s"
            params.append(data.max_amount)

        if(data.account_id):
            query += " AND t.account_id = %s"
            params.append(data.account_id)
            
        if(data.category_id):
            query += " AND t.category_id = %s"
            params.append(data.category_id)

        if(data.type):
            query += " AND t.type = %s"
            params.append(data.type)

        query += " ORDER BY t.transaction_date DESC"

        cursor.execute(query,params)
        transaction = cursor.fetchall()
        return {
            "transaction": transaction
        }

    finally:
        cursor.close()


@router.get("/{transaction_id}")
def get_transaction(
    transaction_id: int,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            SELECT
            t.id, t.category_id, c.name AS category_name,
            t.account_id, a.name AS payment_method,
            t.type, t.amount, t.description, t.transaction_date,
            t.created_at
            FROM transactions t LEFT JOIN categories c
            ON t.category_id = c.id
            JOIN accounts a
            ON t.account_id = a.id
            WHERE t.id = %s
            AND t.user_id = %s
            """,
            (transaction_id, user_id)
        )

        transaction = cursor.fetchone()

        if not transaction:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        return transaction

    finally:
        cursor.close()


@router.put("/{transaction_id}")
def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        # Check whether transaction belongs to current user
        cursor.execute(
            """
            SELECT account_id, type, amount
            FROM transactions
            WHERE id = %s
            AND user_id = %s
            """,
            (transaction_id, user_id)
        )

        existing_transaction = cursor.fetchone()

        if not existing_transaction:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        # Check whether category exists
        if transaction.type == "EXPENSE":
            cursor.execute(
                """
                SELECT id
                FROM categories
                WHERE id = %s
                """,
                (transaction.category_id,)
            )

            category = cursor.fetchone()

            if not category:
                raise HTTPException(
                    status_code=404,
                    detail="Category not found"
                )

        cursor.execute(
            """
            SELECT id
            FROM accounts
            WHERE id = %s AND user_id = %s
            """,
            (transaction.account_id,user_id)
        )

        account = cursor.fetchone()

        if not account:
            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        # Update expense
        cursor.execute(
            """
            UPDATE transactions
            SET
                category_id = %s,
                amount = %s,
                description = %s,
                transaction_date = %s,
                account_id = %s,
                type = %s
            WHERE id = %s
            AND user_id = %s
            """,
            (
                transaction.category_id,
                transaction.amount,
                transaction.description,
                transaction.transaction_date,
                transaction.account_id,
                transaction.type,
                transaction_id,
                user_id
            )
        )

        if existing_transaction["type"] == 'EXPENSE':
            cursor.execute("UPDATE accounts SET balance = balance+%s WHERE id = %s AND user_id = %s",(existing_transaction["amount"],existing_transaction["account_id"],user_id))
        else:
            cursor.execute("UPDATE accounts SET balance = balance-%s WHERE id = %s AND user_id = %s",(existing_transaction["amount"],existing_transaction["account_id"],user_id))

        if transaction.type == "EXPENSE":
            cursor.execute("UPDATE accounts SET balance = balance-%s WHERE id = %s AND user_id = %s",(transaction.amount,transaction.account_id,user_id))
        else:
            cursor.execute("UPDATE accounts SET balance = balance+%s WHERE id = %s AND user_id = %s",(transaction.amount,transaction.account_id,user_id))

        db.commit()

        return {
            "message": "Transaction updated successfully",
            "transaction_id": transaction_id
        }

    finally:
        cursor.close()


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    cursor = db.cursor()

    try:
        # Check whether transaction belongs to current user
        cursor.execute(
            """
            SELECT account_id, type, amount
            FROM transactions
            WHERE id = %s
            AND user_id = %s
            """,
            (transaction_id, user_id)
        )

        existing_transaction = cursor.fetchone()

        if not existing_transaction:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        # Delete expense
        cursor.execute(
            """
            DELETE FROM transactions
            WHERE id = %s
            AND user_id = %s
            """,
            (transaction_id, user_id)
        )

        if existing_transaction["type"] == 'EXPENSE':
            cursor.execute("UPDATE accounts SET balance = balance+%s WHERE id = %s AND user_id = %s",(existing_transaction["amount"],existing_transaction["account_id"],user_id))
        else:
            cursor.execute("UPDATE accounts SET balance = balance-%s WHERE id = %s AND user_id = %s",(existing_transaction["amount"],existing_transaction["account_id"],user_id))

        db.commit()

        return {
            "message": "Transaction deleted successfully"
        }

    finally:
        cursor.close()