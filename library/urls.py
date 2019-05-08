from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

from book import views as bviews

admin.site.site_header = "library admin"
admin.site.site_title = "library admin portal"
admin.site.index_title = "Welcome to library admin portal"


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^chat/', include('chat.urls')),
    url(r'^book/', include('book.urls')),

    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^test/$', bviews.test, name='test', ),
    url(r'^error', bviews.error, name='error', ),

    url(r'^email-book/$', bviews.email_book, name='email-book', ),
    url(r'^bf/$', bviews.book_form, name='bf', ),
    url(r'^hello$', bviews.hello, name='hello', ),
]


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
#     urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
