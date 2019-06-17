from django.contrib import admin
from django.utils.html import format_html


try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from .models import Book
from crm.models import House


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'delete', )
    search_fields = ('name',)
    list_display = ('name', 'author_link', 'name', 'name')
    list_display = ('name', 'author', 'name', 'name')
    list_display = ('name', 'author', 'borrowed')
    list_display = ('name', 'author', 'borrowed', 'name', 'name')

    list_display_links = ('name', 'author',)

    def author_link(self, book):
        link = reverse("admin:book_author_change", args=[book.author.id])
        return u'<a href="%s">%s</a>' % (link, book.author.name)
    author_link.allow_tags = True
    author_link.short_description = 'Author'

    # autocomplete_fields = ['author']

    def delete(self, book):
        link = reverse("admin:book_book_delete", args=[book.pk])
        button = '<input type="button" onclick="location.href=\'{}\'" value="Delete" />'
        return button.format(link)
    delete.allow_tags = True
    delete.short_description = 'Delete book'


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


from speedinfo.models import ViewProfiler

admin.site.unregister(ViewProfiler)
