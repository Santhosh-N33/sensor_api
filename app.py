from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import datetime

app = Flask(__name__)

# Initialize Firebase only once
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

@app.route('/upload-sensor', methods=['POST'])
def upload_sensor_data():
    data = request.get_json()
    uid = data.get('uid')
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    moisture = data.get('moisture')

    if uid is None or temperature is None or humidity is None or moisture is None:
        return jsonify({"error": "Missing fields"}), 400

    doc_ref = db.collection('users').document(uid).collection('sensors').document()
    doc_ref.set({
        'temperature': temperature,
        'humidity': humidity,
        'moisture': moisture,
        'timestamp': datetime.datetime.utcnow()
    })

    return jsonify({"status": "success"}), 200
