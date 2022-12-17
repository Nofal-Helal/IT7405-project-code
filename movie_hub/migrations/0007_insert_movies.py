# Generated by Django 4.1.3 on 2022-12-17 23:03

from django.apps.registry import Apps
from django.db import migrations
from movie_hub_project.settings import BASE_DIR
import pickle
import zlib

def insertMovies(apps: Apps, _schema_editor):
    Movie = apps.get_model('movie_hub', 'Movie')

    # Read movies from compressed pickled file
    with open(BASE_DIR / 'movie_hub/movies.pickle.zlib', 'rb') as file:
        pickledMovies = zlib.decompress(file.read())
        movies: [Movie] = pickle.loads(pickledMovies)
        for movie in movies:
            movie.save()


def deleteMovies(apps: Apps, _schema_editor):
    Movie = apps.get_model('movie_hub', 'Movie')
    Movie.objects.delete()

class Migration(migrations.Migration):

    dependencies = [
        ("movie_hub", "0006_add_dummy_users"),
    ]

    operations = [migrations.RunPython(insertMovies, deleteMovies)]
