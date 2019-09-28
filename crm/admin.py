from django.contrib import admin
from django.contrib.postgres import fields
from django.utils.html import format_html
from django_json_widget.widgets import JSONEditorWidget

from crm.models import House


class HouseAdmin(admin.ModelAdmin):
    def url_for_result(self, house):
        html_string = format_html(u'<a href="/admin/crm/house/{}/change/">{}', house.id, house.id)
        return html_string

    list_display = ('id', 'url_for_result', 'id',)


# admin.site.register(House, HouseAdmin)

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'data')
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }
