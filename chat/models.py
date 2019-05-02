from django.db import models

print(__file__)


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
