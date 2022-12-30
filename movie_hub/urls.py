from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),

    re_path(r'^movie/(?P<id>[0-9a-f]{24})/([-a-zA-Z0-9_]+/){0,1}$',
            views.movie_detail,
            name='movie_detail'),

    path('login/', views.user_login, name='login'),

    path('login/?next=<path:next_page>',
         views.user_login,
         name='login-with-redirect'),

    path('sign-up/', views.user_signup, name='signup'),

    path('sign-up/?next=<path:next_page>', 
         views.user_signup, 
         name='signup-with-redirect'),

    path('logout/', views.user_logout, name='logout'),

    re_path(r'^comment/(?P<id>[0-9a-f]{24})/$',
            views.movie_comment_form,
            name="movie_comment_form"),

    path('movies/search/', views.movies_search, name="movies_search"),

    path('movies/top/', views.movies_top, name="movies_top"),

    re_path(r'^movies/(?:latest/){0,1}$', views.movies_latest, name="movies_latest"),

    re_path((r'^movies/genre/(?P<genre>Action|Adventure|Animation|Comedy|'
             r'Crime|Documentary|Drama|Family|Fantasy|History|Horror|Music|'
             r'Mystery|Romance|Sci-Fi|Thriller|War|Western)/$'),
            views.movies_genres,
            name="movies_genres"),

    path('---admin-add-movies.62b0/',
         views.admin_add_movies, 
         name='admin-add-movies'),
]
