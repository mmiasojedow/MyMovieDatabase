from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    imdb_link = models.URLField(max_length=200)
    last_sync = models.DateTimeField(auto_now=True)
