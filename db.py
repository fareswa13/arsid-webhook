import sqlite3

def create_connection():
    conn = sqlite3.connect("webhook_data.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS webhook_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merchant_id TEXT,
            customer_name TEXT,
            email TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_data(merchant_id, customer_name, email, timestamp):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO webhook_data (merchant_id, customer_name, email, timestamp)
        VALUES (?, ?, ?, ?)
    """, (merchant_id, customer_name, email, timestamp))
    conn.commit()
    conn.close()
import sqlite3

def get_all_data():
    conn = sqlite3.connect('webhook_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM webhook_data')
    rows = cursor.fetchall()
    conn.close()
    return rows
