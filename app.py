import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

# Initialize Firebase using the json file directly
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/upload", methods=["POST"])
def upload_sensor_data():
    try:
        data = request.get_json(force=True)
        uid = data.get("uid")
        if not uid:
            return jsonify({"error": "UID missing"}), 400

        db.collection("users").document(uid).collection("sensors").add({
            "temperature": data.get("temperature"),
            "humidity": data.get("humidity"),
            "moisture": data.get("moisture"),
            "timestamp": datetime.now(timezone.utc)
        })

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
