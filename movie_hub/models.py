from djongo import models
from djongo.models import (
    ArrayField,
    CharField,
    DateTimeField,
    EmbeddedField,
    FloatField,
    IntegerField,
    JSONField,
    Model,
    ObjectIdField,
    TextField,
)


# Create your models here.
class IMDB(Model):
    imdb_id = CharField(max_length=20)
    rating = FloatField()
    votes = IntegerField()

    class Meta:
        abstract = True


class Comment(Model):
    user_id = ObjectIdField()
    text = TextField()
    date = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Duration(Model):
    hours = IntegerField()
    minutes = IntegerField

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
    genres = JSONField(default=[])
    imdb = EmbeddedField(IMDB, blank=True)
    comments = ArrayField(Comment, blank=True, default=[])

