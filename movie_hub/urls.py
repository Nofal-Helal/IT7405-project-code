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

    path('---admin-add-movies.62b0/',
         views.admin_add_movies, 
         name='admin-add-movies'),
]
