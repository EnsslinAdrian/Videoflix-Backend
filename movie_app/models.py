from django.db import models

def movie_upload_path(instance, filename):
    return f"movies/tmp/original.mp4"

def cover_upload_path(instance, filename):
    return f"movies/tmp/cover.jpg"

class Movie(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    genre = models.CharField(max_length=30)
    release = models.DateField()
    director = models.CharField(max_length=30)
    license_type = models.CharField(max_length=30)
    license_url = models.URLField()
    source_url = models.URLField()
    cover = models.ImageField(upload_to=cover_upload_path)
    movie_url = models.FileField(upload_to=movie_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

class Trailer(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    genre = models.CharField(max_length=30)
    release = models.DateField()
    director = models.CharField(max_length=30)
    license_type = models.CharField(max_length=30)
    license_url = models.URLField()
    source_url = models.URLField()
    cover = models.ImageField(upload_to='trailer')
    movie_url = models.FileField(upload_to='trailer')
    created_at = models.DateTimeField(auto_now_add=True)