from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "SMS Webhook is running"

@app.route("/sms", methods=["POST"])
def sms_webhook():
    data = request.get_json(force=True, silent=True)
    print("Incoming SMS:", data)
    return jsonify({"status": "received"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
