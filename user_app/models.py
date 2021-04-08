from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    imdb_link = models.URLField(max_length=200)
