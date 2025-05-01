from flask import Flask, request, jsonify
import datetime
from db import create_table, insert_data

app = Flask(__name__)
create_table()  # ينشئ الجدول عند تشغيل التطبيق

@app.route('/webhook', methods=['POST'])
def salla_webhook():
    data = request.json
    print(f"📥 Webhook Received at {datetime.datetime.now()}:")
    print(data)

    try:
        insert_data(
            merchant_id=str(data.get("merchant")),
            customer_name=str(data["data"].get("full_name", "")),
            email=str(data["data"].get("email", "")),
            timestamp=data.get("created_at")
        )
    except Exception as e:
        print(f"❌ Error inserting data: {e}")

    return jsonify({"status": "received"}), 200

@app.route('/')
def home():
    return "Arsid Webhook is live ✅"
from db import get_all_data
from flask import render_template  # تأكد أن هذا السطر موجود في الأعلى

@app.route('/dashboard')
def dashboard():
    rows = get_all_data()
    return render_template('dashboard.html', rows=rows)
