from django.db import models

def movie_upload_path(instance, filename):
    """
    Returns the upload path for movie files.
    Currently hardcoded to 'movies/tmp/original.mp4'.
    """
    return f"movies/tmp/original.mp4"

def cover_upload_path(instance, filename):
    """
    Returns the upload path for cover images.
    Currently hardcoded to 'movies/tmp/cover.jpg'.
    """
    return f"movies/tmp/cover.jpg"

class Movie(models.Model):
    """
    Represents a movie entity with details such as title, description, genre, release date, director, licensing information, 
    media URLs, and timestamps for creation.
    """
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
    """
    Represents a movie trailer with metadata and associated media files.

    Attributes:
        title (str): The title of the trailer.
        description (str): A brief description of the trailer.
        genre (str): The genre of the trailer.
        release (date): The release date of the trailer.
        director (str): The director of the trailer.
        license_type (str): The type of license for the trailer.
        license_url (str): The URL to the license details.
        source_url (str): The URL to the source of the trailer.
        cover (ImageField): The cover image for the trailer.
        movie_url (FileField): The video file of the trailer.
        created_at (datetime): The timestamp when the trailer was created.
    """
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