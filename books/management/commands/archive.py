import time
import gzip
import glob
import json
import os

from django.core.management.base import BaseCommand
from django.utils.timezone import now, activate, localtime
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        while True:
            for i in range(10000):
                time.sleep(0.01)
            # print('archive')
            # time.sleep(10)
