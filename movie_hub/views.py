from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import Movie

# Create your views here.
def homepage(request: HttpRequest) -> HttpResponse:
    context = {
        'featured_movies': Movie.objects.order_by('dateAdded')[:5],
        'movies': Movie.objects.all()
    }
    return render(request, 'movie_hub/movies.html', context) 
