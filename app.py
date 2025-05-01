from flask import Flask, request, jsonify, render_template, redirect, url_for
from db import create_table, insert_data, get_data_by_token
import datetime
import secrets
import sqlite3

app = Flask(__name__)
create_table()

@app.route('/webhook', methods=['POST'])
def salla_webhook():
    data = request.json
    print(f"⚡️ Webhook Received at {datetime.datetime.now()}:")
    print(data)

    try:
        merchant_id = str(data.get("merchant"))
        customer_name = str(data["data"].get("full_name", ""))
        email = str(data["data"].get("email", ""))
        timestamp = data.get("created_at")
        token = secrets.token_hex(8)

        entry_time = str(data["data"].get("entry_time", ""))
        exit_time = str(data["data"].get("exit_time", ""))
        duration = str(data["data"].get("duration", ""))
        country = str(data["data"].get("country", ""))
        city = str(data["data"].get("city", ""))

        insert_data(
            merchant_id, customer_name, email, timestamp, token,
            entry_time, exit_time, duration, country, city
        )
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        return jsonify({"status": "error"}), 500

    return jsonify({"status": "received"}), 200

@app.route('/')
def home():
    return redirect(url_for('list_tokens'))

@app.route('/dashboard/<token>')
def dashboard_info(token):
    rows = get_data_by_token(token)
    if not rows:
        return "⚠️ الرابط غير صالح أو لا توجد بيانات."

    formatted_rows = []
    for row in rows:
        try:
            entry_time = datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S").strftime("%I:%M %p")
            exit_time = datetime.datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S").strftime("%I:%M %p")
            duration = str(round(float(row[5]), 2)) + " دقيقة"
        except:
            entry_time, exit_time, duration = row[3], row[4], row[5]

        formatted_rows.append((
            row[0], row[1], row[2], entry_time, exit_time, duration, row[6], row[7], token
        ))

    return render_template("dashboard.html", rows=formatted_rows)

@app.route('/tokens')
def list_tokens():
    conn = sqlite3.connect("webhook_data.db")
    c = conn.cursor()
    c.execute("SELECT DISTINCT token FROM salla_data")
    tokens = c.fetchall()
    conn.close()

    links = [f"<li><a href='/dashboard/{t[0]}'>لوحة التاجر: {t[0]}</a></li>" for t in tokens]
    return f"<h2>💼 روابط لوحات التحكم</h2><ul>{''.join(links)}</ul>"

if __name__ == '__main__':
    app.run(debug=True)
