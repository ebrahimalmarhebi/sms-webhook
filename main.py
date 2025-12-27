from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "SMS Webhook is running ✅"

@app.route("/sms", methods=["POST"])
def sms_webhook():
    data = request.json
    print("Incoming SMS:", data)
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
