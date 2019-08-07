from django.apps import AppConfig
from django.apps import apps
from django.contrib import admin


class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(ListAdminMixin, self).__init__(model, admin_site)


class BookConfig(AppConfig):
    name = 'book'

    def ready(self):
        models = apps.get_models()
        for model in models:
            admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
            try:
                pass
                # admin.site.register(model, admin_class)
            except admin.sites.AlreadyRegistered:
                pass
