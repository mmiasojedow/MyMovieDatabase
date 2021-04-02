from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
import requests
from bs4 import BeautifulSoup

from main_app.models import Movie
from main_app.scraper import *

User = get_user_model()


class MainView(View):
    def get(self, request):
        user = request.user
        if user.is_anonymous:
            return render(request, 'main_app/base.html')
        else:
            movies = Movie.objects.filter(user=user)
            return render(request, 'main_app/base.html', {'movies': movies})


class SyncView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        movies = len(Movie.objects.filter(user=user))
        return render(request, 'main_app/sync.html', {'movies': movies})

    def post(self, request):
        user = request.user
        movies = len(Movie.objects.filter(user=user))
        if movies > 0:
            get_new_movies(user)
        else:
            get_all_movies(user)
        return redirect('main')
