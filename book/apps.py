from django.apps import AppConfig

print(__file__)

from django.apps import apps

print('books app config')

class BookConfig(AppConfig):
    name = 'book'

    print('books app config')
