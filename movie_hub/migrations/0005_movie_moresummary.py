# Generated by Django 4.1.3 on 2022-12-17 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movie_hub", "0004_movie_indexes"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="moreSummary",
            field=models.TextField(blank=True),
        ),
    ]
