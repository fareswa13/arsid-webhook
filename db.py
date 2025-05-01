import sqlite3

DB_NAME = "webhook_data.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS salla_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merchant_id TEXT,
            customer_name TEXT,
            email TEXT,
            timestamp TEXT,
            token TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_data(merchant_id, customer_name, email, timestamp, token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO salla_data (merchant_id, customer_name, email, timestamp, token)
        VALUES (?, ?, ?, ?, ?)
    """, (merchant_id, customer_name, email, timestamp, token))
    conn.commit()
    conn.close()

def get_data_by_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT customer_name, email, timestamp FROM salla_data WHERE token=?
    """, (token,))
    rows = c.fetchall()
    conn.close()
    return rows
