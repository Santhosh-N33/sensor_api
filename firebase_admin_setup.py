import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase credentials from Render's Secrets Manager
service_account_key = json.loads(os.getenv("FIREBASE_SERVICE_ACCOUNT"))

# Initialize Firebase Admin SDK
cred = credentials.Certificate(service_account_key)
firebase_admin.initialize_app(cred)

db = firestore.client()
