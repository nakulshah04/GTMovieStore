from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    poster_url = models.URLField()

    def __str__(self):
        return self.title