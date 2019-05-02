from django.apps import AppConfig

print('chat apps')


class ChatConfig(AppConfig):
    name = 'chat'
    print('chat appconfig')


print(__file__)
