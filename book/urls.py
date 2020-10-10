from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from book import views

router = SimpleRouter()

router.register(r'authors', views.AuthorViewSet, 'author')
router.register(r'books', views.BookViewSet, 'books')

urlpatterns = [
    url(r'^bf$', views.book_form, name='book_form'),
    url(r'^comp$', views.comp, name='comp'),
    url(r'^sleep$', views.sleep, name='sleep'),
]

urlpatterns += router.urls
