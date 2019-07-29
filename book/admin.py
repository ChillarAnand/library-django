from django.contrib import admin
from django.utils.html import format_html


try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from .models import Author, Book
from crm.models import House


class BookAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    # autocomplete_fields = ['author']

    list_display = ('name', 'author', 'delete', )
    list_display = ('name', 'author', 'author_link', 'delete', 'borrowed', 'is_available', 'name', 'name')

    # list_display_links = ('name', 'author',)

    def author_link(self, book):
        link = reverse("admin:book_author_change", args=[book.author.id])
        html = '<a href="{}">{}</a>'.format(link, book.author.name)
        return format_html(html)
    author_link.short_description = 'Author'

    def delete(self, book):
        link = reverse("admin:book_book_delete", args=[book.pk])
        html = '<input type="button" onclick="location.href=\'{}\'" value="Delete" />'.format(link)
        return format_html(html)
    delete.short_description = 'Delete'

    def toggle_availability(self, book):
        html = ''
        return format_html(html)

class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name',)


# admin.site.register(Author)
# admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
# admin.site.register(Book)


class HouseAdmin(admin.ModelAdmin):
    def url_for_result(self, house):
        html_string = format_html(u'<a href="/admin/crm/house/{}/change/">{}', house.id, house.id)
        return html_string

    list_display = ('id', 'url_for_result', 'id', )


admin.site.register(House, HouseAdmin)


from django.apps import apps


class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(ListAdminMixin, self).__init__(model, admin_site)


models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass

from django.apps import apps

models = apps.get_models()

for model in models:
    try:
        print(model)
        # admin.site.register(model)
    except:
        pass

from speedinfo.models import ViewProfiler

admin.site.unregister(ViewProfiler)
