import debug_toolbar
# import object_tools
from controlcenter.views import controlcenter
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.views import generic

from book import views as bviews

admin.site.site_header = "library admin"
admin.site.site_title = "library admin portal"
admin.site.index_title = "Welcome to library admin portal"
# from django_otp.admin import OTPAdminSite

# admin.site.__class__ = OTPAdminSite
# from django.contrib.admin import sites
#
# library_admin_site = LibraryOTPAdminSite()
# admin.site = library_admin_site
# sites.site = library_admin_site

from library.admin import LibraryOTPAdminSite

ladmin = LibraryOTPAdminSite()


def trigger_error(request):
    division_by_zero = 1 / 0
    return division_by_zero


urlpatterns = [
    path('sentry', trigger_error),
    path('sentry/', trigger_error),
    path('sentry2/', trigger_error),
    # path('jet_api/', include('jet_django.urls')),

    # url(r'^object-tools/', object_tools.tools.urls),
    url(r'^$', generic.RedirectView.as_view(url='/admin/', permanent=True), name='index'),
    # url(r'^advanced_filters/', include('advanced_filters.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^ladmin/', ladmin.urls),
    # url(r'^hadmin/', include('admin_honeypot.urls', namespace='admin_honeypot')),

    # url(r'^sadmin/', admin_site.urls),
    url(r'^chat/', include('chat.urls')),
    url(r'^book/', include('book.urls')),

    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^test/$', bviews.test, name='test', ),
    url(r'^error', bviews.error, name='error', ),

    url(r'^email-book/$', bviews.email_book, name='email-book', ),
    url(r'^bf/$', bviews.book_form, name='bf', ),
    url(r'^hello', bviews.hello, name='hello', ),

    # url(r'jet_api/', include('jet_django.urls')),
    url(r'^admin/dashboard/', controlcenter.urls),

    url(r'^silk/', include('silk.urls', namespace='silk')),

    path('^.*', bviews.black_hole),
    path('^.*/', bviews.black_hole),
    re_path(r'^(?P<path>.*)/$', bviews.black_hole),
    path('', bviews.black_hole),
]

if settings.DEBUG:
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
