from django.shortcuts import render
from django.http import Http404
from movies.firebase.config.firebase_init import initialize_firebase
from firebase_admin import firestore
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime


initialize_firebase()

db = firestore.client()

def homepage(request):
    api_url = 'https://api.themoviedb.org/3/movie/now_playing'
    api_key = 'f2169e05c3c7239e9f580445e0755083'

    search_query = request.GET.get("q", "").strip()
    sort_order = request.GET.get("sort", "")

    movies_ref = db.collection("Movies")
    stored_movies = [doc.to_dict() for doc in movies_ref.stream()]

    if not stored_movies:
        movies = []
        for page in range(1, 11):
            response = requests.get(api_url, params={'api_key': api_key, 'language': 'en-US', 'page': page})
            if response.status_code == 200:
                results = response.json().get('results', [])
                movies.extend(results)

        existing_movie_ids = {movie['id'] for movie in stored_movies}
        for movie in movies:
            if str(movie['id']) not in existing_movie_ids:
                movie_ref = movies_ref.document(str(movie['id']))
                movie_ref.set({
                    "id": movie['id'],
                    "title": movie['title'],
                    "poster_path": movie['poster_path'],
                    "overview": movie['overview'],
                    "release_date": movie['release_date'],
                    "rating": movie.get('vote_average', 0),
                    "created_at": firestore.SERVER_TIMESTAMP
                })
                stored_movies.append(movie)

    if search_query:
        filtered_movies = [movie for movie in stored_movies if search_query.lower() in movie['title'].lower()]
    else:
        filtered_movies = stored_movies

    # Sorting movies based on sort query
    if sort_order == "title_asc":
        filtered_movies.sort(key=lambda x: x['title'].lower())
    elif sort_order == "title_desc":
        filtered_movies.sort(key=lambda x: x['title'].lower(), reverse=True)
    elif sort_order == "date_desc":
        filtered_movies.sort(key=lambda x: x['release_date'], reverse=True)
    elif sort_order == "date_asc":
        filtered_movies.sort(key=lambda x: x['release_date'])

    # Convert release_date to datetime object for formatting
    for movie in filtered_movies:
        if movie['release_date']:
            movie['release_date'] = datetime.strptime(movie['release_date'], "%Y-%m-%d")
    return render(request, 'Homepage/homepage.html', {"movies": filtered_movies})

def movie_detail(request, movie_id):
    """
    Fetch detailed movie information and reviews from TMDB or Firestore if already cached.
    """
    api_key = 'f2169e05c3c7239e9f580445e0755083'

    movie_id = str(movie_id)

    movies_ref = db.collection("Movies")

    movie_doc = movies_ref.document(movie_id).get()

    if movie_doc.exists:
        movie = movie_doc.to_dict()
        reviews = movie.get("reviews", ["No reviews available for this movie."])
        return render(request, 'Movies/movie_detail.html', {'movie': movie, 'reviews': reviews})

    movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    movie_response = requests.get(movie_url, params={'api_key': api_key, 'language': 'en-US'})

    reviews = []
    page = 1
    total_pages = 1  

    while page <= total_pages:
        reviews_url = f'https://api.themoviedb.org/3/movie/{movie_id}/reviews'
        reviews_response = requests.get(reviews_url, params={'api_key': api_key, 'language': 'en-US', 'page': page})

        if reviews_response.status_code == 200:
            data = reviews_response.json()
            total_results = data.get("total_results", 0)
            reviews.extend(data.get("results", []))
            total_pages = data.get("total_pages", 1)
            page += 1  
        else:
            break  

    if len(reviews) == 0:
        reviews = ["No reviews available for this movie."]

    if movie_response.status_code == 200:
        movie = movie_response.json()

        movie_doc = movies_ref.document(movie_id)
        movie_doc.set({
            "id": movie_id,
            "title": movie["title"],
            "poster_path": movie["poster_path"],
            "overview": movie["overview"],
            "release_date": movie["release_date"],
            "rating": movie.get("vote_average", 0),
            "reviews": reviews,  
            "created_at": firestore.SERVER_TIMESTAMP
        })
        return render(request, 'Movies/movie_detail.html', {'movie': movie, 'reviews': reviews})

    raise Http404("Movie not found.")

# Simulated pricing (in a real app, this would come from a database)
MOVIE_PRICES = {
    1400383: 9.99,  # Example Movie ID → Price
    299534: 12.99,
    76341: 7.99,
}



def cart(request):
    """ View Cart Page """
    cart = request.session.get('cart', {})

    cart_items = []
    cart_total = 0

    for movie_id, movie_data in cart.items():
        if isinstance(movie_data, int):  # Fix for incorrectly stored integer values
            movie_data = {"title": f"Movie {movie_id}", "poster": "", "quantity": movie_data}

        cart_items.append({
            "movie": {
                "id": movie_id,
                "title": movie_data.get("title", f"Movie {movie_id}"),
                "poster": movie_data.get("poster", ""),
            },
            "quantity": movie_data.get("quantity", 1)
        })

    return render(request, "Movies/cart.html", {"cart_items": cart_items})


def add_to_cart(request, movie_id):
    """ Add Movie to Cart """
    api_url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    api_key = 'f2169e05c3c7239e9f580445e0755083'

    response = requests.get(api_url, params={'api_key': api_key, 'language': 'en-US'})

    if response.status_code == 200:
        movie_data = response.json()
        cart = request.session.get('cart', {})

        cart[movie_id] = {
            "title": movie_data["title"],
            "poster": f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}",
            "quantity": cart.get(movie_id, {}).get("quantity", 0) + 1
        }

        request.session['cart'] = cart  # Save updated cart in session
        messages.success(request, f"Added {movie_data['title']} to cart!")

    return redirect("cart")

def update_cart(request, movie_id):
    """ Update Cart Quantity """
    if request.method == "POST":
        new_quantity = int(request.POST.get("quantity", 1))
        cart = request.session.get('cart', {})
        if new_quantity > 0:
            cart[movie_id] = new_quantity
        else:
            cart.pop(movie_id, None)  # Remove if quantity is 0
        request.session['cart'] = cart
        messages.success(request, "Cart updated!")
    return redirect("cart")


def remove_from_cart(request, movie_id):
    """ Remove Movie from Cart """
    cart = request.session.get('cart', {})

    movie_id = str(movie_id)

    if movie_id in cart:
        del cart[movie_id]  

    request.session['cart'] = cart  # Save updated cart
    messages.success(request, "Movie removed from cart!")
    return redirect("cart")

def checkout(request):
    """ Checkout Process """
    request.session['cart'] = {}  # Clear cart after checkout
    messages.success(request, "Purchase successful! 🎉")
    return redirect("homepage")

def about(request):
    """
    Render the About page.
    """
    return render(request, 'Movies/aboutpage.html')



def login_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('homepage')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'Auth/login.html')  

def register_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
        else:
            # Create the user in Django
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()

            user_data = {
                "username": username,
                "email": email,
                "uid": str(user.id),  
                "created_at": firestore.SERVER_TIMESTAMP  
            }

            try:
                db.collection('RegisteredUsers').document(str(user.id)).set(user_data)
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect('login')
            except Exception as e:
                messages.error(request, "Failed to register user in Firestore. Please try again later.")

    return render(request, 'Auth/register.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')