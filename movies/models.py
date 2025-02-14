import random
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    poster_url = models.URLField()
    vote_count = models.IntegerField(default=0)
    vote_average = models.FloatField(default=0.0)
    popularity = models.FloatField(default=0.0)
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        """ Assign a random price if it's not set """
        if not self.price or self.price == 0.00:
            self.price = random.choice([11.99, 9.99, 7.99])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.movie.title}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)  # Link order to a user
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def update_status(self, new_status):
        if new_status in dict(self.STATUS_CHOICES):  
            self.status = new_status
            self.save()

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)  # ✅ FIXED
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.movie.title} (Order {self.order.id})"
