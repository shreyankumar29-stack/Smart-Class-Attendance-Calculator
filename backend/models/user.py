from db import get_db_connection
from flask_login import UserMixin



class User(UserMixin):

    def __init__(
        self,
        id,
        username,
        email,
        image_file,
        password
    ):

        self.id = id

        self.username = username

        self.email = email

        self.image_file = image_file

        self.password = password

# ==========================
# CREATE USER
# ==========================

def create_user(
    username,
    email,
    password,
    image_file="default.jpg"
):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users
        (
            username,
            email,
            image_file,
            password
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
        """,
        (
            username,
            email,
            image_file,
            password
        )
    )

    conn.commit()

    cur.close()
    conn.close()


# ==========================
# GET USER BY EMAIL
# ==========================

def get_user_by_email(email):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE email=%s
        """,
        (email,)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user


# ==========================
# GET USER BY USERNAME
# ==========================

def get_user_by_username(username):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE username=%s
        """,
        (username,)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user


# ==========================
# GET USER BY ID
# ==========================

def get_user_by_id(user_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE id=%s
        """,
        (user_id,)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user

# ==========================
# UPDATE USER
# ==========================

def update_user(
    user_id,
    username,
    email,
    image_file
):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET
            username = %s,
            email = %s,
            image_file = %s
        WHERE id = %s
        """,
        (
            username,
            email,
            image_file,
            user_id
        )
    )

    conn.commit()

    cur.close()
    conn.close()

# ==========================
# LOAD USER
# ==========================
def load_user(user_id):

    user = get_user_by_id(user_id)

    if user:

        return User(

            id=user[0],

            username=user[1],

            email=user[2],

            image_file=user[3],

            password=user[4]

        )

    return None