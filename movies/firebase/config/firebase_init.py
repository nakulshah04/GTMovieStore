import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    """
    Initialize Firebase Admin SDK with the service account credentials.
    Ensure that the credentials file is correctly placed.
    """
    try:
        # Point to your service account JSON file
        cred = credentials.Certificate("movies/firebase/config/firebaseAuth.json")
        firebase_admin.initialize_app(cred)
    except ValueError:
        # If Firebase is already initialized, just pass
        pass
