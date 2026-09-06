
def get_category_by_name(cursor, user_id, category_name):
    query = """
        SELECT id,name FROM categories
        WHERE (user_id = %s OR user_id IS NULL)
        AND name = %s
        """
    params = (user_id, category_name)
    cursor.execute(query,params)
    return cursor.fetchone()


def get_categories(cursor, user_id):
    query = """
        SELECT id,name FROM categories
        WHERE (user_id = %s OR user_id IS NULL)
        """
    cursor.execute(query,(user_id,))
    return cursor.fetchall()


def get_category_by_id(cursor, user_id, category_id):
    query = """
        SELECT id,name,user_id FROM categories
        WHERE id = %s AND (user_id = %s OR user_id IS NULL)
        """
    params = (category_id, user_id)
    cursor.execute(query,params)
    return cursor.fetchone()


def create_category(cursor, user_id, category_name):
    query = """
        INSERT INTO categories (name, user_id)
        VALUES (%s, %s)
        """
    params = (category_name,user_id)

    cursor.execute(query,params)
    return cursor.lastrowid


def update_category(cursor, user_id, category_id, category_name):
    query = """
        UPDATE categories
        SET name = %s
        WHERE id = %s AND user_id=%s
        """
    params = (category_name, category_id, user_id)
    cursor.execute(query,params)


def delete_category(cursor, user_id, category_id):
    query = """
            DELETE FROM categories
            WHERE id = %s AND user_id = %s
            """
    params = (category_id, user_id)
    cursor.execute(query,params)
            