from flask import Flask, request, jsonify, render_template, redirect, url_for
from db import create_table, insert_data, get_data_by_token
import datetime
import secrets

app = Flask(__name__)

# Create DB table if not exists
create_table()

@app.route('/webhook', methods=['POST'])
def salla_webhook():
    data = request.json
    print(f"⚡️ Webhook Received at {datetime.datetime.now()}:")
    print(data)

    try:
        merchant_id = str(data.get("merchant"))
        token = secrets.token_hex(8)  # unique token for dashboard

        insert_data(
            merchant_id=merchant_id,
            customer_name=str(data["data"].get("full_name", "")),
            email=str(data["data"].get("email", "")),
            timestamp=data.get("created_at"),
            token=token
        )
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        return jsonify({"status": "error"}), 500

    return jsonify({"status": "received"}), 200

@app.route('/')
def home():
    return redirect(url_for('dashboard_info'))

@app.route('/dashboard/<token>')
def dashboard_info(token):
    rows = get_data_by_token(token)
    if not rows:
        return "⚠️ الرابط غير صالح أو لا توجد بيانات."
    return render_template("dashboard.html", rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
