from django.db import models

# Create your models here.


class House(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
