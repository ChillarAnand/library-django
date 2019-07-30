from django.db import models


class Foo(models.Model):
    foo_field1 = models.CharField(max_length=50, blank=True, null=True)


class Main(models.Model):
    main_field1 = models.CharField(max_length=50, blank=True, null=True)
    m2mfield = models.ManyToManyField(Foo, through="FooBar", null=True)
    # m2mfield = models.ManyToManyField(Foo)


class FooBar(models.Model):
    main = models.ForeignKey(Main, on_delete=models.CASCADE, null=True, blank=True)
    foo = models.ForeignKey(Foo, on_delete=models.CASCADE, null=True, blank=True)
    new_field = models.CharField(max_length=50, null=True, blank=True)
