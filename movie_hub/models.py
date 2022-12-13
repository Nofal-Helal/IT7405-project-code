from djongo import models
from djongo.models import (Model, CharField, TextField, IntegerField,
                           DecimalField, DurationField)


# Create your models here.
class Movie(Model):
    title = CharField(max_length=60)
    year = IntegerField()
    duration = DurationField()
