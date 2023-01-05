from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.utils import DatabaseError
from django.forms import Form
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.utils import text, timezone
from djongo.models.fields import ObjectId
from math import ceil

from .forms import AuthenticationForm, UserCreationForm, AddMovieFromIMDBForm, CommentForm
from .models import Movie, Comment


# Create your views here.
def homepage(request: HttpRequest) -> HttpResponse:
    context = {
        'featured_movies':
        Movie.objects.order_by('-dateAdded')[:8],
        'latest_movies':
        Movie.objects.order_by('-dateAdded')[:12],
        'top_movies':
        Movie.objects.mongo_find({}, sort=[('imdb.rating', -1)])[:12],
    }
    return render(request, 'movie_hub/movies.html', context)


def movie_detail(request: HttpRequest, id: str) -> HttpResponse:
    movie = Movie.objects.get(pk=ObjectId(id))
    movie.comments = [{
        **comment, 'user':
        auth.models.User.objects.get(id=comment['user_id'])
    } for comment in movie.comments]

    comments_form = CommentForm()
    num_comments = len(movie.comments)
    avg = sum(map(lambda c: c['rating'], movie.comments)) / num_comments

    context = {
        'movie': movie,
        'form': comments_form,
        'avg': avg,
        'num_comments': num_comments
    }
    return render(request, 'movie_hub/movie_detail.html', context)


def movie_comment_form(request: HttpRequest, id: str) -> HttpResponse:
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = {}
            comment['user_id'] = request.user.id
            comment['rating'] = form.cleaned_data['rating']
            comment['text'] = form.cleaned_data['text']
            comment['date'] = timezone.now()
            movie = Movie.objects.get(pk=ObjectId(id))
            movie.comments.insert(0, comment)
            movie.save()
            return HttpResponseRedirect(
                f'/movie/{movie._id}/{text.slugify(movie.title)}')
    else:
        # this view only accepts POST
        return HttpResponseNotFound()


def movies_search(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('q', default="")
    movies = Movie.objects.mongo_find({'$text': {'$search': query}})
    context = {'movies': movies, 'query': query}
    return render(request, 'movie_hub/movies_search.html', context)


movies_per_page = 18


def pages(current: int, count: int = Movie.objects.count()) -> dict:
    last_page = ceil(count / movies_per_page)
    pages = {
        'previous': current - 1 if current > 1 else 1,
        'current': current,
        'next': current + 1 if current < last_page else last_page,
        'last_page': last_page,
        'pages': range(1, last_page + 1)
    }
    return pages


def movies_top(request: HttpRequest) -> HttpResponse:
    page = request.GET.get('page', default=1)
    try:
        page = int(page)
        if not page > 0: raise Exception()
    except Exception:
        page = 1

    start = (page - 1) * movies_per_page
    end = start + movies_per_page
    movies = Movie.objects.mongo_find({},
                                      sort=[('imdb.rating', -1)])[start:end]
    context = {
        'movies': movies,
        'title': 'Top Rated Movies',
        'page': page,
        'pages': pages(page)
    }
    return render(request, 'movie_hub/movies_paginated.html', context)


def movies_latest(request: HttpRequest) -> HttpResponse:
    page = request.GET.get('page', default=1)
    try:
        page = int(page)
        if not page > 0: raise Exception()
    except Exception:
        page = 1

    start = (page - 1) * movies_per_page
    end = start + movies_per_page
    movies = Movie.objects.order_by('-dateAdded')[start:end]
    context = {
        'movies': movies,
        'title': 'Latest Movies',
        'pages': pages(page)
    }
    return render(request, 'movie_hub/movies_paginated.html', context)


def movies_genres(request: HttpRequest, genre: str) -> HttpResponse:
    page = request.GET.get('page', default=1)
    try:
        page = int(page)
        if not page > 0: raise Exception()
    except Exception:
        page = 1

    start = (page - 1) * movies_per_page
    end = start + movies_per_page
    num_movies = Movie.objects.mongo_count_documents({'genres': genre})
    movies = Movie.objects.mongo_find({'genres': genre})[start:end]
    context = {
        'movies': movies,
        'title': genre + ' Movies',
        'genre': genre,
        'pages': pages(page, num_movies)
    }
    return render(request, 'movie_hub/movies_genres.html', context)


def user_login(request: HttpRequest, next_page='/') -> HttpResponse:
    from django.contrib.auth.views import LoginView

    # Use auth's LoginView with customized form
    return (LoginView.as_view(next_page=next_page,
                              authentication_form=AuthenticationForm,
                              extra_context={'next_page': next_page})(request))


def user_signup(request: HttpRequest, next_page='/') -> HttpResponse:
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
            return HttpResponseRedirect(next_page)
        else:
            form.updateClasses()
    else:
        # create blank form
        form = UserCreationForm()

    context = {'form': form, 'next_page': next_page}
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
