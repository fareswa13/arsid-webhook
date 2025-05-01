""import sqlite3

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
            token TEXT,
            entry_time TEXT,
            exit_time TEXT,
            duration TEXT,
            country TEXT,
            city TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_data(merchant_id, customer_name, email, timestamp, token, entry_time, exit_time, duration, country, city):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO salla_data (
            merchant_id, customer_name, email, timestamp, token,
            entry_time, exit_time, duration, country, city
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (merchant_id, customer_name, email, timestamp, token, entry_time, exit_time, duration, country, city))
    conn.commit()
    conn.close()

def get_data_by_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT customer_name, email, timestamp, entry_time, exit_time, duration, country, city
        FROM salla_data WHERE token=?
    """, (token,))
    rows = c.fetchall()
    conn.close()
    return rows
