# app.py
from flask import Flask, request, jsonify
from firebase_admin_setup import db
from datetime import datetime, timezone


app = Flask(__name__)
@app.route("/upload", methods=["POST"])
def upload_sensor_data():
    try:
        data = request.get_json(force=True)  # force=True to handle bad headers
        uid = data.get("uid")

        if not uid:
            return jsonify({"error": "UID missing"}), 400

        # Store to Firestore
        db.collection("users").document(uid).collection("sensors").add({
            "temperature": data.get("temperature"),
            "humidity": data.get("humidity"),
            "moisture": data.get("moisture"),
            "timestamp": datetime.now(timezone.utc)
        })

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
