from djongo import models
from djongo.models import (
    ArrayField,
    CharField,
    DateTimeField,
    EmbeddedField,
    FloatField,
    ForeignKey,
    IntegerField,
    JSONField,
    Model,
    ObjectIdField,
    TextField,
)
from django.contrib.auth.models import User


# Create your models here.
class IMDB(Model):
    imdb_id = CharField(max_length=20)
    rating = FloatField()
    votes = IntegerField()

    class Meta:
        abstract = True


class Comment(Model):
    user_id = IntegerField()
    text = TextField()
    rating = FloatField()
    date = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Duration(Model):
    hours = IntegerField()
    minutes = IntegerField()

    class Meta:
        abstract = True


class Movie(Model):
    _id = ObjectIdField()
    title = CharField(max_length=60)
    year = IntegerField()
    duration = EmbeddedField(Duration)
    directors = JSONField(default=[])
    writers = JSONField(default=[])
    cast = JSONField(default=[])
    posterImage = models.URLField(blank=True)
    summary = TextField(blank=True)
    moreSummary = TextField(blank=True)
    genres = JSONField(default=[])
    parentsGuide = CharField(max_length=5,
                             choices=[('G', 'G - General Audience'),
                                      ('PG',
                                       'PG - Parental Guidance Suggested'),
                                      ('PG-13',
                                       'PG-13 - Parents Strongly Cautioned'),
                                      ('R', 'R - Restricted'),
                                      ('NC-17', 'NC-17 - Adults Only')])
    imdb = EmbeddedField(IMDB, blank=True)
    comments = ArrayField(Comment, blank=True, default=[])
    dateAdded = DateTimeField(auto_now_add=True)

