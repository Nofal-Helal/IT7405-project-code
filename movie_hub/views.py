from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.utils import DatabaseError
from django.forms import Form
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from djongo.models.fields import ObjectId

from .forms import AuthenticationForm, UserCreationForm, AddMovieFromIMDBForm
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


def user_login(request: HttpRequest, next_page='/') -> HttpResponse:
    from django.contrib.auth.views import LoginView

    # Use auth's LoginView with customized form
    return (LoginView.as_view(next_page=next_page,
                              authentication_form=AuthenticationForm)(request))


def user_signup(request: HttpRequest) -> HttpResponse:
    form: Form

    if request.method == 'POST':
        # process submitted form if valid
        form = UserCreationForm(request.POST)
        form_is_valid: bool
        try:
            form_is_valid = form.is_valid()
        except DatabaseError as e:
            form_is_valid = False
            form.add_error('username',
                           'A user with this username already exists.')

        if form_is_valid:
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            form.updateClasses()
    else:
        # create blank form
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/signup.html', context)


def user_logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_add_movies(request: HttpRequest) -> HttpResponse:
    from .downloadMovieData import get_movie_Model

    form: Form
    if request.method == 'POST':
        # process submitted form if valid
        form = AddMovieFromIMDBForm(request.POST)
        if form.is_valid():
            movies_added = 0
            movies_failed = []
            for movie_id in form.cleaned_data['ids']:
                try:
                    movie = get_movie_Model(movie_id)
                    movie.save()
                    movies_added += 1
                except Exception:
                    movies_failed.append(movie_id)

            context = {
                'form': form,
                'movies_added': movies_added,
                'movies_failed': movies_failed
            }
            return render(request, 'movie_hub/add_movies_imdb.html', context)
        else:
            form.updateClasses()
    else:
        # create blank form
        form = AddMovieFromIMDBForm()

    context = {'form': form}
    return render(request, 'movie_hub/add_movies_imdb.html', context)
