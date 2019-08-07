from django.db import models


class Fruit(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)


class Basket(models.Model):
    limit_choices_to = {'id_in': [2, 3]}
    name = models.CharField(max_length=50, blank=True, null=True)
    fruits = models.ManyToManyField(Fruit, through="BasketFruit")
    # fruits = models.ManyToManyField(Fruit)



class BasketFruit(models.Model):
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE, null=True, blank=True)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
