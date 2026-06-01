from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import admin

# Create your models here.
class Libro(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    pages = models.IntegerField()
    published_year = models.DateField()

    def __str__(self):
        return self.title
    
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pages', 'published_year')
    search_fields = ('title', 'author')
    list_filter = ('published_year',)

