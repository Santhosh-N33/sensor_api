from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

app = Flask(__name__)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/upload-sensor', methods=['POST'])
def upload_sensor():
    data = request.get_json()
    uid = data.get("uid")

    if not uid:
        return jsonify({"error": "Missing UID"}), 400

    doc_ref = db.collection("users").document(uid).collection("sensors").document("latest")
    doc_ref.set({
        "temperature": data.get("temperature"),
        "humidity": data.get("humidity"),
        "soilMoisture": data.get("moisture"),
        "timestamp": datetime.utcnow()
    })

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
