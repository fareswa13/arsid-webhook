from flask import Flask, request, jsonify
import datetime
import sqlite3
import os

app = Flask(__name__)

# إنشاء قاعدة البيانات (أول مرة فقط)
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            gender TEXT,
            city TEXT,
            age INTEGER,
            event TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

# استدعاء إنشاء قاعدة البيانات
init_db()

@app.route('/webhook', methods=['POST'])
def salla_webhook():
    data = request.json
    print(f"🔔 Webhook Received at {datetime.datetime.now()}:")

    try:
        customer = data.get("data", {})
        name = customer.get("full_name", "")
        phone = customer.get("mobile", "")
        email = customer.get("email", "")
        gender = customer.get("gender", "")
        city = customer.get("city", "")
        age = customer.get("age", None)
        event = data.get("event", "")
        created_at = datetime.datetime.now().isoformat()

        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO visitors (name, phone, email, gender, city, age, event, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, phone, email, gender, city, age, event, created_at))
        conn.commit()
        conn.close()

        return jsonify({"status": "stored"}), 200

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    return "Arsid Webhook is live ✅"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
