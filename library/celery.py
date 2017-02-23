import celery
from django.conf import settings

app = celery.Celery('library')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
