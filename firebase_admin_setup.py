import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Get and parse the Firebase service account from environment variable
firebase_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")

if not firebase_json:
    raise RuntimeError("FIREBASE_SERVICE_ACCOUNT env variable is not set or empty.")

try:
    service_account_info = json.loads(firebase_json)
    # Replace escaped newlines in the private key
    service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")
except Exception as e:
    raise RuntimeError(f"Failed to parse FIREBASE_SERVICE_ACCOUNT JSON: {e}")

# Initialize Firebase
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)
db = firestore.client()
