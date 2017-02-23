import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand

from django.utils import autoreload


def restart_celery(*args, **kwargs):
    cmd = 'pgrep celery | xargs kill -9'
    subprocess.call(cmd, shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    script = settings.BASE_DIR + '/scripts/start_celery.sh'
    subprocess.call([script])


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Starting celery worker with autoreload...')
        autoreload.main(restart_celery, args=None, kwargs=None)
