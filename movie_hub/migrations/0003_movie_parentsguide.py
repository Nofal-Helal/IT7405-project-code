# Generated by Django 4.1.3 on 2022-12-15 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movie_hub", "0002_movie_dateadded"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="parentsGuide",
            field=models.CharField(
                choices=[
                    ("G", "G - General Audience"),
                    ("PG", "PG - Parental Guidance Suggested"),
                    ("PG-13", "PG-13 - Parents Strongly Cautioned"),
                    ("R", "R - Restricted"),
                    ("NC-17", "NC-17 - Adults Only"),
                ],
                default="R",
                max_length=5,
            ),
            preserve_default=False,
        ),
    ]
