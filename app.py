from flask import Flask, request, jsonify, render_template, redirect, url_for
from db import create_table, insert_data, get_data_by_token
import datetime
import secrets

app = Flask(__name__)

# إنشاء الجدول عند التشغيل
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

        # بيانات المتابعة
        entry_time = str(data["data"].get("entry_time", ""))
        exit_time = str(data["data"].get("exit_time", ""))
        duration = str(data["data"].get("duration", ""))
        country = str(data["data"].get("country", ""))
        city = str(data["data"].get("city", ""))

        insert_data(
            merchant_id=merchant_id,
            customer_name=customer_name,
            email=email,
            timestamp=timestamp,
            token=token,
            entry_time=entry_time,
            exit_time=exit_time,
            duration=duration,
            country=country,
            city=city
        )
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        return jsonify({"status": "error"}), 500

    return jsonify({"status": "received"}), 200

@app.route('/')
def home():
    return redirect(url_for('dashboard_info', token="demo"))  # مؤقتًا

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
            row[0],  # الاسم
            row[1],  # الإيميل
            row[2],  # التوقيت
            entry_time,
            exit_time,
            duration,
            row[6],  # الدولة
            row[7]   # المدينة
        ))

    return render_template("dashboard.html", rows=formatted_rows)

if __name__ == '__main__':
    app.run(debug=True)
