import os
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from datetime import datetime, timezone

# Initialize Flask app
app = Flask(__name__)

# Fetch Firebase credentials from environment variables
firebase_service_account = os.getenv("FIREBASE_SERVICE_ACCOUNT")
if not firebase_service_account:
    raise ValueError("FIREBASE_SERVICE_ACCOUNT environment variable is missing")

# Initialize Firebase Admin SDK with the service account
cred = credentials.Certificate(firebase_service_account)
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

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


