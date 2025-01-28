import firebase_admin
from django.shortcuts import render
from GTMovieStore.firebase.config.firebase_init import initialize_firebase
from firebase_admin import firestore
import json
import requests

def homepage(request):
    api_url = 'https://api.themoviedb.org/3/movie/now_playing'
    api_key = 'f2169e05c3c7239e9f580445e0755083'

    movies = []  
    num_pages = 20 

    for page in range(1, num_pages + 1):
        response = requests.get(api_url, params={
            'api_key': api_key,
            'language': 'en-US',
            'page': page
        })
        if response.status_code == 200:
            movies.extend(response.json().get('results', []))
        else:
            break  

    return render(request, 'homepage.html', {"movies": movies})
