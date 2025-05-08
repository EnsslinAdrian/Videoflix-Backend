# movie_app/management/commands/generate_master_playlists.py

from django.core.management.base import BaseCommand
from movie_app.models import Movie
from movie_app.api.signals import create_master_playlist

import os

class Command(BaseCommand):
    help = 'Erzeugt Master.m3u8 Playlists für alle existierenden Filme.'

    def handle(self, *args, **options):
        movies = Movie.objects.all()
        count = 0

        for movie in movies:
            if not movie.movie_url:
                self.stdout.write(f"Film {movie.id} hat keinen movie_url. Überspringe.")
                continue

            movie_dir = os.path.dirname(movie.movie_url.path)
            if not os.path.exists(movie_dir):
                self.stdout.write(f"Film {movie.id} Verzeichnis existiert nicht: {movie_dir}. Überspringe.")
                continue

            self.stdout.write(f"Erzeuge Master.m3u8 für Film {movie.id}...")
            create_master_playlist(movie_dir)
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Fertig! Für {count} Filme wurde die Master-Playlist erstellt oder geprüft.'))
