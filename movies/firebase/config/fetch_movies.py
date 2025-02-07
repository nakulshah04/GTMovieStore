import requests
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebaseAuth.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

def update_reviews():
    api_key = 'f2169e05c3c7239e9f580445e0755083'

    reviews_ref = db.collection("Reviews") 

    print("Fetching movies and their reviews...")

    for page in range(1, 6):  
        api_url = f'https://api.themoviedb.org/3/movie/now_playing'
        response = requests.get(api_url, params={'api_key': api_key, 'language': 'en-US', 'page': page})

        if response.status_code == 200:
            results = response.json().get('results', [])
            for movie in results:
                movie_id = str(movie['id'])

                reviews_url = f'https://api.themoviedb.org/3/movie/{movie_id}/reviews'
                reviews_response = requests.get(reviews_url, params={'api_key': api_key, 'language': 'en-US'})

                if reviews_response.status_code == 200:
                    reviews_data = reviews_response.json()
                    reviews = reviews_data.get("results", [])

                    for review in reviews:
                        review_doc_ref = reviews_ref.document() 
                        review_doc_ref.set({
                            "movie_id": movie_id,
                            "author": review.get("author", "Unknown"),
                            "content": review.get("content", ""),
                            "created_at": firestore.SERVER_TIMESTAMP
                        })

    print("Reviews added successfully!")

if __name__ == "__main__":
    update_reviews()
