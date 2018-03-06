from django.shortcuts import render
from django.http import HttpResponse


def hello(request):
    from celery import Celery
    celery = Celery()
    celery.config_from_object('library.settings.base')
    celery.send_task('library.settings.base.add', (2,2))

    return HttpResponse({'hello'})
