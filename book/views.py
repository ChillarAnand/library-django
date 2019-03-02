from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import connection
from django.http import HttpResponse



channel_layer = get_channel_layer()


def test(request):
    return HttpResponse({'test passed'})


def error(request):
    return someerror


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


def home(request):
    from silk.models import Request
    data = Request.objects.all()
    query = '''
    SELECT s.*,
       (s.atime * s.cpath) as ifactor
  FROM (
        select path,
               avg(time_taken) as atime,
               count(path) as cpath
          from silk_request
         group by PATH
       ) s
 ORDER BY ifactor DESC;
'''
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()

    column_width=20
    for row in data:
        for el in row:
            print(str(el).ljust(column_width), sep='')
        print

    return HttpResponse({'home'})
