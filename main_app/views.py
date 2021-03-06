from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import DeleteView
from django.core.paginator import Paginator


from main_app.forms import MovieNoteForm, TagForm
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
            search = request.GET.get('search')
            if search:
                if search.startswith('#'):
                    search = '%23' + search[1:]
                    try:
                        tag = Tag.objects.get(
                            user=user, name__icontains='#' + search[3:])
                        movies = Movie.objects.filter(user=user, tags=tag)
                    except:
                        movies = []
                        status = 'Nie masz takiego tagu'
                else:
                    movies = Movie.objects.filter(
                        user=user, title__icontains=search)
                    if len(movies) == 0:
                        status = 'Nie masz takiego filmu'
            else:
                movies = Movie.objects.filter(user=user)
            order_by = request.GET.get('order_by', 'pk')
            if order_by and len(movies) is not 0:
                movies = movies.order_by(order_by)
            paginator = Paginator(movies, 10)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
            return render(request, 'main_app/base.html', {'page': page, 'search': search, 'order_by': order_by, 'status': status})


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
