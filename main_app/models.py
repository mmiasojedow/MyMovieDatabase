from django.conf import settings
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=128)
    rating = models.IntegerField()
    link = models.URLField(max_length=200)
    note = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField('Tag')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name
