from movie_app.models import Movie
from movie_app.api.tasks import convert_480p, convert_720p, convert_1080p
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

import os
import django_rq
import glob
import shutil

@receiver(post_save, sender=Movie)
def movie_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for Movie model post-save.

    - Clears the cache.
    - If the movie was newly created:
        - Moves uploaded movie and cover to a structured folder.
        - Updates the file paths in the instance.
        - Creates the target directory if it doesn't exist.
        - Enqueues video conversion tasks (480p, 720p, 1080p) to RQ.
    """

    cache.clear()
    movie_dir = os.path.join("media/movies", str(instance.id))

    if created:
        os.makedirs(movie_dir, exist_ok=True)

        if instance.movie_url:
            old_path = instance.movie_url.path
            new_movie_path = os.path.join(movie_dir, "original.mp4")
            shutil.move(old_path, new_movie_path)
            instance.movie_url.name = f"movies/{instance.id}/original.mp4"

        if instance.cover:
            old_cover = instance.cover.path
            new_cover_path = os.path.join(movie_dir, "cover.jpg")
            shutil.move(old_cover, new_cover_path)
            instance.cover.name = f"movies/{instance.id}/cover.jpg"

        instance.save()

        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_480p, instance.movie_url.path)
        queue.enqueue(convert_720p, instance.movie_url.path)
        queue.enqueue(convert_1080p, instance.movie_url.path)
        
def create_master_playlist(movie_dir):
    """
    Erstellt eine Master-Playlist (master.m3u8) für ein gegebenes Verzeichnis mit Video-Playlists.
    Diese Funktion überprüft, ob Playlists für verschiedene Auflösungen (480p, 720p, 1080p) 
    im angegebenen Verzeichnis vorhanden sind, und erstellt eine Master-Playlist, die 
    diese Varianten referenziert.
    Args:
        movie_dir (str): Der Pfad zum Verzeichnis, das die Video-Playlists enthält.
    Returns:
        None: Gibt nichts zurück, erstellt jedoch eine Datei 'master.m3u8' im Verzeichnis, 
        falls Varianten gefunden werden.
    """
    master_path = os.path.join(movie_dir, "master.m3u8")

    variants = []
    if os.path.exists(os.path.join(movie_dir, "480p.m3u8")):
        variants.append(('480p.m3u8', 600000, '854x480'))
    if os.path.exists(os.path.join(movie_dir, "720p.m3u8")):
        variants.append(('720p.m3u8', 1400000, '1280x720'))
    if os.path.exists(os.path.join(movie_dir, "1080p.m3u8")):
        variants.append(('1080p.m3u8', 2800000, '1920x1080'))

    if not variants:
        print("Keine Varianten gefunden. Master.m3u8 wird nicht erstellt.")
        return

    with open(master_path, "w") as f:
        f.write("#EXTM3U\n")
        for filename, bandwidth, resolution in variants:
            f.write(f'#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},RESOLUTION={resolution}\n')
            f.write(f"{filename}\n")

    print(f"Master-Playlist erstellt: {master_path}")

@receiver(post_delete, sender=Movie)
def auto_delete_file_on_delete(sender, instance, *args, **kwargs):
    """
    Signal handler for Movie model post-delete.

    - Clears the cache.
    - Deletes all video and cover files associated with the movie.
    - Removes the entire movie directory if it exists.
    """
    cache.clear()

    movie_dir = os.path.dirname(instance.movie_url.path)
    if os.path.isdir(movie_dir):
        for root, dirs, files in os.walk(movie_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(movie_dir)