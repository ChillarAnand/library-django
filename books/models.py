from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class AuthorQuerySet(models.QuerySet):
    pass


class AuthorManager(models.Manager):
    def get_queryset(self):
        return AuthorQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().filter(active=True)




class BookQuerySet(models.QuerySet):
    pass


class BookManager(models.Manager):
    def get_queryset(self):
        qs = BookQuerySet(self.model, using=self._db)
        # qs = qs.select_related('author')
        qs = qs.prefetch_related('author')
        # qs = qs.filter(author__isnull=False)
        return qs

    def active(self):
        return self.get_queryset().filter(active=True)


class Author(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True, help_text='Please enter the date in <b>YYYY-MM-DD</b> format.')
    active = models.NullBooleanField(default=False)

    objects = AuthorManager()

    def __str__(self):
        return self.name


class TimeAuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Book(TimeAuditModel):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=100)
    is_available = models.BooleanField(default=True, help_text='Is the books available to buy?')
    published_date = models.DateField(null=True, blank=True, help_text='Please enter the date in <b>YYYY-MM-DD</b> format.')
    cover = models.FileField(null=True, blank=True, upload_to='files/')
    rating = models.FloatField(null=True, blank=True)
    format = JSONField(blank=True, null=True)

    # sobjects = BookManager()

    def __str__(self):
        return self.name or ''


class Article(TimeAuditModel):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)


class BookProxy(Book):
    class Meta:
        proxy = True


class Library(models.Model):
    name = models.CharField(max_length=256)


class BestSeller(models.Model):
    book = models.ForeignKey('Book', null=True, blank=True, on_delete=models.SET_NULL)
    year = models.IntegerField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('index')

    def __str__(self):
        if self.book:
            return self.book.name or ''
        else:
            return ''


class BorrowedBook(models.Model):
    book = models.ForeignKey('Book', null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    borrowed_date = models.DateField(null=True, blank=True)


class BorrowedBookDashboard(BorrowedBook):
    class Meta:
        proxy = True
