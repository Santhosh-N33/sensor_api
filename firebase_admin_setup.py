import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Read JSON string from environment variable
firebase_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")

if not firebase_json:
    raise Exception("FIREBASE_SERVICE_ACCOUNT is not set")

service_account_info = json.loads(firebase_json)
cred = credentials.Certificate(service_account_info)

firebase_admin.initialize_app(cred)
db = firestore.client()
