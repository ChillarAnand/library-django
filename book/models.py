from django.db import models

print(__file__)

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    borrowed = models.CharField(max_length=100, default='')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
