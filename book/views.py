from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse


channel_layer = get_channel_layer()


def test(request):
    return HttpResponse({'test passed'})


def hello(request):
    from celery import Celery
    celery = Celery()
    celery.config_from_object('library.settings.base')
    celery.send_task('library.settings.base.add', (2, 2))
    return HttpResponse({'hello'})


def email_book(request):
    async_to_sync(channel_layer.send)(
        "email-book",
        {
            'type': 'send-email',
            'id': 12,
            'message': 'message',
        }
    )
    return HttpResponse({'book emailed'})
