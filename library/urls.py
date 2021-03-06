import debug_toolbar
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from books import views as bviews

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
    url(r'^$', bviews.home, name='home'),

    path('error', trigger_error),

    url(r'^admin/', admin.site.urls),

    url(r'^books/', include('books.urls')),

    # path('jet_api/', include('jet_django.urls')),
    # url(r'^object-tools/', object_tools.tools.urls),
    # url(r'^$', generic.RedirectView.as_view(url='/admin/', permanent=True), name='index'),
    # url(r'^advanced_filters/', include('advanced_filters.urls')),
    # url(r'^hadmin/', include('admin_honeypot.urls', namespace='admin_honeypot')),

    # url(r'^sadmin/', admin_site.urls),
    # url(r'^chat/', include('chat.urls')),

    url(r'^email-books/$', bviews.email_book, name='email-books', ),

    url(r'^silk/', include('silk.urls', namespace='silk')),

    # path('^.*', bviews.black_hole),
    # path('^.*/', bviews.black_hole),
    # re_path(r'^(?P<path>.*)/$', bviews.black_hole),
    # path('', bviews.black_hole),
]

if settings.DEBUG:
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
