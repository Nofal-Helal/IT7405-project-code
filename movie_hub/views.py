from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.utils import DatabaseError
from django.forms import Form
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.utils import text, timezone
from djongo.models.fields import ObjectId

from .forms import AuthenticationForm, UserCreationForm, AddMovieFromIMDBForm, CommentForm
from .models import Movie, Comment


# Create your views here.
def homepage(request: HttpRequest) -> HttpResponse:
    context = {
        'featured_movies': Movie.objects.order_by('-dateAdded')[:5],
        'movies': Movie.objects.all()[:20]
    }
    return render(request, 'movie_hub/movies.html', context)


def movie_detail(request: HttpRequest, id: str) -> HttpResponse:
    movie = Movie.objects.get(pk=ObjectId(id))
    movie.comments = [{
        **comment, 'user':
        auth.models.User.objects.get(id=comment['user_id'])
    } for comment in movie.comments]

    comments_form = CommentForm()

    context = {'movie': movie, 'form': comments_form}
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
            movie.comments.append(comment)
            movie.save()
            return HttpResponseRedirect(
                f'/movie/{movie._id}/{text.slugify(movie.title)}')
    else:
        # this view only accepts POST
        return HttpResponseNotFound()


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
