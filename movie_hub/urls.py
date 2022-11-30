from django.urls import path
from movie_hub import views

urlpatterns = [
    path('', views.homepage, name='home')
]
