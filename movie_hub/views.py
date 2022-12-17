from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from djongo.models.fields import ObjectId
from typing import Optional

from .models import Movie


# Create your views here.
def homepage(request: HttpRequest) -> HttpResponse:
    context = {
        'featured_movies': Movie.objects.order_by('-dateAdded')[:5],
        'movies': Movie.objects.all()[:20]
    }
    return render(request, 'movie_hub/movies.html', context)


def movie_detail(request: HttpRequest, id: str) -> HttpResponse:
    movie = Movie.objects.get(pk=ObjectId(id))
    return render(request, 'movie_hub/movie_detail.html', {'movie': movie})

