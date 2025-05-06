from movie_app.models import Movie
from movie_app.api.tasks import convert_480p, convert_720p, convert_1080p
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

import os
import django_rq
import shutil

@receiver(post_save, sender=Movie)
def movie_post_save(sender, instance, created, **kwargs):
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

        queue.enqueue(convert_480p, instance.movie_url.path, timeout=600)
        queue.enqueue(convert_720p, instance.movie_url.path, timeout=900)
        queue.enqueue(convert_1080p, instance.movie_url.path, timeout=1800)

@receiver(post_delete, sender=Movie)
def auto_delete_file_on_delete(sender, instance, *args, **kwargs):
    cache.clear()

    movie_dir = os.path.dirname(instance.movie_url.path)
    if os.path.isdir(movie_dir):
        for root, dirs, files in os.walk(movie_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(movie_dir)

CACHE_TTL = 60 * 15
