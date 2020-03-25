from django.conf import settings
from django.core.checks import Error
from django.core.checks import Tags
from django.core.checks import register
from django.urls import resolve


@register(Tags.security, deploy=True)
def check_admin_path(app_configs, **kwargs):
    errors = []
    try:
        default_admin = resolve('/admin/')
    except Resolver404:
        default_admin = None
    if default_admin:
        msg = 'Found admin in default "/admin/" path'
        hint = 'Route admin via different url'
        errors.append(Error(msg, hint))
    return errors
