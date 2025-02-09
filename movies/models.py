from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    poster_url = models.URLField()
    vote_count = models.IntegerField(default=0)
    vote_average = models.FloatField(default=0.0)
    popularity = models.FloatField(default=0.0)

    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.author} on {self.movie.title}"
