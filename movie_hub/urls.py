from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    re_path(r'^movie/(?P<id>[0-9a-f]{24})/([-a-zA-Z0-9_]+/){0,1}$', views.movie_detail, name='movie_detail'),
]
