from django.db import models

from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    authors = models.ManyToManyField(Author)
    genres = models.ManyToManyField(Genre)
    published_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
