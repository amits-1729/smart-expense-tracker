from app.schemas import TransactionCreate, TransactionFilter, TransactionUpdate



def create_transaction(
    cursor,
    user_id,
    transaction: TransactionCreate
):

    query = """
        INSERT INTO transactions (
        user_id, account_id, category_id, type, amount,
        description, transaction_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    params = (
        user_id,
        transaction.account_id,
        transaction.category_id,
        transaction.type,
        transaction.amount,
        transaction.description,
        transaction.transaction_date
    )

    cursor.execute(query, params)
    return cursor.lastrowid




def get_transactions(
    cursor,
    user_id,
    data: TransactionFilter
):

    query = """
        SELECT
        t.id, t.category_id, c.name AS category_name,
        t.account_id, a.name AS account_name,
        t.type, t.amount, t.description,
        t.transaction_date,t.created_at

        FROM transactions t
        LEFT JOIN categories c
        ON t.category_id = c.id
        JOIN accounts a
        ON t.account_id = a.id
        WHERE t.user_id = %s
        AND (c.user_id = %s OR c.user_id IS NULL)
    """

    params = [user_id, user_id]

    if data.start_date:
        query += " AND t.transaction_date >= %s"
        params.append(data.start_date)

    if data.end_date:
        query += " AND t.transaction_date <= %s"
        params.append(data.end_date)

    if data.min_amount:
        query += " AND t.amount >= %s"
        params.append(data.min_amount)

    if data.max_amount:
        query += " AND t.amount <= %s"
        params.append(data.max_amount)

    if data.account_id:
        query += " AND t.account_id = %s"
        params.append(data.account_id)

    if data.category_id:
        query += " AND t.category_id = %s"
        params.append(data.category_id)

    if data.type:
        query += " AND t.type = %s"
        params.append(data.type)

    query += " ORDER BY t.transaction_date DESC"

    cursor.execute(query, params)

    return cursor.fetchall()


def get_transaction(
    cursor,
    user_id,
    transaction_id
):
    query = """
            SELECT
            t.id, t.category_id, c.name AS category_name,
            t.account_id, a.name AS account_name,
            t.type, t.amount, t.description,
            t.transaction_date, t.created_at

            FROM transactions t LEFT JOIN categories c
            ON t.category_id = c.id
            JOIN accounts a
            ON t.account_id = a.id
            WHERE t.id = %s
            AND t.user_id = %s
            AND (c.user_id = %s OR c.user_id IS NULL)
        """
    params = [transaction_id, user_id, user_id]
    cursor.execute(query,params)

    return cursor.fetchone()



def update_transaction(
    cursor,
    user_id,
    transaction_id,
    transaction: TransactionUpdate
):
    query = """
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
        """
    
    params = (
        transaction.category_id,
        transaction.amount,
        transaction.description,
        transaction.transaction_date,
        transaction.account_id,
        transaction.type,
        transaction_id,
        user_id
    )

    cursor.execute(query, params)
    return transaction_id


def delete_transaction(
    cursor,
    user_id,
    transaction_id
):
    query = """
            DELETE FROM transactions
            WHERE id = %s
            AND user_id = %s
        """
    params = (transaction_id, user_id)
    cursor.execute(query, params)