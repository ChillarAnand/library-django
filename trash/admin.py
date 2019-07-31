from django.contrib import admin

from .models import *


class M2MInlineAdmin(admin.TabularInline):
    model = Main.m2mfield.through
    extra = 1


class MainAdmin(admin.ModelAdmin):
    inlines = [M2MInlineAdmin,]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        print('called formfield_for_manytomany')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_field_queryset(self, db, db_field, request):
        print('called get_field_queryset')
        return super().get_field_queryset(db, db_field, request)


admin.site.register(Main, MainAdmin)
