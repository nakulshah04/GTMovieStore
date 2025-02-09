from django.db import models

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

