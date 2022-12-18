from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),

    re_path(r'^movie/(?P<id>[0-9a-f]{24})/([-a-zA-Z0-9_]+/){0,1}$',
            views.movie_detail,
            name='movie_detail'),

    path('login/', views.user_login, name='login'),

    path('login/?from=<path:next_page>',
         views.user_login,
         name='login-with-redirect'),

    path('sign-up/', views.user_signup, name='signup'),

    path('logout/', views.user_logout, name='logout'),
]
