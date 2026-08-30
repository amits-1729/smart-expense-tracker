
from app.schemas import BudgetFilter, BudgetUpdate





def get_budget(cursor, user_id, month, category_id):
    query = """
            SELECT id
            FROM budgets
            WHERE user_id = %s
            AND category_id = %s
            AND month = %s
            """
    params = [user_id, category_id, month]

    cursor.execute(query, params)
    return cursor.fetchall()


def get_budget_by_id(cursor, user_id, budget_id):
    query = """
            SELECT 
            b.id, b.category_id, c.name as category_name,
            b.amount, b.month, b.year, b.created_at
            FROM budgets b
            JOIN categories c ON b.category_id = c.id
            WHERE b.user_id = %s
            AND b.id = %s
            AND (c.user_id = %s OR c.user_id IS NULL)
            """
    params = [user_id, budget_id, user_id]

    cursor.execute(query, params)
    return cursor.fetchone()




def create_budget(cursor, user_id, month, category_id, amount):
    query = """
            INSERT INTO budgets (
            user_id, category_id, amount, month, year)
            VALUES (%s, %s, %s, %s, %s)
            """
    params = [user_id, category_id, amount, month, 2026]

    cursor.execute(query, params)
    return cursor.lastrowid




def get_budgets(
    cursor,
    user_id: int,
    data: BudgetFilter
):

    query = """
        SELECT
            b.id,
            b.category_id,
            c.name AS category_name,
            b.amount,
            b.month,
            b.year,
            b.created_at
        FROM budgets b
        JOIN categories c
        ON b.category_id = c.id
        WHERE b.user_id = %s
        AND (c.user_id = %s OR c.user_id IS NULL)
    """

    params = [user_id, user_id]

    if data.month is not None:
        query += " AND b.month = %s"
        params.append(data.month)

    if data.year is not None:
        query += " AND b.year = %s"
        params.append(data.year)

    if data.category_id is not None:
        query += " AND b.category_id = %s"
        params.append(data.category_id)

    if data.min_amount is not None:
        query += " AND b.amount >= %s"
        params.append(data.min_amount)

    if data.max_amount is not None:
        query += " AND b.amount <= %s"
        params.append(data.max_amount)

    query += " ORDER BY b.year DESC, b.month DESC"

    cursor.execute(query,params)
    return cursor.fetchall()




def update_budget(
    cursor,
    user_id:int,
    budget_id: int,
    budget:BudgetUpdate
):
    
    query = """
        UPDATE budgets
        SET
        category_id = %s, amount = %s, month = %s
        WHERE id = %s AND user_id = %s
        """
    params = (
        budget.category_id, budget.amount, budget.month,
        budget_id, user_id
    )
    cursor.execute(query,params)



def delete_budget(
    cursor,
    user_id:int,
    budget_id: int
):
    
    query = """
        DELETE FROM budgets
        WHERE id = %s AND user_id = %s
        """
    params = (budget_id, user_id)
    cursor.execute(query,params)




def get_budget_status(
    cursor,
    user_id: int,
    month: int,
    year: int
):

    query = """
        SELECT
            b.category_id,
            c.name AS category_name,
            b.amount AS budget,

            COALESCE(SUM(t.amount), 0) AS spent

        FROM budgets b
        JOIN categories c
        ON b.category_id = c.id

        LEFT JOIN transactions t
            ON t.category_id = b.category_id
            AND t.user_id = b.user_id
            AND t.type = 'EXPENSE'
            AND MONTH(t.transaction_date) = b.month
            AND YEAR(t.transaction_date) = b.year

        WHERE b.user_id = %s
        AND (c.user_id = %s OR c.user_id IS NULL)
        AND b.month = %s
        AND b.year = %s

        GROUP BY b.id, b.category_id, c.name, b.amount
    """

    cursor.execute(
        query,(user_id, user_id, month, year )
    )

    return cursor.fetchall()