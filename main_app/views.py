import requests
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import DeleteView

from main_app.forms import MovieNoteForm, SearchForm, TagForm
from main_app.models import Movie, Tag
from main_app.scraper import get_all_movies, get_new_movies

User = get_user_model()


class MainView(View):
    def get(self, request):
        user = request.user
        status = 'Twoje filmy'
        if user.is_anonymous:
            return render(request, 'main_app/base.html')
        else:
            form = SearchForm()
            movies = Movie.objects.filter(user=user)
            return render(request, 'main_app/base.html', {'movies': movies, 'form': form, 'status': status})

    def post(self, request):
        user = request.user
        form = SearchForm(request.POST)
        if form.is_valid():
            status = 'Wyniki wyszukiwania'
            name = form.cleaned_data['name']
            if name.startswith('#'):
                try:
                    tag = Tag.objects.get(user=user, name__icontains=name)
                    movies = Movie.objects.filter(user=user, tags=tag)
                except:
                    movies = []
                    status = 'Nie masz takiego tagu'
            else:
                movies = Movie.objects.filter(user=user, title__icontains=name)
            return render(request, 'main_app/base.html', {'movies': movies, 'form': form, 'status': status})
        else:
            status = 'Twoje filmy'
            return render(request, 'main_app/base.html', {'movies': movies, 'form': form, 'status': status})


class SyncView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        movies = len(Movie.objects.filter(user=user))
        return render(request, 'main_app/sync.html', {'movies': movies})

    def post(self, request):
        user = request.user
        movies = len(Movie.objects.filter(user=user))
        try:
            if movies > 0:
                get_new_movies(user)
                return redirect('main')
            else:
                get_all_movies(user)
                return redirect('main')
        except:
            return redirect('main')


class MovieDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        return render(request, 'main_app/movie.html', {'movie': movie})


class MovieTagView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = request.user
        movie = Movie.objects.get(pk=pk)
        tags = Tag.objects.filter(user=user)
        return render(request, 'main_app/movie_tag.html', {'movie': movie, 'tags': tags})

    def post(self, request, pk):
        user = request.user
        movie = Movie.objects.get(pk=pk)
        tags = Tag.objects.filter(user=user)
        chosen_tags = request.POST.getlist('tags')
        new_tags = []
        for tag in chosen_tags:
            new_tags.append(Tag.objects.get(pk=tag))
        movie.tags.set(new_tags)
        return render(request, 'main_app/movie.html', {'movie': movie, 'tags': tags})


class MovieNoteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        form = MovieNoteForm()
        return render(request, 'main_app/movie_note.html', {'movie': movie, 'form': form})

    def post(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        form = MovieNoteForm(request.POST)
        if form.is_valid():
            note = form.cleaned_data['note']
            movie.note = note
            movie.save()
        return render(request, 'main_app/movie.html', {'movie': movie, 'form': form})


class TagView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        tags = Tag.objects.filter(user=user)
        form = TagForm()
        return render(request, 'main_app/tag.html', {'tags': tags, 'form': form})

    def post(self, request):
        user = request.user
        tags = Tag.objects.filter(user=user)
        form = TagForm(request.POST)
        if form.is_valid():
            name = '#' + form.cleaned_data['name']
            if Tag.objects.filter(name=name, user=user).count() == 0:
                Tag.objects.create(user_id=user.id, name=name)
            return render(request, 'main_app/tag.html', {'tags': tags, 'form': form})
        else:
            return render(request, 'main_app/tag.html', {'tags': tags, 'form': form})


class TagDeleteView(DeleteView):
    model = Tag
    success_url = reverse_lazy('tag')
