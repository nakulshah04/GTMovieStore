from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:movie_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:movie_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('cart/update/<int:movie_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('movie/<int:movie_id>/review/add/', views.add_review, name='add_review'),  # Keeping one valid path

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
