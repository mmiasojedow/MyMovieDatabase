from django.contrib import admin

from main_app.models import Movie, Tag

# Register your models here.

admin.site.register(Movie)
admin.site.register(Tag)
