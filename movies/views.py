from .models import Movie  

from django.shortcuts import render, get_object_or_404, redirect
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
from django.contrib.auth.decorators import login_required
from .models import Movie, Review




def homepage(request):
    search_query = request.GET.get('q', '').strip()
    sort_option = request.GET.get('sort', '')

    movies = Movie.objects.all().order_by('?')  

    if search_query:
        movies = movies.filter(title__icontains=search_query)

    if sort_option == "title_asc":
        movies = movies.order_by('title')
    elif sort_option == "title_desc":
        movies = movies.order_by('-title')
    elif sort_option == "date_asc":
        movies = movies.order_by('release_date')
    elif sort_option == "date_desc":
        movies = movies.order_by('-release_date')

    return render(request, 'Homepage/homepage.html', {
        "movies": movies,
        "search_query": search_query,
    })


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = movie.reviews.all() 

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        review = Review.objects.create(
            movie=movie,
            user=request.user,
            rating=rating,
            comment=comment
        )
        review.save()
        return redirect('movie_detail', movie_id=movie.id)

    return render(request, 'Movies/movie_detail.html', {'movie': movie, 'reviews': reviews})




@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if movie.reviews.filter(user=request.user).exists():
        messages.error(request, "You can only post one review per movie.")
        return redirect("movie_detail", movie_id=movie.id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment").strip()

        if not rating or not comment:
            messages.error(request, "Both rating and comment are required.")
            return redirect("movie_detail", movie_id=movie.id)

        review = Review.objects.create(
            movie=movie,
            user=request.user,
            rating=int(rating),
            comment=comment
        )

        messages.success(request, "Review added successfully!")
        return redirect("movie_detail", movie_id=movie.id)

    return redirect("movie_detail", movie_id=movie.id)



MOVIE_PRICES = {
    1400383: 9.99, 
    299534: 12.99,
    76341: 7.99,
}



def cart(request):
    """ View Cart Page """
    cart = request.session.get('cart', {})

    cart_items = []
    cart_total = 0

    for movie_id, movie_data in cart.items():
        if isinstance(movie_data, int):  
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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Movie  

def add_to_cart(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)  
    cart = request.session.get('cart', {})

    movie_id_str = str(movie_id)  

    if movie_id_str in cart:
        cart[movie_id_str]["quantity"] += 1
    else:
        cart[movie_id_str] = {
            "title": movie.title,
            "poster": movie.poster_url if movie.poster_url else "/static/default.jpg",
            "quantity": 1
        }

    request.session['cart'] = cart  
    messages.success(request, f"Added {movie.title} to cart!")

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

    request.session['cart'] = cart  
    messages.success(request, "Movie removed from cart!")
    return redirect("cart")

def checkout(request):
    """ Checkout Process """
    request.session['cart'] = {}  
    messages.success(request, "Purchase successful! 🎉")
    return redirect("homepage")

def about(request):
    """
    Render the About page.
    """
    return render(request, 'Movies/about.html')



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

        # Validation checks
        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                messages.success(request, "Account created successfully! You can now log in.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('register')

    return render(request, 'Auth/register.html')



def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')