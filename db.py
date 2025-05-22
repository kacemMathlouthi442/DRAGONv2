import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg.connect(os.environ.get("DATABASE_URL"))

def create_users_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    first_name TEXT,
    API BOOLEAN DEFAULT FALSE,
    subscribed BOOLEAN DEFAULT FALSE,
    banned BOOLEAN DEFAULT FALSE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
            """)
            conn.commit()

def add_user(user):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (id, first_name)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (user.id,user.first_name))
            conn.commit()

def redeem_token(user_id, value=True):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET api_token = %s WHERE id = %s", (value, user_id))
            conn.commit()

def set_subscribed(user_id, value=True):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET subscribed = %s WHERE id = %s", (value, user_id))
            conn.commit()

def set_banned(user_id, value=True):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET banned = %s WHERE id = %s", (user_id,value))
            conn.commit()

def get_user_count():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users")
            count = cur.fetchone()[0]
            return count


def is_user_useAPI(user_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT API FROM users WHERE id = %s", (user_id,))
            result = cur.fetchone()
            return result[0] if result else False
        
def user_exists(user_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
            return cur.fetchone() is not None
        
def is_user_banned(user_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT banned FROM users WHERE id = %s", (user_id,))
            result = cur.fetchone()
            return result[0] if result else False
        
def is_user_subscribed(user_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT subscribed FROM users WHERE id = %s", (user_id,))
            result = cur.fetchone()
            return result[0] if result else False
