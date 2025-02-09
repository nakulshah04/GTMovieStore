from django.core.management.base import BaseCommand
from movies.utils import fetch_movies  # Import your function

class Command(BaseCommand):
    help = 'Fetches movies from the TMDb API and saves them to the database'

    def handle(self, *args, **kwargs):
        fetch_movies()  
        self.stdout.write(self.style.SUCCESS('Successfully fetched movies!'))
