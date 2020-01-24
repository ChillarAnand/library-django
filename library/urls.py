import debug_toolbar
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import generic
from controlcenter.views import controlcenter

from book import views as bviews

admin.site.site_header = "library admin"
admin.site.site_title = "library admin portal"
admin.site.index_title = "Welcome to library admin portal"


urlpatterns = [
    url(r'^$', generic.RedirectView.as_view(url='/admin/', permanent=True), name='index'),
    url(r'^advanced_filters/', include('advanced_filters.urls')),
    url(r'^admin/dashboard/', controlcenter.urls),
    url(r'^admin/', admin.site.urls),
    # url(r'^sadmin/', admin_site.urls),
    url(r'^chat/', include('chat.urls')),
    url(r'^book/', include('book.urls')),

    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^test/$', bviews.test, name='test', ),
    url(r'^error', bviews.error, name='error', ),

    url(r'^email-book/$', bviews.email_book, name='email-book', ),
    url(r'^bf/$', bviews.book_form, name='bf', ),
    url(r'^hello', bviews.hello, name='hello', ),
]

if settings.DEBUG:
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
    if settings.SILK_ENABLED:
        urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    pass
