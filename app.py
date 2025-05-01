from flask import Flask, request, jsonify, render_template_string
import datetime
import sqlite3

app = Flask(__name__)

# ========== قاعدة البيانات ==========
def init_db():
    conn = sqlite3.connect('webhook.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            city TEXT,
            gender TEXT,
            age INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ========== استقبال Webhook ==========
@app.route('/webhook', methods=['POST'])
def salla_webhook():
    data = request.json

    name = data.get("full_name", "غير معروف")
    city = data.get("city", "غير محددة")
    gender = data.get("gender", "غير معروف")
    age = data.get("age", 0)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('webhook.db')
    c = conn.cursor()
    c.execute("INSERT INTO visitors (name, city, gender, age, timestamp) VALUES (?, ?, ?, ?, ?)",
              (name, city, gender, age, timestamp))
    conn.commit()
    conn.close()

    return jsonify({"status": "stored"}), 200

# ========== صفحة عرض الزوار ==========
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('webhook.db')
    c = conn.cursor()
    c.execute("SELECT name, city, gender, age, timestamp FROM visitors ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    html = '''
    <html>
    <head>
        <title>لوحة الزوار</title>
        <style>
            body { font-family: Tahoma; direction: rtl; padding: 40px; background: #f5f5f5; }
            table { width: 100%; border-collapse: collapse; background: white; }
            th, td { padding: 12px; border: 1px solid #ccc; text-align: center; }
            th { background: #333; color: white; }
        </style>
    </head>
    <body>
        <h2>📊 لوحة الزوار</h2>
        <table>
            <tr>
                <th>الاسم</th>
                <th>المدينة</th>
                <th>النوع</th>
                <th>العمر</th>
                <th>وقت الدخول</th>
            </tr>
            {% for row in rows %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
                <td>{{ row[4] }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''
    return render_template_string(html, rows=rows)

@app.route('/')
def home():
    return "Arsid Webhook is live ✅"

if __name__ == '__main__':
    app.run(debug=True)
