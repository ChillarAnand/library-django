from django.conf.urls import url, include
from django.contrib import admin
from book import views as bviews


admin.site.site_header = "library admin"
admin.site.site_title = "library admin portal"
admin.site.index_title = "Welcome to library admin portal"


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^chat/', include('chat.urls')),

    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^test/$', bviews.test, name='test', ),

    url(r'^$', bviews.hello, name='hello', ),
]
