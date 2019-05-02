import json
import sys
from asgiref.sync import async_to_sync
from channels.generic.websocket import SyncConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from django.conf import settings

channel_layer = get_channel_layer()
print(__file__)


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


class EmailBook(SyncConsumer):
    def send_email(self, message):
        print(message)


class LibraryWebsocketConsumer(WebsocketConsumer):
    http_user_and_session = False
    strict_ordering = False

    def connect(self, cls=None):
        if not cls:
            cls = self
        if settings.TEST:
            print('WS connected: {}'.format(cls.__class__.__name__))
            sys.stdout.flush()
        self.accept()

    def disconnect(self, close_code=None):
        if settings.TEST:
            cls = self
            async_to_sync(cls.channel_layer.group_discard)(
                cls.room_group_name,
                cls.channel_name
            )
            print('WS disconnected: {}'.format(cls.__class__.__name__))
            sys.stdout.flush()

    def receive(self, cls=None, text_data=None):
        cls = self
        if settings.TEST:
            print('WS received: {} {}'.format(cls.__class__.__name__, text_data))
            sys.stdout.flush()

    def message(self, event):
        cls = self
        if settings.TEST:
            print('WS sent: {} {}'.format(cls.__class__.__name__, event))
            sys.stdout.flush()
        message = event['message']
        self.send(text_data=json.dumps(message))


class EchoConsumer(LibraryWebsocketConsumer):
    def connect(self):
        super().connect()
        self.room_group_name = 'echo'
        async_to_sync(channel_layer.group_add)(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        super().receive()
        group_name = 'echo'
        data = {'type': 'message', 'message': text_data}
        async_to_sync(channel_layer.group_send)(group_name, data)
