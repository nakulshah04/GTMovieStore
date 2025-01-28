import firebase_admin
from firebase_admin import credentials, firestore

SERVICE_ACCOUNT_PATH = "movies/firebase/config/firebaseAuth.json"  # Update with correct path

# Initialize Firebase
def initialize_firebase():
    if not firebase_admin._apps:  # Check if the Firebase app is already initialized
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred, name="GtMovies")
    return firestore.client()  # Return Firestore client