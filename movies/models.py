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


