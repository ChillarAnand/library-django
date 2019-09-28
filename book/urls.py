from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from book import views

router = SimpleRouter()

router.register(r'author', views.AuthorViewSet, 'Author')
router.register(r'books', views.BookViewSet, 'Book')

urlpatterns = [
                  url(r'^bf$', views.book_form, name='book_form'),
                  url(r'^comp$', views.comp, name='comp'),
                  url(r'^sleep$', views.sleep, name='sleep'),
] + router.urls
