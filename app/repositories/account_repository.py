

def get_account_by_name(cursor, user_id, name):
    query = "SELECT id FROM accounts WHERE name = %s AND user_id = %s"
    params = (name, user_id)
    cursor.execute(query, params)
    return cursor.fetchone()


def create_account(cursor, user_id, name):
    query = "INSERT INTO accounts (user_id, name) VALUES (%s, %s);"
    params = (user_id, name)

    cursor.execute(query,params)
    return cursor.lastrowid


def get_accounts(cursor, user_id):
    query = """
            SELECT id, name, balance
            FROM accounts
            WHERE user_id = %s
        """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


def get_account_by_id(cursor, user_id, account_id):
    query = "SELECT id FROM accounts WHERE id = %s AND user_id = %s"
    params = (account_id, user_id)
    cursor.execute(query, params)
    return cursor.fetchone()


def update_account_balance(
    cursor,
    user_id,
    account_id,
    amount,
    transaction_type
):
    query = """
            UPDATE accounts
            SET balance = balance - %s
            WHERE id = %s AND user_id = %s
            """

    if transaction_type == "EXPENSE":
        cursor.execute(
            query, (amount, account_id, user_id)
        )

    else:
        cursor.execute(
            query, (-amount, account_id, user_id)
        )