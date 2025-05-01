from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def salla_webhook():
    data = request.json
    print(f"🔔 Webhook Received at {datetime.datetime.now()}:")
    print(data)
    return jsonify({"status": "received"}), 200

@app.route('/')
def home():
    return "Arsid Webhook is live ✅"
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
