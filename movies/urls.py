from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.urls import path
from .views import checkout, order_history

from django.contrib.auth import views as auth_views

from .views import edit_review, delete_review




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
    path('movie/<int:movie_id>/review/add/', views.add_review, name='add_review'),  



    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='Auth/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Auth/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Auth/password_reset_complete.html'), name='password_reset_complete'),

    path("edit-review/<int:review_id>/", edit_review, name="edit_review"),
    path("delete-review/<int:review_id>/", delete_review, name="delete_review"),

    path('checkout/', checkout, name='checkout'),
    path('orders/', order_history, name='orders'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
