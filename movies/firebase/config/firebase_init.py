import firebase_admin
from firebase_admin import credentials

SERVICE_ACCOUNT_PATH = "movies/firebase/config/firebaseAuth.json"  # Update with correct path

def initialize_firebase():
    if not firebase_admin._apps:  # Ensures Firebase initializes only once
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred)