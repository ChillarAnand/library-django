import os

import django
from django.core.handlers import wsgi
from django.views import debug


class StaffDebugWSGIHandler(wsgi.WSGIHandler):

    def handle_uncaught_exception(self, request, resolver, exc_info):
        if hasattr(request, 'user') and request.user.is_staff:
            return debug.technical_500_response(request, *exc_info)

        return super().handle_uncaught_exception(request, resolver, exc_info)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library.settings")

django.setup(set_prefix=False)

application = StaffDebugWSGIHandler()
