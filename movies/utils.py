import requests
from .models import Movie

TMDB_API_KEY = 'f2169e05c3c7239e9f580445e0755083' 
BASE_URL = 'https://api.themoviedb.org/3'

def fetch_movies():
    page = 1
    while page <= 6:  # Fetch 6 pages of movies
        response = requests.get(
            f'{BASE_URL}/movie/popular',
            params={
                'api_key': TMDB_API_KEY,
                'page': page,
            }
        )

        if response.status_code == 200:
            data = response.json()
            movies = data['results']
            
            for movie_data in movies:
                # Extract the necessary details
                title = movie_data.get('title')
                description = movie_data.get('overview')
                release_date = movie_data.get('release_date')
                tmdb_id = movie_data.get('id')
                poster_url = f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path')}"
                vote_count = movie_data.get('vote_count', 0)
                vote_average = movie_data.get('vote_average', 0.0)
                popularity = movie_data.get('popularity', 0.0)

                # Save the movie to the database
                Movie.objects.update_or_create(
                    tmdb_id=tmdb_id,
                    defaults={
                        'title': title,
                        'description': description,
                        'release_date': release_date,
                        'poster_url': poster_url,
                        'vote_count': vote_count,
                        'vote_average': vote_average,
                        'popularity': popularity,
                    }
                )

        else:
            print(f"Error fetching page {page}: {response.status_code}")
            break

        page += 1