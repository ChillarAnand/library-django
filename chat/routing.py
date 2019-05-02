from django.conf.urls import url

from . import consumers

print(__file__)

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
    url(r'^ws/echo/$', consumers.EchoConsumer),
]
