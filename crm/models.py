from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.


class House(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    data = JSONField(default=dict, null=True, blank=True)
