# Generated by Django 5.2 on 2025-04-30 11:30

import movie_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='cover',
            field=models.ImageField(upload_to=movie_app.models.cover_upload_path),
        ),
        migrations.AlterField(
            model_name='movie',
            name='movie_url',
            field=models.FileField(upload_to=movie_app.models.movie_upload_path),
        ),
    ]
