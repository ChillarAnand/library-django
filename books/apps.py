from django.apps import AppConfig
from django.apps import apps
from django.contrib import admin


class ListModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super().__init__(model, admin_site)


class BookConfig(AppConfig):
    name = 'books'

    def ready(self):
        models = apps.get_models()
        for model in models:
            try:
                # admin.site.register(model, ListModelAdmin)
                pass
            except admin.sites.AlreadyRegistered:
                pass
