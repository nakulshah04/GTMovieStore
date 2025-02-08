# DONT CHANGE ANYTHING TO THIS -- NETHANN 

# THIS BASICALLY UPDATES FIREBASE MOVIES

import requests
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebaseAuth.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

def update_movies():
    api_url = 'https://api.themoviedb.org/3/movie/now_playing'
    api_key = 'f2169e05c3c7239e9f580445e0755083'

    movies_ref = db.collection("Movies")
    existing_movies = {doc.id for doc in movies_ref.stream()}  

    print(f"Found {len(existing_movies)} existing movies in Firestore.")

    print("Fetching new movies...")

    movies = []
    for page in range(1, 11):  
        response = requests.get(api_url, params={'api_key': api_key, 'language': 'en-US', 'page': page})
        if response.status_code == 200:
            results = response.json().get('results', [])
            movies.extend(results)
        else:
            print(f"Failed to fetch movies on page {page}. Status code: {response.status_code}")

    added_count = 0
    for movie in movies:
        movie_id = str(movie['id'])
        print(f"Checking if movie {movie_id} exists...")  
        if movie_id not in existing_movies:
            movie_doc_ref = movies_ref.document(movie_id)
            movie_doc_ref.set({
                "id": movie['id'],
                "title": movie['title'],
                "poster_path": movie['poster_path'],
                "overview": movie['overview'],
                "release_date": movie['release_date'],
                "rating": movie.get('vote_average', 0),
                "vote_count": movie.get('vote_count', 0),
                "popularity": movie.get('popularity', 0),
                "created_at": firestore.SERVER_TIMESTAMP
            })
            added_count += 1
            print(f"Movie {movie_id} added to Firestore.")
            

    print(f"YUH ADDED {added_count} NEW MOVIES.")



if __name__ == "__main__":
    update_movies()
