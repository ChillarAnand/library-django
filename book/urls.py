from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from book import views

router = SimpleRouter()

router.register(r'author', views.AuthorViewSet, 'Author')
router.register(r'book', views.BookViewSet, 'Book')

urlpatterns = [
    url(r'^bf$', views.book_form, name='book_form'),
] + router.urls
