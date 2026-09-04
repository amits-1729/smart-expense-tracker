from app.schemas import RegisterUser

def get_user(cursor, user_email):
    query = """
            SELECT id, name, email, password
            FROM users
            WHERE email = %s
            """
    cursor.execute(query,(user_email,))

    return cursor.fetchone()


def get_user_by_id(cursor, user_id):
    query = """
            SELECT id, name, email, created_at
            FROM users
            WHERE id = %s
            """
    cursor.execute(query,(user_id,))

    return cursor.fetchone()

def register_user(
    cursor,
    user:RegisterUser,
    hashed_password
):
    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    params = (user.name, user.email, hashed_password)

    cursor.execute(query,params)


def reset_password(
    cursor,
    user_id:int,
    password
):
    query = """
            UPDATE users
            SET password = %s
            WHERE id = %s
            """
    cursor.execute(query,(password,user_id))