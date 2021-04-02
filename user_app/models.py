from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    imdb_link = models.URLField(max_length=200)
    last_sync = models.DateTimeField(auto_now=True)
