"""moviedb_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main_app.views import (MainView, MovieDetailView, MovieNoteView,
                            MovieTagView, SyncView, TagDeleteView, TagView)
from user_app.views import LoginView, LogoutView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('sync/', SyncView.as_view(), name='sync'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie'),
    path('movie-tags/<int:pk>/', MovieTagView.as_view(), name='movie_tags'),
    path('movie-note/<int:pk>/', MovieNoteView.as_view(), name='movie_note'),
    path('tag/', TagView.as_view(), name='tag'),
    path('tag/<pk>/delete/', TagDeleteView.as_view(), name='tag_delete'),

]
