from flask import Flask, request, jsonify, render_template, redirect, url_for
from db import create_table, insert_data, get_data_by_token, get_all_tokens
import datetime
import secrets

app = Flask(__name__)
create_table()

@app.route('/webhook', methods=['POST'])
def salla_webhook():
    data = request.json
    print(f"⚡ Webhook Received at {datetime.datetime.now()}:")
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
    return render_template("dashboard.html", rows=rows)

@app.route('/tokens')
def list_tokens():
    tokens = get_all_tokens()
    return render_template("tokens.html", tokens=tokens)

if __name__ == '__main__':
    app.run(debug=True)
