from django.conf.urls import url
from django.contrib import admin

from book import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.BookListView.as_view(), name='books'),
]
